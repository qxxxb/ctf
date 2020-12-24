first fgets:
s: rsp (rbp - 240)
n: 19

second fgets:
s: rbp - 0xd0 (rbp - 208)
n: 200

pwndbg> disassemble main
Dump of assembler code for function main:
   0x000055555555473a <+0>:	push   rbp
   0x000055555555473b <+1>:	mov    rbp,rsp
   0x000055555555473e <+4>:	sub    rsp,0xf0
   0x0000555555554745 <+11>:	mov    rax,QWORD PTR fs:0x28
   0x000055555555474e <+20>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000555555554752 <+24>:	xor    eax,eax
   0x0000555555554754 <+26>:	lea    rdi,[rip+0xe9]        # 0x555555554844
   0x000055555555475b <+33>:	mov    eax,0x0
   0x0000555555554760 <+38>:	call   0x555555554600 <printf@plt>
   0x0000555555554765 <+43>:	mov    rdx,QWORD PTR [rip+0x2008a4]        # 0x555555755010 <stdin@@GLIBC_2.2.5>
   0x000055555555476c <+50>:	lea    rax,[rbp-0xf0]
   0x0000555555554773 <+57>:	mov    esi,0x13
   0x0000555555554778 <+62>:	mov    rdi,rax
   0x000055555555477b <+65>:	call   0x555555554610 <fgets@plt>
   0x0000555555554780 <+70>:	mov    rdx,QWORD PTR [rip+0x200889]        # 0x555555755010 <stdin@@GLIBC_2.2.5>
   0x0000555555554787 <+77>:	lea    rax,[rbp-0xd0]
   0x000055555555478e <+84>:	mov    esi,0xc8
   0x0000555555554793 <+89>:	mov    rdi,rax
   0x0000555555554796 <+92>:	call   0x555555554610 <fgets@plt>
   0x000055555555479b <+97>:	lea    rdx,[rbp-0xd0]
   0x00005555555547a2 <+104>:	mov    eax,0x0
=> 0x00005555555547a7 <+109>:	call   rdx
   0x00005555555547a9 <+111>:	nop
   0x00005555555547aa <+112>:	mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555547ae <+116>:	xor    rax,QWORD PTR fs:0x28
   0x00005555555547b7 <+125>:	je     0x5555555547be <main+132>
   0x00005555555547b9 <+127>:	call   0x5555555545f0 <__stack_chk_fail@plt>
   0x00005555555547be <+132>:	leave
   0x00005555555547bf <+133>:	ret
