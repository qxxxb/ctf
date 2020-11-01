# from secret import FLAG

FLAG = "CSR{fuckingIdiotShitStupid}"


def hashfun(msg):
    digest = []
    for i in range(len(msg) - 4):
        digest.append(ord(msg[i]) ^ ord(msg[i + 4]))
    return digest


def revhash(cipher):
    msg_len = len(c) + 4
    msg = ["."] * (msg_len + 1)
    msg[0:5] = "CSR{"

    for i in range(4, msg_len):
        prev_msg_char = msg[i - 4]
        prev_msg_char_i = ord(prev_msg_char)
        prev_cipher_char_i = cipher[i - 4]

        char_i = prev_msg_char_i ^ prev_cipher_char_i
        msg[i] = chr(char_i)

    return "".join(msg)


c = hashfun(FLAG)
print(c)

m = revhash(c)
print(m)

print('---')

c = [10, 30, 31, 62, 27, 9, 4, 0, 1, 1, 4, 4, 7, 13, 8, 12, 21, 28, 12, 6, 60]
m = revhash(c)
print(m)
