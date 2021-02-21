# antistatic

**Category**: Reversing \
**Tags**: `crackme`, `babyrev` \
**Points**: 100 (51 solves) \
**Author**: Retr0id

## Challenge

Heisenberg's uncertainty principle also applies to CTF. Please do not observe my crackme, otherwise you may change its behavior!

Author: Retr0id \
Attachments: `antistatic`

## Solution

Open in Ghidra and decompile. `main` does basically nothing but
`__libc_gnu_init` looks interesting. A lot of weird antidebugging stuff going
on that I just NOP'd out.

After cleaning up the decompiled C it's a lot easier to see what's going on:

```python
import pwn

elf = pwn.ELF("antistatic")
gnu_hash = elf.read(elf.sym["gnu_hash"], 50)

for j in range(0x13):
    for c in range(256):
        if (c ^ 0x42 + j) & 0xff == gnu_hash[j]:
            print(chr(c), end="")

print()
# union{ct0rs_b3war3}
```
