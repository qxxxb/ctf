import pwn

computed = {}


def sterling2(n, k):
    key = str(n) + "," + str(k)

    if key in computed.keys():
        return computed[key]
    if n == k == 0:
        return 1
    if (n > 0 and k == 0) or (n == 0 and k > 0):
        return 0
    if n == k:
        return 1
    if k > n:
        return 0
    result = k * sterling2(n - 1, k) + sterling2(n - 1, k - 1)
    computed[key] = result
    return result


def prime_factors(n):
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors


def solve(gn, ln):
    if ln % gn != 0:
        return 0

    b = ln // gn
    ps = prime_factors(b)
    return 2 * (sterling2(len(ps), 2) + 1)


def get_n():
    s = io.recvlineS()
    a = s.split(' = ')
    return int(a[1])


if __name__ == '__main__':
    pwn.context.log_level = 'debug'
    io = pwn.remote('challs.xmas.htsp.ro', 6050)

    for _ in range(5):
        io.recvline()

    i = 1
    while i <= 100:
        print("Question", i)
        io.recvline()
        gn = get_n()
        ln = get_n()
        ans = solve(gn, ln)
        io.sendline(str(ans))

        output = io.recvline().strip()
        if output == 'That is not the correct answer!':
            exit(1)

        i += 1

    io.interactive()
