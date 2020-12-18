import pwn
import heapq
import ast


def solve(xs, k1, k2):
    hlow = []
    hhigh = []

    for x in xs:
        heapq.heappush(hlow, x)
        heapq.heappush(hhigh, -x)

    lows = []
    highs = []

    for _ in range(k1):
        lows.append(heapq.heappop(hlow))
    for _ in range(k2):
        highs.append(-heapq.heappop(hhigh))

    return lows, highs


def format_ans(both):
    ls = [str(x) for x in both[0]]
    hs = [str(x) for x in both[1]]
    return ', '.join(ls) + '; ' + ', '.join(hs)


if __name__ == '__main__':
    pwn.context.log_level = 'debug'
    io = pwn.remote('challs.xmas.htsp.ro', 6051)

    for i in range(7):
        io.recvline()

    def get_xs():
        s = io.recvlineS()
        a = s.split(' = ')
        s = a[1]
        xs = ast.literal_eval(s)
        return xs

    def get_k():
        s = io.recvlineS()
        a = s.split(' = ')
        return int(a[1])

    i = 1
    while i <= 50:
        xs = [1, 9, 8, 10, 7]
        io.recvline()
        xs = get_xs()
        k1 = get_k()
        k2 = get_k()
        ans = format_ans(solve(xs, k1, k2))
        io.sendline(ans)
        io.recvline()
        i += 1

    io.interactive()
