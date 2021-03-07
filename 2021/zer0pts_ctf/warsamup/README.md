# war(sa)mup

**Category**: Crypto \
**Points**: 102 (95 solves) \
**Author**: theoldmoon0602

## Challenge

Do you know RSA? I know. \
Attachments: `warsamup.tar.gz`

## Solution

Here's the task:

```python
from Crypto.Util.number import getStrongPrime, GCD
from random import randint
from flag import flag
import os

def pad(m: int, n: int):
  # PKCS#1 v1.5 maybe
  ms = m.to_bytes((m.bit_length() + 7) // 8, "big")
  ns = n.to_bytes((n.bit_length() + 7) // 8, "big")
  assert len(ms) <= len(ns) - 11

  ps = b""
  while len(ps) < len(ns) - len(ms) - 3:
    p = os.urandom(1)
    if p != b"\x00":
      ps += p
  return int.from_bytes(b"\x00\x02" + ps + b"\x00" + ms, "big")


while True:
  p = getStrongPrime(512)
  q = getStrongPrime(512)
  n = p * q
  phi = (p-1)*(q-1)
  e = 1337
  if GCD(phi, e) == 1:
    break

m = pad(int.from_bytes(flag, "big"), n)
c1 = pow(m, e, n)
c2 = pow(m // 2, e, n)

print("n =", n)
print("e =", e)
print("c1=", c1)
print("c2=", c2)
```

The `pad` function looks interesting, but since both `c1` and `c2` use the same
padded message, it doesn't seem to matter.

Knowing that, it seems like the
[Franklin-Reiter related message attack](https://crypto.stackexchange.com/q/30884)
will work.

The only twist is this: `c2 = pow(m // 2, e, n)`.
- If `m` is even, then `m == (m // 2) * 2`
- If `m` is odd, then `m == (m // 2) * 2 + 1`

To check if `m` is even or odd, we can do this:
```python
assert c1 != (c2 * pow(2, e, n)) % n
```

Now we know `m` is odd and:
```python
assert c2 == pow((m - 1) // 2, e, n)

two_inv = inverse_mod(2, n)
assert c2 == pow(two_inv * (m - 1), e, n)
```

Therefore the polyonmials we use for Franklin-Reiter's attack are:
```python
f1 = X^e - c1
f2 = (two_inv * (X - 1))^e - c2
```

Here's my solution:
```python
import Crypto.Util.number as cun

n = 113135121314210337963205879392132245927891839184264376753001919135175107917692925687745642532400388405294058068119159052072165971868084999879938794441059047830758789602416617241611903275905693635535414333219575299357763227902178212895661490423647330568988131820052060534245914478223222846644042189866538583089
e = 1337
c1= 89077537464844217317838714274752275745737299140754457809311043026310485657525465380612019060271624958745477080123105341040804682893638929826256518881725504468857309066477953222053834586118046524148078925441309323863670353080908506037906892365564379678072687516738199061826782744188465569562164042809701387515
c2= 18316499600532548540200088385321489533551929653850367414045951501351666430044325649693237350325761799191454032916563398349042002392547617043109953849020374952672554986583214658990393359680155263435896743098100256476711085394564818470798155739552647869415576747325109152123993105242982918456613831667423815762

# c1 = pow(m, e, n)
# c2 = pow(m // 2, e, n)

two_inv = inverse_mod(2, n)
# We know c1 != (c2 * pow(2, e, n)) % n
# Therefore m is odd and:
# c2 = pow((m - 1) // 2, e, n)
# c2 = pow(two_inv * (m - 1), e, n)

R.<X> = Zmod(n)[]
f1 = X^e - c1
f2 = (two_inv * (X - 1))^e - c2

# GCD is not implemented for rings over composite modulus in Sage
def pgcd(f, g):
    while g:
        r = f % g
        f, g = g, r
    return f.monic()

ans = -pgcd(f1, f2).coefficients()[0]
ans = cun.long_to_bytes(ans)
i = ans.rfind(b"\x00")
ans = ans[i + 1:]
print(ans)
```

Output:
```
$ sage solve.sage
b'zer0pts{y0u_g07_47_13457_0v3r_1_p0in7}'
```
