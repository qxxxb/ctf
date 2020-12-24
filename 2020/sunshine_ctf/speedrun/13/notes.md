 ► 0x8048528 <vuln+39>    ret    <0x61716161>

 Dump of assembler code for function systemFunc:
    0x080484d6 <+0>:	push   ebp
    0x080484d7 <+1>:	mov    ebp,esp
    0x080484d9 <+3>:	push   ebx
    0x080484da <+4>:	sub    esp,0x4
    0x080484dd <+7>:	call   0x8048582 <__x86.get_pc_thunk.ax>
    0x080484e2 <+12>:	add    eax,0x1b1e
    0x080484e7 <+17>:	sub    esp,0xc
    0x080484ea <+20>:	lea    edx,[eax-0x19f0]
    0x080484f0 <+26>:	push   edx
    0x080484f1 <+27>:	mov    ebx,eax
    0x080484f3 <+29>:	call   0x8048390 <system@plt>
    0x080484f8 <+34>:	add    esp,0x10
    0x080484fb <+37>:	nop
    0x080484fc <+38>:	mov    ebx,DWORD PTR [ebp-0x4]
    0x080484ff <+41>:	leave  
    0x08048500 <+42>:	ret    
