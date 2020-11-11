def inc(c, d):
    return chr(ord(c) + d)

def dec(c, d):
    return chr(ord(c) - d)

arg1 = ["+"] * 29

arg1[0x13] = '6'
arg1[0x10] = 'n'
arg1[0xd] = 'r'
arg1[0x14] = dec('%', -8)
arg1[0xf] = 'n'
arg1[10] = 'p'
arg1[0x10] = dec('u', 7)
arg1[3] = '{'
arg1[0x13] = '6'
arg1[0x15] = 'q'
arg1[2] = 'n'
arg1[0] = 's'
arg1[7] = 'l'
arg1[0xe] = 'u'
arg1[0xc] = dec(',', -1)
arg1[4] = 'b'
arg1[6] = dec('o', 3)
arg1[0x12] = 'n'
arg1[0x16] = dec('z', 5)
arg1[0x17] = '1'
arg1[1] = 'u'
arg1[5] = dec('8', 5)
arg1[8] = dec('f', 3 + 4 - 9)
arg1[0xb] = dec('<', 7)
arg1[0x11] = dec('-', 6 - 8 + ord('\t') - 5 - 6)
arg1[9] = dec(',', 1 + 2 - 7)
arg1[0x18] = dec('Y', -10 - 8 + ord('\b'))
arg1[0x19] = dec('w', 5 + ord('\a'))
arg1[0x1a] = dec('m', -6 + ord('\a'))
arg1[0x1b] = 'y'
arg1[0x1c] = '}'

for i, c in enumerate(arg1):
    print(i, c)

print()

key = "".join(arg1)
print(key)

with open('key.txt', 'w') as f:
    f.write(key)
