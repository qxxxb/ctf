import pwn

io = pwn.ssh(
    host='pwnable.kr',
    port=2222,
    user='random',
    password='guest'
)

# e_file = io.download_file('random')

for i in range(2 ** 32):
    sh = pwn.process('./random')
    # sh = io.run('./random')
    sh.sendline(str(i))
    response = sh.recvall().decode(errors='replace')
    print(response)
    if response[:5] != "Wrong":
        break
