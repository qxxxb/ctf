from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30016)
# sh = process('./chall_16')

def fuck(x):
    x = ord(x)
    for i in range(0x30, 0x94):
        x = x ^ i
    return chr(x)

key = 'Queue epic guitar solo *syn starts shredding*\n'
payload = [fuck(k) for k in key]
payload = "".join(payload)
print(payload)

sh.sendline(payload)
sh.interactive()

# payload = 'A' * 45

# with open('payload', 'w') as f:
#     f.write(payload + "\n")

# 0x555555755020

# sh.sendline(payload)
# sh.interactive()

# ► 0x400b9c <main+63>    ret    <0x6261616362616162>
