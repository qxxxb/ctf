from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30009)
# sh = process('./chall_09')

key = [0x79, 0x17, 0x46, 0x55, 0x10, 0x53, 0x5f, 0x5d, 0x55, 0x10, 0x58, 0x55, 0x42, 0x55, 0x10, 0x44, 0x5f, 0x3a]
text = [chr(k ^ 0x30) for k in key]
print(text)

payload = "".join(text)
print(payload) # I've come here to

sh.sendline(payload)
sh.interactive()
