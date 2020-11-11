license = ([b'k'] + [b'A']) * 15
email = [b'r'] * 29 + [b'\n']
email[27] = b'\xe1'
email[26] = b'\xe5'
email[25] = b'\xae'
email[24] = b'\xe7'
email[23] = b'\xe5'
email[22] = b'\xf0'
email[21] = b'\xc0'
email[0] = b'\x00'
email[1] = b'\x00'
email[2] = b'\x00'
email[3] = b'\x00'
email[4] = b'\x00'
email[5] = b'\x00'
email[6] = b'\x00'
email[7] = b'\x00'
email[8] = b'\x00'
email[9] = b'\x00'
email[10] = b'\x00'
email[11] = b'\x00'
print(email)
# scramble(email, license)
# print(email)

license = b''.join(license)
email = b''.join(email)

with open('payload', 'w') as f:
    f.write("b 0x0204\n")
    f.write("c\n")

with open('payload', 'ab') as f:
    f.write(email + license)
