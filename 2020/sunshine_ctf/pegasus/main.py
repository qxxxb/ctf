def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def pack(n):
    s = format(n % (1 << 16), '016b')
    return int(s, 2)


def unpack(n):
    twos_comp(n, 16)


def check_license_key(key, r3):
    key = [k | 0x80 for k in key]

    rv = 0
    r4 = 0

    while r3 != 0:
        print(key)
        r3 -= 1

        r5 = key[rv] + 0x80
        rv += 1

        r5 = r5 - 235
        if r5 > 0xf:
            print("r5")
            return False

        r6 = key[rv] + 0x80
        rv += 1

        r6 = r6 & 0x7f  # Take the first 7 bits
        r6 = r6 - 0x41
        if r6 > 0xf:
            print("r6")
            return False

        r6 = r6 << 4
        r5 = r5 | r6

        key[r4] = r5
        r4 += 1

    return True


def check_email(email):
    rv = 0
    r4 = 0
    r5 = 0

    # r5 = end of buf
    while email[r5] != 0:
        r5 += 1

    r6 = r5
    rv = r5 - r4  # distance between end of buf and beginning (29)

    if rv < 0xA:
        return 1

    rv = email[r5]  # rv = last char (zero)
    r5 -= 1

    print(rv)
    rv = rv - 0x72  # wait a second. won't this always be zero?
    if rv != 0:
        return 1

    rv = email[r5]  # rv = next char from end
    r5 -= 1

    rv = rv ^ 0xe1
    if rv != 0:
        return 1

    r5 = r4
    r7 = 0
    while True:
        rv = r7 + 0x7
        r4 = email[r5]
        tmp = email[rv]
        tmp = tmp + r4
        email[rv] = tmp
        r5 += 1
        r7 += 1
        if r5 <= r6:
            break


email = [0xfa] * 29 + [0]
print(check_email(email))


# def rev_even_lk():
#     for c in range(0x0, 0xff + 1):
#         cm = c | 0x80
#         r5 = cm - 0xeb
#         print(c, r5)
#         if r5 <= 0xf:
#             return r5


# r5 = rev_even_lk()
# print(r5)

# def gen_license_key():
#     r5 = 0 + 235 - 0x80
#     r6 = 0xc1  # first_byte(0x41 - 0x80)
#     return ([r5] + [r6]) * 15


# license_key = gen_license_key()
# checked_license_key = license_key.copy()
# print(check_license_key(checked_license_key, 8))
# print(license_key)
