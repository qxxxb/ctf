from itertools import product
from math import ceil, log
import challenge as chal
import pprint
import sys
import pwn
import time

use_import = False
remote = False

if len(sys.argv) >= 2:
    use_import = 'i' in sys.argv[1]
    remote = 'r' in sys.argv[1]

bigrams = [''.join(bigram) for bigram in product(chal.ALPHABET, repeat=2)]
bigrams = set(bigrams)


def parse_flag_ct(output):
    output = output.split('\n')
    ct = output[1]
    return ct[2:-2]


def parse_ct(output):
    output = output.split('\n')
    ct = output[1]
    return ct


def get_cycles():
    bigs = set(bigrams)  # Don't alter global
    cycles = []

    while len(bigs) > 0:
        cycle = [bigs.pop()]
        i = 0

        while True:
            if use_import:
                x = chal.encrypt(cycle[-1])
            else:
                io.sendline(cycle[-1])
                output = io.recvuntilS('>')
                x = parse_ct(output)

            if x == cycle[0]:
                break
            cycle.append(x)
            bigs.remove(x)
            x = x
            i += 1

            print('.', end='', flush=True)
        cycles.append(cycle)

    cycles.sort(key=lambda x: len(x))
    return cycles


def check_odd_cycles(cycles):
    clens = {}
    for c in cycles:
        clen = len(c)
        if clen in clens:
            clens[clen] += 1
        else:
            clens[clen] = 1

    for clen in clens:
        n = clens[clen]
        if n % 2 == 1 and n > 1:
            return False

    return True


def sep_knowns(cycles):
    unknowns = []
    knowns = []

    i = 0
    while i < len(cycles):
        if i + 1 < len(cycles) and len(cycles[i]) == len(cycles[i + 1]):
            unknowns.append(cycles[i])
            unknowns.append(cycles[i + 1])
            i += 2
        else:
            knowns.append(cycles[i])
            i += 1

    return knowns, unknowns


def count_iters(unknowns):
    n_iters = 1
    for i in range(0, len(unknowns), 2):
        n_iters *= len(unknowns[i])

    return n_iters


class Gbox:
    def init_known(self, c):
        n = len(c)
        mid = (n + 1) // 2
        for i, b in enumerate(c):
            de_i = (i + mid) % n
            de_b = c[de_i]
            self.rbox[de_b] = b

    def init_knowns(self, knowns):
        for c in knowns:
            self.init_known(c)

    def __init__(self, knowns, unknowns):
        self.rbox = {}
        self.knowns = knowns
        self.unknowns = unknowns
        self.init_knowns(knowns)

    def get(self, b):
        if b in self.rbox:
            return self.rbox[b]
        else:
            for xi, x in enumerate(self.unknowns):
                if b in x:
                    yi = xi ^ 1
                    y = self.unknowns[yi]

                    offset = self.offsets[xi // 2]
                    n = self.limits[xi // 2]

                    if b in x:
                        i = ((x.index(b) - 1) + offset) % n
                        return y[i]
                    else:
                        i = (y.index(b) - offset) % n
                        return x[i]

    def calc_unknown_limits(self):
        self.limits = []
        for i in range(0, len(self.unknowns), 2):
            self.limits.append(len(self.unknowns[i]))

    def inc_offsets(self):
        i = 0
        while True:
            self.offsets[i] += 1
            if self.offsets[i] == self.limits[i]:
                self.offsets[i] = 0
                i += 1
            else:
                break

    def decrypt_all(self, ct):
        self.calc_unknown_limits()
        self.offsets = [0] * len(self.limits)
        pts = []
        n_iters = count_iters(self.unknowns)

        # TODO: Not working when `len(self.unknowns)` > 2
        for i in range(n_iters):
            pts.append(self.decrypt(flag_ct))

            if i < n_iters - 1:
                self.inc_offsets()

        self.init_knowns(gbox.unknowns)
        self.unknowns = []
        pts.append(self.decrypt(ct))

        return pts

    def decrypt(self, ct):
        ct = list(ct)
        rounds = int(2 * ceil(log(len(ct), 2)))

        def unshuffle(ct):
            mid = len(ct) // 2
            evens = ct[:mid]
            odds = ct[mid:]
            for i, c in enumerate(ct):
                if i % 2 == 0:
                    ct[i] = evens[i // 2]
                else:
                    ct[i] = odds[i // 2]
            return ct

        for round in range(rounds):
            # Shuffle, but not in the first round
            if round > 0:
                ct = unshuffle(ct)

            # Decrypt
            for i in range(0, len(ct), 2):
                ct[i:i+2] = self.get(''.join(ct[i:i+2]))
                # ct[i:i+2] = gbox.get(''.join(ct[i:i+2]))

        return ''.join(ct)


if __name__ == "__main__":
    while True:
        if not use_import:
            if remote:
                io = pwn.remote('queensarah2.chal.perfect.blue', 1)
            else:
                io = pwn.process('challenge.py')

            output = io.recvuntilS('>')
            flag_ct = parse_flag_ct(output)
            print('Flag CT:', flag_ct)

        cycles = get_cycles()
        knowns, unknowns = sep_knowns(cycles)

        if check_odd_cycles(cycles):
            if len(unknowns) < 2:
                n_iters = len(unknowns)
                break
            else:
                n_iters = count_iters(unknowns)
                if n_iters < 500:
                    break
        else:
            print("check_odd_cycles doesn't like it")

        if use_import:
            chal.reload()
        print('#')
    print()

    print('cycles:', ' '.join([str(len(c)) for c in cycles]))
    print('knowns:', ' '.join([str(len(c)) for c in knowns]))
    print('unknowns:', ' '.join([str(len(c)) for c in unknowns]))

    gbox = Gbox(knowns, unknowns)

    pts = gbox.decrypt_all(flag_ct)
    pprint.pprint(pts)

    fn = 'output' + str(time.time())
    with open(fn, 'w') as f:
        for pt in pts:
            f.write(pt + '\n')

    io.interactive()
