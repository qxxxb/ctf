login:
  $rsp = 0xffffc2b0
  &passcode1 = 0xffffc2b8
  &passcode2 = 0xffffc2bc

&passcode1 catches the last 4 bytes of `name`

payload = '0' * 96
payload += 0xffffc2b8

input:
  First 4 bytes: 338150
  Last 4 byteS: 13371337

## Plan

We can overwrite the value of `passcode1`.
We can use `scanf` to set 8 bytes of memory located at `passcode1`.

For some reason, when we try to put the address of `passcode1` as its value,
nothing happens after the `scanf` call. The idea was that the `scanf` would
overwrite the values of both `passcode1` and `passcode2`. However, there values
didn't change at all. I'm not sure why this didn't work. Maybe it's because the
value of `passcode1` was sign-extended from 4 bytes to 8 bytes, making it point
to a completely different address.

Anyway, we have to come up with a different plan now. What address should we
modify?

Immediately after the call to `scanf`, we call `fflush(stdin)`. Since this is
the first calling `fflush`, it isn't mapped to a real address yet.

### Aside on the GOT and PLT

- `plt`: Procedure Linkage Table
- `got`: Global Offset Table

The `plt` is always called first. Each entry in the `plt` looks like this:
- The first instruction is a jump to a function pointer
  - We must dereference it before we jump
  - If it's the first time calling this function, this function pointer points
    to an entry in the `.got.plt`.
      - This entry is initially simply set to the address of the next
        instruction of the `plt` entry.
  - If it's not the first time calling this function, this function pointer
    already points to the calculated real address. We just jump there and never
    execute the subsequent instructions.
- The next instructions are as follows:
  - Push some constant to the stack (a parameter representing the slot number)
  - Jump to a constant address (routine for calculating real address)
  - Set the function pointer of the `plt` entry to the calculated real address

Relocation Read-Only (RELRO) settings:
- Partial
  - `plt` is read-only
  - `.got.plt` is writeable
  - This means that if we control the address of `.got.plt` and it's the first
    time calling the function, we will jump to that address we specified
- Complete
  - `plt` and `.got.plt` are prepopulated by the linker when the program starts
  - Write access is removed
  - Exploit not possible

More info: https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html.

---

Our goal is to write the jump destination in the `.got.plt` for `fflush`
