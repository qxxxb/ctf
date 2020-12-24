Value of rdx
pwndbg> p $rbp-8
$2 = (void *) 0x7fffffffd418

We can control the value of `rdx`, so we can call any function.
But how do we specify the parameters? Can we use a ROP chain?

pwndbg> p system
$3 = {int (const char *)} 0x7ffff7e36f20 <__libc_system>

pwndbg> print system
$1 = {<text variable, no debug info>} 0x4004b0 <system@plt>

pwndbg> search /bin/sh
chall_04        0x4006b8 0x68732f6e69622f /* '/bin/sh' */
chall_04        0x6006b8 0x68732f6e69622f /* '/bin/sh' */
libc-2.31.so    0x7ffff7f78156 0x68732f6e69622f /* '/bin/sh' */

0x4005dc <vuln+18>    lea    rax, [rbp - 0x40]
