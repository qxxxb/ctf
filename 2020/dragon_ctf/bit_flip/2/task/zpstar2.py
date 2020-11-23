def subgroup(g, p):
    x = g
    subgroup = {x}
    while True:
        if len(subgroup) > 2 ** 16:
            return {}

        x = (x * g) % p
        if x == 1:
            return subgroup
        else:
            subgroup.add(x)


def order(g, p):
    r = 1
    x = g
    while True:
        if r > 2 ** 16:
            return -1

        x = (x * g) % p
        r += 1
        if x == 1:
            return r


threshold = 2 ** 16

# p = 101
# p = 6211
p = 7591
ws = [2, 3, 5, 11, 23]

# 11391379263766066030135918376562538981196391001827571715194865455842376327512086588913712210956579206753407897779606205522510652032504825336272563672326153
# 175083521025227068065005769255555330084246339562637073163258119397507888347146180107558222551295089760865507217657571191905153189246459685033749
# [mpz(2), mpz(2), mpz(2), mpz(3), mpz(67), mpz(109), mpz(229), mpz(1621)]
# p = 11391379263766066030135918376562538981196391001827571715194865455842376327512086588913712210956579206753407897779606205522510652032504825336272563672326153
# ws = [2, 3, 67, 109, 229, 1621]

g = 5

orders = {}
for i in range(1, p):
    orders[i] = order(i, p)

for i in orders:
    if orders[i] == p - 1:
        print(i, orders[i])

for w in ws:
    q = (p - 1) // w
    assert w * q == p - 1
    ins_pub = pow(g, q, p)  # Magic
    print(w, order(ins_pub, p))

# print("shared:", shared_j)
# subgroup = get_subgroup(shared_j, p)
# print(subgroup)
# print(len(subgroup))
