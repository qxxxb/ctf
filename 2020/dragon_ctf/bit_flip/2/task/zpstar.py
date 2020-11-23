import gmpy2


def order(g, p):
    x = 1
    group = {x}
    while True:
        if len(group) > 2 ** 16:
            return -1

        x = (x * g) % p
        if x in group:
            break
        else:
            group.add(x)

    return len(group)


def get_group(g, p):
    x = 1
    group = {x}
    while True:
        if len(group) > 2 ** 16:
            return None

        x = (x * g) % p
        if x in group:
            break
        else:
            group.add(x)

    return group


# p = 101
# p = 101
# p = 103
# p = 6211
# p = 7591

group_lens = {}
p = 1
g = 5

primes = []
for i in range(1000):
    p = gmpy2.next_prime(p)
    if (p - 1) % 5 == 0:
        primes.append(p)

for p in primes:
    group_lens[p] = order(g, p)

# for i in range(1000):
#     p = gmpy2.next_prime(p)
#     group_lens[p] = order(g, p)
