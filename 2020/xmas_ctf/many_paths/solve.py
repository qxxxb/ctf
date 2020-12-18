import pwn
import numpy as np
# from numpy.linalg import matrix_power
import ast
import mp

# nc challs.xmas.htsp.ro 6053
io = pwn.remote('challs.xmas.htsp.ro', 6053)
pwn.context.log_level = 'debug'

for i in range(5):
    io.recvline()


def get_n():
    s = io.recvlineS()
    print(s)
    s = s.split(' = ')
    return int(s[1])


def get_matrix():
    io.recvline()
    s = io.recvuntilS('forbidden nodes: ', drop=True)
    s = s.split()
    for i, x in enumerate(s[:-1]):
        s[i] += ';'
    s = '\n'.join(s)
    return np.matrix(s)


def get_forbidden_nodes():
    s = io.recvuntilS(']\n')
    return ast.literal_eval(s)


def get_length():
    s = io.recvlineS()
    s = s.split(' = ')
    return int(s[1])


def solve(A, length):
    B = mp.matrix_power_mod(A, length, 666013)
    # TODO: modulo during power?
    ans = B[0, len(A) - 1]
    ans = ans % 666013
    return ans


for i in range(40):
    io.recvline()
    n = get_n()
    A = get_matrix()
    forbidden = get_forbidden_nodes()
    length = get_length()

    # Indexing should start from 0
    forbidden = [x - 1 for x in forbidden]

    for x in forbidden:
        A[x] = 0
        A[:, x] = 0

    ans = solve(A, length)
    io.sendline(str(ans))
    io.recvline()
    io.recvline()

io.interactive()
