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
    license = 0  # &license[0]
    email = 30  # &email[0]
    email_tail = 30 + 28  # &email[28]

    email_i = email
    license_i = 0
    while True:
        # 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, ...
        RV = license + (license_i & 0b11)

        # email[0], email[1], email[2], ... , email[28]
        email = stack[email_i]
        stack[RV] = (stack[RV] + email) & 0xff

        email_i += 1
        license_i += 1
        if email_i > email_tail:
            break


def measure(stack):
    ans = [0] * 8
    for i in range(0, 8):
        ans[i] = stack[i] - 0
    return ans


def split_diffs(diffs):
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


def apply_fixes(email, fixes):
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

with open('stack', 'r') as f:
    s = f.read()
    stack = parse_hexdump(s)
    hexdump(stack, addr=0xfac4)
    scramble(stack)
    print()
    hexdump(stack, addr=0xfac4)
    print()
    diffs = measure(stack)
    print(diffs)
    fixes = split_diffs(diffs)
    print(fixes)
    apply_fixes(email, fixes)
    print()
    print("New email:")
    hexdump(email)
