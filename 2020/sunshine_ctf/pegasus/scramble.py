stack = [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\xc1', b'\xeb', b'\x00', b'\x00', b'\x00', b'\x00', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\xf2', b'\x72', b'\x00']
print(stack)

rv = 30  # &email[0]
r3 = 0  # &license[0]

r4 = rv
r5 = rv

# ...

r6 = 58

r5 = r4
r7 = 0
while True:
    rv = r3 + 0x7 + r7
    r4 = stack[r5]
    tmp = stack[rv]
    tmp = bytes([tmp[0] & r4[0]])
    stack[rv] = tmp
    r5 += 1
    r7 += 1
    if r5 <= r6:
        break

rv = 0
r7 = 0

print(stack)

while True:
    r5 = r3 + r7
    r5 = stack[r5]
    # print(stack[r5])
    print(rv)
    r7 += 1
    if r7 >= 0x7:
        break

print(rv)
