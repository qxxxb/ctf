# flag

```bash
 file flag
flag_orig: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped

 binwalk flag

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF, 64-bit LSB executable, AMD x86-64, version 1 (GNU/Linux)
216           0xD8            ELF, 64-bit LSB processor-specific, (GNU/Linux)
304819        0x4A6B3         Copyright string: "Copyright (C) 1996-2011 the UPX Team. All Rights Reserved. $"

 strings flag_orig | grep upx
$Info: This file is packed with the UPX executable packer http://upx.sf.net $

 sudo apt-get install upx-ucl

 upx -d flag
```

Run `aa` in radare2 to perform analysis. Then do:
```
[0x00401164]> s main
[0x00401164]> pdf
            ; DATA XREF from entry0 @ 0x401075
┌ 61: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_8h @ rbp-0x8
│           0x00401164      55             push rbp
│           0x00401165      4889e5         mov rbp, rsp
│           0x00401168      4883ec10       sub rsp, 0x10
│           0x0040116c      bf58664900     mov edi, str.I_will_malloc___and_strcpy_the_flag_there._take_it. ; 0x496658 ; "I will malloc() and strcpy the flag there. take it."
│           0x00401171      e80a0f0000     call sym.puts               ; int puts(const char *s)
│           0x00401176      bf64000000     mov edi, 0x64               ; 'd' ; 100
│           0x0040117b      e850880000     call sym.malloc             ;  void *malloc(size_t size)
│           0x00401180      488945f8       mov qword [var_8h], rax
│           0x00401184      488b15e50e2c.  mov rdx, qword [obj.flag]   ; [0x6c2070:8]=0x496628 str.UPX...__sounds_like_a_delivery_service_: ; "(fI"
│           0x0040118b      488b45f8       mov rax, qword [var_8h]
│           0x0040118f      4889d6         mov rsi, rdx
│           0x00401192      4889c7         mov rdi, rax
│           0x00401195      e886f1ffff     call fcn.00400320
│           0x0040119a      b800000000     mov eax, 0
│           0x0040119f      c9             leave
└           0x004011a0      c3             ret
[0x00401164]> pf S @obj.flag
0x006c2070 = 0x006c2070 -> 0x00496628 "UPX...? sounds like a delivery service :)"
```

We can pretty much already see the flag where it's value is moved to `rdx` at
instruction `0x00401184`. Just to make sure, let's run it in GDB.

```
pwndbg> b *0x00401184
pwndbg> ni
pwndbg> reg rdx
*RDX  0x496628 ◂— push   rbp /* 'UPX...? sounds like a delivery service :)' */
```

The flag is `UPX...? sounds like a delivery service :)`.
