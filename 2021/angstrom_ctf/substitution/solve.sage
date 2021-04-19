from functools import reduce
import pwn

p = 691

def substitute(value):
    return (reduce(lambda x, y: x * value + y, key)) % p


def crack(zs):
    n = len(zs)

    M = MatrixSpace(GF(p), n, n)
    V = VectorSpace(GF(p), n)

    A = M(lambda i, j: pow(i, n - j - 1, p))
    Y = V(zs)

    X = A \ Y
    print(bytes(X))


def grab_subs(io):
    zs = []
    for i in range(100):
        io.sendlineafter("> ", str(i))
        z = io.recvlineS().strip().split()[-1]
        z = int(z)
        print(z, end=" ", flush=True)
        zs.append(z)
    print()
    return zs


# io = pwn.remote("crypto.2021.chall.actf.co", 21601)
# zs = grab_subs(io)
# print(f"[+] Got subs: {zs}")

zs = [125, 492, 670, 39, 244, 257, 104, 615, 129, 520, 428, 599, 404, 468, 465, 523, 345, 44, 425, 515, 116, 120, 515, 283, 651, 199, 69, 388, 319, 410, 133, 267, 215, 352, 521, 270, 629, 564, 662, 640, 352, 351, 481, 103, 161, 106, 306, 360, 587, 318, 450, 314, 164, 185, 519, 85, 472, 343, 41, 652, 320, 581, 400, 259, 119, 525, 374, 434, 162, 661, 145, 360, 209, 302, 426, 285, 358, 610, 572, 366, 434, 627, 206, 427, 166, 527, 590, 189, 462, 148, 428, 140, 306, 163, 265, 249, 522, 66, 136, 332]

for i in range(4, 100):
    try:
        crack(zs[:i])
    except Exception as e:
        pass
