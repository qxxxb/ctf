► 0x555555554756 <main+60>    call   fgets@plt <fgets@plt>
       s: 0x7fffffffd380 ◂— 0x0
       n: 0xc7
       stream: 0x7ffff7fac980 (_IO_2_1_stdin_) ◂— 0xfbad2088

n = 199

pwndbg> reg rdx
*RDX  0x555555554610 (_start) ◂— xor    ebp, ebp

pwndbg> disassemble vuln
Dump of assembler code for function vuln:
   0x0000555555554768 <+0>:	push   rbp
   0x0000555555554769 <+1>:	mov    rbp,rsp
   0x000055555555476c <+4>:	sub    rsp,0x240
   0x0000555555554773 <+11>:	lea    rdi,[rip+0xe6]        # 0x555555554860
   0x000055555555477a <+18>:	call   0x5555555545d0 <puts@plt>
   0x000055555555477f <+23>:	mov    rdx,QWORD PTR [rip+0x20088a]        # 0x555555755010 <stdin@@GLIBC_2.2.5>
   0x0000555555554786 <+30>:	lea    rax,[rbp-0x40]
   0x000055555555478a <+34>:	mov    esi,0x64
   0x000055555555478f <+39>:	mov    rdi,rax
   0x0000555555554792 <+42>:	call   0x5555555545f0 <fgets@plt>
   0x0000555555554797 <+47>:	mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555479b <+51>:	mov    eax,0x0
   0x00005555555547a0 <+56>:	call   rdx
   0x00005555555547a2 <+58>:	nop
   0x00005555555547a3 <+59>:	leave
   0x00005555555547a4 <+60>:	ret
