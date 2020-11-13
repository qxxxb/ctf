import pwn
import sys


def parse_hexdump(hexdump):
    ans = bytearray()
    for line in hexdump.splitlines():
        tokens = line.split()
        tokens = tokens[1:-1]  # Discard first and last
        for token in tokens:
            # Iterate each token two chars at a time
            for i in range(0, len(token), 2):
                byte_str = token[i: i + 2]
                byte = int(byte_str, 16)
                ans.append(byte)
    return ans


def hexdump(stack, addr=0x0, addr_max_width=4):
    # Print 16 bytes per row
    for i in range(0, len(stack), 16):
        sub = stack[i: i + 16]

        pair_strs = []

        # Read 2 bytes at time
        for j in range(0, len(sub), 2):
            pair = sub[j: j + 2]
            pair_strs.append(pair.hex())

        s = " ".join(pair_strs)

        # Insert spaces every 4 characters
        addr_str = "{:x}".format(addr).rjust(addr_max_width, '0')
        print('{}: {}'.format(addr_str, s))
        addr += 16


def scramble(stack):
    license = 0  # R3 = &license[0]
    email = 30  # R4 = &email[0]
    email_tail = 30 + 28  # R6 = &email[28]

    email_i = email  # R5
    license_i = 0  # R7
    while True:
        # license_i: 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, ...
        RV = license + (license_i & 0b111)

        # email[0], email[1], email[2], ... , email[28]
        email = stack[email_i]
        stack[RV] = (stack[RV] + email) & 0xff

        email_i += 1
        license_i += 1
        if email_i > email_tail:
            break


def measure_diffs(stack):
    # Measure the differences required to make the first 8 bytes of the license
    # key zero
    ans = [0] * 8
    for i in range(0, 8):
        ans[i] = 0x100 - stack[i]
    return ans


def split_diffs(diffs):
    # Split the differences that exceed the size of one byte
    ans = []
    for i, diff in enumerate(diffs):
        fixes = []
        max_inc = 0xff - 0x80
        while (diff + 0x80) > 0xff:
            diff -= max_inc
            fixes.append(max_inc)
        fixes.append(diff)
        ans.append(fixes)

    return ans


def apply_diffs(email, fixes):
    # Apply the differences among the email bytes
    for i, fix in enumerate(fixes):
        for j, inc in enumerate(fix):
            email[i + (j * 8)] += inc


license = ([b'k'] + [b'A']) * 15
email = bytearray(30)
email[-1] = ord('\n')
email[-2] = ord('r')
email[-3] = 0xe1
email[-4] = 0xe5
email[-5] = 0xae
email[-6] = 0xe7
email[-7] = 0xe5
email[-8] = 0xf0
email[-9] = 0xc0

with open('dump', 'r') as f:
    s = f.read()
    stack = parse_hexdump(s)

    scramble(stack)
    print('Hexdump post-scramble:')
    hexdump(stack, addr=0xfac4)
    print()

    diffs = measure_diffs(stack)
    diffs = split_diffs(diffs)
    apply_diffs(email, diffs)

    print("New email:")
    hexdump(email)
    print()

if len(sys.argv) > 1:
    # Only do the IO stuff if we run with args (doesn't matter what).
    # This is so we can test the functions above without intializing pwntools
    # every time.

    if sys.argv[1] == 'r':
        # Run on remote
        p = pwn.remote('chal.2020.sunshinectf.org', port=10001)
    else:
        # Debug local process
        p = pwn.process(
            './runpeg -p peg_rev_checker.so LicenseChecker.peg -d',
            shell=True
        )

        p.recvuntil('EAR debugger')
        p.sendline('')
        p.recvuntil('(dbg) ')

        p.sendline('b 0x01E8')
        p.sendline('c')

    p.recvuntil('Email: ')
    p.send(email)

    p.recvuntil('License key: ')
    license = b''.join(license)
    p.send(license)

    if sys.argv[1] == 'r':
        print(p.recvall(timeout=2).decode())
    else:
        p.interactive()
