def get_subgroup(g, p):
    x = 1
    subgroup = {x}
    while True:
        if len(subgroup) > 2 ** 16:
            return None

        x = (x * g) % p
        if x in subgroup:
            return subgroup
        else:
            subgroup.add(x)



# p = 101
# p = 6211
p = 7591
g = 5

# 7390: 2, 3, 5, 11, 23
# How does this even work??
w = 11
# Using 2, 3, or 5 can give us 1. How is that possible?

assert (p - 1) % w == 0
k = (p - 1) // w
# k = (p - 1) // w * 12345
# We can multiply `k` by an integer as well!

pub_k = pow(g, k, p)

j = 3413  # random
pub_j = pow(g, j, p)

shared_j = pow(pub_k, j, p)
shared_k = pow(pub_j, k, p)
assert shared_j == shared_k

print("shared:", shared_j)
subgroup = get_subgroup(shared_j, p)
print(subgroup)
print(len(subgroup))
