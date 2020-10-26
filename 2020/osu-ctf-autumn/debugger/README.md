## debugger

Points: 10

After looking at the source code, it looks like the ideal place to set a
breakpoint would be on the `memset` call. We can open up `pwn` in gdb:

```gdb
(gdb) disassemble main
Dump of assembler code for function main:
   0x0000000000400577 <+0>: push   %rbp
   0x0000000000400578 <+1>: mov    %rsp,%rbp
...
   0x0000000000400644 <+205>:   mov    %rax,%rdi
   0x0000000000400647 <+208>:   callq  0x400480 <memset@plt>
   0x000000000040064c <+213>:   lea    0xe0(%rip),%rdi        # 0x400733
End of assembler dump.
```

We can set a breakpoint at the `memset` call like so:
```gdb
(gdb) break *0x0000000000400647
Breakpoint 1 at 0x400647: file pwn.c, line 11.
```

Then we can `run` the program. To see the flag, we can do `print
decrypted_flag` which gives us `osuctf{brutus_l0ves_br3akpoints}`
