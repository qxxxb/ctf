from pwn import *
import subprocess

sh = remote('chal.2020.sunshinectf.org', 30017)
# sh = process('./chall_17')

sub_ans = subprocess.check_output('./a.out')
p = sub_ans.decode().strip()
print(p)

sh.sendline(p)
print(sh.recvall())
