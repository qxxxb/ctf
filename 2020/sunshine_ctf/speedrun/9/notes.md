key length: 18
AAAAAAAAAAAAAAAAA

fgets:
s = rbp-0x50
n = 0x31

IAAAAAAAAAAAAAAAA
IAAA9999AAAAAAAAA
0ZZZ

x = rbp-0x54

first_char ^ 0x30 == 121
first_char = 73

pwndbg> telescope $rdi
00:0000│ rdx rdi  0x555555755020 (key) ◂— 0x5d5f531055461779
01:0008│          0x555555755028 (key+8) ◂— 0x4410554255581055
02:0010│          0x555555755030 (key+16) ◂— 0x3a5f /* '_:' */
03:0018│          0x555555755038 (key+24) ◂— 0x0

pwndbg> hex $rdi
+0000 0x555555755020  79 17 46 55  10 53 5f 5d  55 10 58 55  42 55 10 44  │y.FU│.S_]│U.XU│BU.D│
+0010 0x555555755030  5f 3a 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │_:..│....│....│....│
+0020 0x555555755040  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │....│....│....│....│

pwndbg> disassemble main
Dump of assembler code for function main:
   0x00005555555547dd <+0>:	push   rbp
   0x00005555555547de <+1>:	mov    rbp,rsp
   0x00005555555547e1 <+4>:	push   rbx
   0x00005555555547e2 <+5>:	sub    rsp,0x58
   0x00005555555547e6 <+9>:	mov    rax,QWORD PTR fs:0x28
   0x00005555555547ef <+18>:	mov    QWORD PTR [rbp-0x18],rax
   0x00005555555547f3 <+22>:	xor    eax,eax
   0x00005555555547f5 <+24>:	mov    rdx,QWORD PTR [rip+0x200864]        # 0x555555755060 <stdin@@GLIBC_2.2.5>
   0x00005555555547fc <+31>:	lea    rax,[rbp-0x50]
   0x0000555555554800 <+35>:	mov    esi,0x31
   0x0000555555554805 <+40>:	mov    rdi,rax
   0x0000555555554808 <+43>:	call   0x555555554690 <fgets@plt>
   0x000055555555480d <+48>:	lea    rax,[rbp-0x50]
   0x0000555555554811 <+52>:	mov    rdi,rax
   0x0000555555554814 <+55>:	call   0x555555554660 <strlen@plt>
   0x0000555555554819 <+60>:	mov    rbx,rax
   0x000055555555481c <+63>:	lea    rdi,[rip+0x2007fd]        # 0x555555755020 <key>
=> 0x0000555555554823 <+70>:	call   0x555555554660 <strlen@plt>
   0x0000555555554828 <+75>:	cmp    rbx,rax
   0x000055555555482b <+78>:	jne    0x55555555488b <main+174>
   0x000055555555482d <+80>:	mov    DWORD PTR [rbp-0x54],0x0
   0x0000555555554834 <+87>:	jmp    0x555555554868 <main+139>
   0x0000555555554836 <+89>:	mov    eax,DWORD PTR [rbp-0x54]
   0x0000555555554839 <+92>:	cdqe
   0x000055555555483b <+94>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
   0x0000555555554840 <+99>:	xor    eax,0x30
   0x0000555555554843 <+102>:	mov    ecx,eax
   0x0000555555554845 <+104>:	mov    eax,DWORD PTR [rbp-0x54]
   0x0000555555554848 <+107>:	movsxd rdx,eax
   0x000055555555484b <+110>:	lea    rax,[rip+0x2007ce]        # 0x555555755020 <key>
   0x0000555555554852 <+117>:	movzx  eax,BYTE PTR [rdx+rax*1]
   0x0000555555554856 <+121>:	cmp    cl,al
   0x0000555555554858 <+123>:	je     0x555555554864 <main+135>
   0x000055555555485a <+125>:	mov    edi,0x0
   0x000055555555485f <+130>:	call   0x5555555546a0 <exit@plt>
   0x0000555555554864 <+135>:	add    DWORD PTR [rbp-0x54],0x1
   0x0000555555554868 <+139>:	mov    eax,DWORD PTR [rbp-0x54]
   0x000055555555486b <+142>:	movsxd rbx,eax
   0x000055555555486e <+145>:	lea    rdi,[rip+0x2007ab]        # 0x555555755020 <key>
   0x0000555555554875 <+152>:	call   0x555555554660 <strlen@plt>
   0x000055555555487a <+157>:	cmp    rbx,rax
   0x000055555555487d <+160>:	jb     0x555555554836 <main+89>
   0x000055555555487f <+162>:	lea    rdi,[rip+0xae]        # 0x555555554934
   0x0000555555554886 <+169>:	call   0x555555554680 <system@plt>
   0x000055555555488b <+174>:	nop
   0x000055555555488c <+175>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000555555554890 <+179>:	xor    rax,QWORD PTR fs:0x28
   0x0000555555554899 <+188>:	je     0x5555555548a0 <main+195>
   0x000055555555489b <+190>:	call   0x555555554670 <__stack_chk_fail@plt>
   0x00005555555548a0 <+195>:	add    rsp,0x58
   0x00005555555548a4 <+199>:	pop    rbx
   0x00005555555548a5 <+200>:	pop    rbp
   0x00005555555548a6 <+201>:	ret
