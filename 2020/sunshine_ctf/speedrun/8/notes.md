pwndbg> disassemble main
Dump of assembler code for function main:
   0x000000000040057a <+0>:	push   rbp
   0x000000000040057b <+1>:	mov    rbp,rsp
   0x000000000040057e <+4>:	sub    rsp,0x10
   0x0000000000400582 <+8>:	lea    rax,[rbp-0x4]
   0x0000000000400586 <+12>:	mov    rsi,rax
   0x0000000000400589 <+15>:	lea    rdi,[rip+0xdc]        # 0x40066c
   0x0000000000400590 <+22>:	mov    eax,0x0
   0x0000000000400595 <+27>:	call   0x400470 <__isoc99_scanf@plt>
   0x000000000040059a <+32>:	lea    rax,[rbp-0x10]
   0x000000000040059e <+36>:	mov    rsi,rax
   0x00000000004005a1 <+39>:	lea    rdi,[rip+0xc7]        # 0x40066f
   0x00000000004005a8 <+46>:	mov    eax,0x0
   0x00000000004005ad <+51>:	call   0x400470 <__isoc99_scanf@plt>
   0x00000000004005b2 <+56>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004005b5 <+59>:	mov    rdx,QWORD PTR [rbp-0x10]
   0x00000000004005b9 <+63>:	cdqe
   0x00000000004005bb <+65>:	lea    rcx,[rax*8+0x0]
   0x00000000004005c3 <+73>:	lea    rax,[rip+0x200476]        # 0x600a40 <target>
   0x00000000004005ca <+80>:	mov    QWORD PTR [rcx+rax*1],rdx
   0x00000000004005ce <+84>:	lea    rdi,[rip+0x9e]        # 0x400673
   0x00000000004005d5 <+91>:	call   0x400450 <puts@plt>
   0x00000000004005da <+96>:	nop
   0x00000000004005db <+97>:	leave
   0x00000000004005dc <+98>:	ret

   rax = first
   rdx = second

   rcx = first * 8
   rax = ?

   [rcx + rax] = rdx

   offset = 0x600a40

   [0x6009e8] puts@GLIBC_2.2.5 -> 0x400456 (puts@plt+6) ◂— push   0 /* 'h' */
   [0x6009f0] system@GLIBC_2.2.5 -> 0x400466 (system@plt+6) ◂— push   1
   0x400567: win
   4195687

   distance = 0x50 (80)
   first = -11
   second = 0x6009f0 (6294000)
