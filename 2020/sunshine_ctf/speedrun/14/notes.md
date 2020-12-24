pwndbg> p &__stack_prot
$2 = (<data variable, no debug info> *) 0x6b8ef0 <__stack_prot>

Gadgets

0x0000000000410263: pop rsi; ret;
0x00000000004158f4: pop rax; ret;
0x000000000047f401: mov qword ptr [rsi], rax; ret;
0x0000000000400696: pop rdi; ret;
0x000000000044c0a9: pop rdx; pop rsi; ret;

pwndbg> p &__data_start 
$1 = (<data variable, no debug info> *) 0x6b90e0
