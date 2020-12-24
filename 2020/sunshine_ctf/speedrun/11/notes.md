pwndbg> p $ebp
$4 = (void *) 0xffffc638
pwndbg> stack 120
00:0000│ esp  0xffffc550 —▸ 0xffffc568 ◂— 0x0
01:0004│      0xffffc554 ◂— 0xc7
02:0008│      0xffffc558 —▸ 0xf7fb0580 (_IO_2_1_stdin_) ◂— 0xfbad2288
03:000c│      0xffffc55c —▸ 0x8048520 (vuln+15) ◂— add    ebx, 0x13e8
04:0010│      0xffffc560 ◂— 0x0
05:0014│      0xffffc564 ◂— 0x11
06:0018│ eax  0xffffc568 ◂— 0x0
07:001c│      0xffffc56c —▸ 0xf7e3a7fe (_IO_getline_info+126) ◂— add    dword ptr [esp + 0x14], esi
08:0020│      0xffffc570 —▸ 0xffffc64d ◂— 'aaabaaacaaadaaaea'
09:0024│      0xffffc574 —▸ 0x804a5b1 ◂— 'aaabaaacaaadaaaea\n'
0a:0028│      0xffffc578 ◂— 0x11
0b:002c│      0xffffc57c —▸ 0xf7dd5e40 ◂— 0x5174 /* 'tQ' */
0c:0030│      0xffffc580 —▸ 0xf7fcb110 —▸ 0xf7dcb000 ◂— 0x464c457f
0d:0034│      0xffffc584 —▸ 0xffffc65e ◂— 0xc6800800
0e:0038│      0xffffc588 —▸ 0xf7fb0000 ◂— 0x1e4d6c
0f:003c│      0xffffc58c —▸ 0xf7fb0f20 ◂— 0x0
10:0040│      0xffffc590 —▸ 0xffffc644 ◂— 0xffffffff
11:0044│      0xffffc594 —▸ 0xf7fcb3e0 —▸ 0xf7ffd980 ◂— 0x0
12:0048│      0xffffc598 —▸ 0xf7e4853b (_IO_default_xsputn+11) ◂— add    ebx, 0x167ac5
13:004c│      0xffffc59c ◂— 0x0
14:0050│      0xffffc5a0 —▸ 0xf7fb0580 (_IO_2_1_stdin_) ◂— 0xfbad2288
15:0054│      0xffffc5a4 ◂— 0x12
16:0058│      0xffffc5a8 —▸ 0xffffc628 —▸ 0xffffc668 ◂— 0x0
17:005c│      0xffffc5ac —▸ 0xf7e3a95e (_IO_getline+30) ◂— add    esp, 0x2c
18:0060│      0xffffc5b0 —▸ 0xf7fb0580 (_IO_2_1_stdin_) ◂— 0xfbad2288
19:0064│      0xffffc5b4 —▸ 0xffffc64c ◂— 'aaaabaaacaaadaaaea'
1a:0068│      0xffffc5b8 ◂— 0x12
1b:006c│      0xffffc5bc ◂— 0xa /* '\n' */
1c:0070│      0xffffc5c0 ◂— 0x1
1d:0074│      0xffffc5c4 ◂— 0x0
1e:0078│      0xffffc5c8 —▸ 0xf7fcb410 —▸ 0x804829e ◂— inc    edi /* 'GLIBC_2.0' */
1f:007c│      0xffffc5cc ◂— 0x1
... ↓
21:0084│      0xffffc5d4 ◂— 0x0
22:0088│      0xffffc5d8 —▸ 0xf7e47f69 (__overflow+9) ◂— add    ebx, 0x168097
23:008c│      0xffffc5dc —▸ 0xf7e396fa (fgets+138) ◂— mov    edx, dword ptr [esi]
24:0090│      0xffffc5e0 —▸ 0xf7fb0580 (_IO_2_1_stdin_) ◂— 0xfbad2288
25:0094│      0xffffc5e4 —▸ 0xffffc64c ◂— 'aaaabaaacaaadaaaea'
26:0098│      0xffffc5e8 ◂— 0x12
27:009c│      0xffffc5ec ◂— 0xa /* '\n' */
28:00a0│      0xffffc5f0 ◂— 0x1
29:00a4│      0xffffc5f4 —▸ 0xf7dd5e40 ◂— 0x5174 /* 'tQ' */
2a:00a8│      0xffffc5f8 ◂— 0xa /* '\n' */
... ↓
2c:00b0│      0xffffc600 —▸ 0xf7fe3539 ◂— add    ebx, 0x19ac7
2d:00b4│      0xffffc604 —▸ 0x8049908 (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049818 (_DYNAMIC) ◂— 0x1
2e:00b8│      0xffffc608 —▸ 0xf7fb0000 ◂— 0x1e4d6c
... ↓
30:00c0│      0xffffc610 —▸ 0xffffc668 ◂— 0x0
31:00c4│      0xffffc614 —▸ 0xf7fe9740 ◂— pop    edx
32:00c8│      0xffffc618 ◂— 0xffffffff
33:00cc│      0xffffc61c —▸ 0x8049908 (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049818 (_DYNAMIC) ◂— 0x1
34:00d0│      0xffffc620 —▸ 0xf7fb0000 ◂— 0x1e4d6c
... ↓
36:00d8│      0xffffc628 —▸ 0xffffc668 ◂— 0x0
37:00dc│      0xffffc62c —▸ 0x80485b8 (main+70) ◂— add    esp, 0x10
38:00e0│      0xffffc630 —▸ 0xffffc64c ◂— 'aaaabaaacaaadaaaea'
39:00e4│      0xffffc634 —▸ 0x8049908 (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049818 (_DYNAMIC) ◂— 0x1
3a:00e8│ ebp  0xffffc638 —▸ 0xffffc668 ◂— 0x0
3b:00ec│      0xffffc63c —▸ 0x80485c0 (main+78) ◂— nop

pwndbg> disassemble vuln
Dump of assembler code for function vuln:
   0x08048511 <+0>:	push   ebp
   0x08048512 <+1>:	mov    ebp,esp
   0x08048514 <+3>:	push   ebx
   0x08048515 <+4>:	sub    esp,0xd4
   0x0804851b <+10>:	call   0x8048420 <__x86.get_pc_thunk.bx>
   0x08048520 <+15>:	add    ebx,0x13e8
   0x08048526 <+21>:	mov    eax,DWORD PTR [ebx-0x4]
   0x0804852c <+27>:	mov    eax,DWORD PTR [eax]
   0x0804852e <+29>:	sub    esp,0x4
   0x08048531 <+32>:	push   eax
   0x08048532 <+33>:	push   0xc7
   0x08048537 <+38>:	lea    eax,[ebp-0xd0]
   0x0804853d <+44>:	push   eax
   0x0804853e <+45>:	call   0x8048380 <fgets@plt>
   0x08048543 <+50>:	add    esp,0x10
   0x08048546 <+53>:	sub    esp,0xc
   0x08048549 <+56>:	lea    eax,[ebp-0xd0]
   0x0804854f <+62>:	push   eax
   0x08048550 <+63>:	call   0x8048360 <printf@plt>
   0x08048555 <+68>:	add    esp,0x10
   0x08048558 <+71>:	mov    eax,DWORD PTR [ebx-0x4]
   0x0804855e <+77>:	mov    eax,DWORD PTR [eax]
   0x08048560 <+79>:	sub    esp,0xc
   0x08048563 <+82>:	push   eax
   0x08048564 <+83>:	call   0x8048370 <fflush@plt>
   0x08048569 <+88>:	add    esp,0x10
   0x0804856c <+91>:	nop
   0x0804856d <+92>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x08048570 <+95>:	leave
=> 0x08048571 <+96>:	ret

pwndbg> plt
0x8048360: printf@plt
0x8048370: fflush@plt
0x8048380: fgets@plt
0x8048390: puts@plt
0x80483a0: system@plt
0x80483b0: __libc_start_main@plt
pwndbg> got

GOT protection: No RELRO | GOT functions: 6

[0x8049914] printf@GLIBC_2.0 -> 0xf7e1f050 (printf) ◂— call   0xf7f0d399
[0x8049918] fflush@GLIBC_2.0 -> 0x8048376 (fflush@plt+6) ◂— push   8
[0x804991c] fgets@GLIBC_2.0 -> 0xf7e39670 (fgets) ◂— call   0xf7f0d399
[0x8049920] puts@GLIBC_2.0 -> 0xf7e3b450 (puts) ◂— push   ebp
[0x8049924] system@GLIBC_2.0 -> 0x80483a6 (system@plt+6) ◂— push   0x20 /* 'h ' */
[0x8049928] __libc_start_main@GLIBC_2.0 -> 0xf7de9cf0 (__libc_start_main) ◂— call   0xf7f0d399

pwndbg> p win
$7 = {<text variable, no debug info>} 0x80484e6 <win>
