from z3 import *
from random import Random
from itertools import count
from time import time
from tqdm import tqdm
import os

os.environ["PWNLIB_NOTERM"] = "true"
import pwn

SYMBOLIC_COUNTER = count()


def get_a_b_shifted(x: int):
    # x is multiplied by 2 ** 53, so it's an integer now
    return x >> 26, x % (2 ** 26)


def get_a_b_str(x: int):
    a_shifted, b_shifted = get_a_b_shifted(x)
    a_str = bin(a_shifted)[2:] + "?" * 5
    b_str = bin(b_shifted)[2:] + "?" * 6
    a_str = a_str.rjust(32, "0")
    b_str = b_str.rjust(32, "0")
    return a_str, b_str


def chunks(xs, n):
    """Yield successive n-sized chunks from xs."""
    for i in range(0, len(xs), n):
        yield xs[i : i + n]


class Untwister:
    def __init__(self):
        name = next(SYMBOLIC_COUNTER)
        self.MT = [BitVec(f"MT_{i}_{name}", 32) for i in range(624)]
        self.index = 0
        self.solver = Solver()

    # This particular method was adapted from https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
    def symbolic_untamper(self, solver, y):
        name = next(SYMBOLIC_COUNTER)

        y1 = BitVec(f"y1_{name}", 32)
        y2 = BitVec(f"y2_{name}", 32)
        y3 = BitVec(f"y3_{name}", 32)
        y4 = BitVec(f"y4_{name}", 32)

        equations = [
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18)),
        ]

        solver.add(equations)
        return y1

    def symbolic_twist(
        self,
        MT,
        n=624,
        upper_mask=0x80000000,
        lower_mask=0x7FFFFFFF,
        a=0x9908B0DF,
        m=397,
    ):
        """
        This method models MT19937 function as a Z3 program
        """
        MT = [i for i in MT]  # Just a shallow copy of the state

        for i in range(n):
            x = (MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)
            xA = LShR(x, 1)
            xB = If(
                x & 1 == 0, xA, xA ^ a
            )  # Possible Z3 optimization here by declaring auxiliary symbolic variables
            MT[i] = MT[(i + m) % n] ^ xB

        return MT

    def get_symbolic(self, guess):
        name = next(SYMBOLIC_COUNTER)
        ERROR = 'Must pass a string like "?1100???1001000??0?100?10??10010" where ? represents an unknown bit'

        assert type(guess) == str, ERROR
        assert all(map(lambda x: x in "01?", guess)), ERROR
        assert len(guess) <= 32, "One 32-bit number at a time please"
        guess = guess.zfill(32)

        self.symbolic_guess = BitVec(f"symbolic_guess_{name}", 32)
        guess = guess[::-1]

        for i, bit in enumerate(guess):
            if bit != "?":
                self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

        return self.symbolic_guess

    def submit(self, guess):
        """
        You need 624 numbers to completely clone the state.
            You can input less than that though and this will give you the best guess for the state
        """
        if self.index >= 624:
            name = next(SYMBOLIC_COUNTER)
            next_mt = self.symbolic_twist(self.MT)
            self.MT = [BitVec(f"MT_{i}_{name}", 32) for i in range(624)]
            for i in range(624):
                self.solver.add(self.MT[i] == next_mt[i])
            self.index = 0

        symbolic_guess = self.get_symbolic(guess)
        symbolic_guess = self.symbolic_untamper(self.solver, symbolic_guess)
        self.solver.add(self.MT[self.index] == symbolic_guess)
        self.index += 1

    def get_random(self):
        """
        This will give you a random.Random() instance with the cloned state.
        """
        print("Solving...")
        start = time()
        self.solver.check()
        model = self.solver.model()
        end = time()
        print(f"Solved! (in {round(end-start,3)}s)")

        # Compute best guess for state
        state = list(map(lambda x: model[x].as_long(), self.MT))
        result_state = (3, tuple(state + [self.index]), None)
        r = Random()
        r.setstate(result_state)
        return r


def test():
    """
    This test tries to clone Python random's internal state, given partial output from getrandbits
    """

    r1 = Random()
    ut = Untwister()
    for _ in tqdm(range(1000)):
        x = r1.random()
        x = int(2 ** 53 * x)
        a, b = get_a_b_str(x)
        assert len(a) == 32
        assert len(b) == 32

        # Just send stuff like "?11????0011?0110??01110????01???"
        # Where ? represents unknown bits
        # ut.submit(bin(random_num)[2:] + "?" * 16)
        ut.submit(a)
        ut.submit(b)

    r2 = ut.get_random()
    for _ in range(624):
        assert r1.getrandbits(32) == r2.getrandbits(32)

    print("Test passed!")


if pwn.args.REMOTE:
    io = pwn.remote("crypto.zh3r0.cf", 4444)
else:
    io = pwn.process("python3 challenge.py", shell=True)


def parse_score(s: str):
    frac = s.strip().split()[-1]
    if "/" in frac:
        num, denom = [int(x) for x in frac.split("/")]
        fac = 9007199254740992 // num
        return denom * fac
    else:
        n = int(frac)
        return 9007199254740992 // n


def send_gs(gs):
    s = "\n".join(str(g) for g in gs)
    io.sendline(s)


def recv_xs(n):
    xs = []
    for i in range(n):
        io.recvline()
        xs.append(parse_score(io.recvlineS()))
    return xs


def main():
    ut = Untwister()

    n_collect = 624
    gs = [0.0] * n_collect
    send_gs(gs)
    xs = recv_xs(len(gs))

    for x in tqdm(xs):
        # pwn.log.info(f"x = {x}")
        a, b = get_a_b_str(x)
        assert len(a) == 32
        assert len(b) == 32

        # Just send stuff like "?11????0011?0110??01110????01???"
        # Where ? represents unknown bits
        ut.submit(a)
        ut.submit(b)

    preds = []
    pred_rng = ut.get_random()

    n_left = 2000 - n_collect
    for _ in range(n_left):
        preds.append(pred_rng.random())

    pwn.log.info(f"predicted = {preds}")
    pwn.context.log_level = "debug"

    cs = chunks(preds, n=512)

    for c in cs:
        send_gs(c)
        xs = recv_xs(len(c))

    io.interactive()


if __name__ == "__main__":
    main()
