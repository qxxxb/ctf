# Least Greatest

**Category**: Programming \
**Points**: 50 \
**Author**: Gabies, Nutu

## Challenge

Today in Santa's course in Introduction to Algorithms, Santa told us about the
greatest common divisor and the least common multiple.  He this gave the
following problem as homework and I don't know how to solve it.  Can you please
help me with it?

Target: `nc challs.xmas.htsp.ro 6050`

## Solution

```
$ nc challs.xmas.htsp.ro 6050
Hey, you there! You look like you know your way with complex alogrithms.
There's this weird task that I can't get my head around. It goes something like this:
Given two numbers g and l, tell me how many pairs of numbers (x, y) exist such that gcd(x, y) = g and lcm(x, y) = l
Also, i have to answer 100 such questions in at most 90 seconds.

Test number: 1/100
gcd(x, y) = 28474200049
lcm(x, y) = 13820152331763541836406583892049969
```

Smaller example
```
x = 2 * 2 * 3 * 5 * 5 * 5 * 7 * 7
  = 73500

y = 2 * 2 * 3 * 3 * 5 * 7 * 9 * 9
  = 102060

gn = gcd(x, y) = The least number of common factors
  = 2 * 2 * 3 * 5 * 7

ln = lcm(x, y) = The most number of common factors
  = 2 * 2 * 3 * 3 * 5 * 5 * 5 * 7 * 7 * 9 * 9

d = lcm(x, y) / gcd(x, y) = The other factors
  = 3 * 5 * 5 * 7 * 9 * 9
  = (3) * (5**2) * (7) * (9**2)
```

For two numbers to have a GCD of `gn`, they must have at least those prime
factors. \
For two numbers to have an LCM of `ln`, they need to have at most those prime factors.

Given this case
```
a = gn * 3 * (9**2)
b = gn * (5**2) * 7
```

Notice that
```
gcd(a, b) == gn
lcm(a, b) == ln
```

The key is that
- `a` and `b` must include `gn`
- `a` and `b` cannot share any prime factors aside from `gn`
- `a` and `b` must use all prime factors from `d`

The answer to the problem is the number of ways to partition the unique prime
factors (`{3, 5, 7, 9}` in this case) of `d` into two sets.

To calculate this, we can just use this formula:
[Stirling numbers of the second kind](https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind)

I don't really understand how it works so I just stole the Python
implementation from Rosetta code
[here](https://rosettacode.org/wiki/Stirling_numbers_of_the_second_kind#Python).

So the algorithm is just
```python
gn = gcd(a, b)
ln = lcm(a, b)
d = gn // ln
ps = set(prime_factors(d))
# Add 1 to account for (gn, ln)
# (x, y) and (y, x) are different, so multiply by two
ans = 2 * (stirling2(len(ps), 2) + 1)
```

Full script in `solve.py`

```
...
Question 100
[DEBUG] Sent 0xb bytes:
    b'8589934592\n'
[DEBUG] Received 0xa1 bytes:
    b"Good, that's right!\n"
    b'Wow, you really know this kind of weird math?\n'
    b" Here's your flag: X-MAS{gr347es7_c0mm0n_d1v1s0r_4nd_l345t_c0mmon_mult1pl3_4r3_1n73rc0nn3ct3d}\n"
[*] Switching to interactive mode
Wow, you really know this kind of weird math?
 Here's your flag: X-MAS{gr347es7_c0mm0n_d1v1s0r_4nd_l345t_c0mmon_mult1pl3_4r3_1n73rc0nn3ct3d}
```
