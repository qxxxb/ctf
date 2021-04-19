# Substitution

**Category**: Crypto \
**Points**: 140 (130 solves) \
**Author**: EvilMuffinHa

## Challenge

Source:
```python
from functools import reduce

with open("flag", "r") as f:
    key = [ord(x) for x in f.read().strip()]


def substitute(value):
    return (reduce(lambda x, y: x * value + y, key)) % 691


print(
    "Enter a number and it will be returned with our super secret synthetic substitution technique"
)
while True:
    try:
        value = input("> ")
        if value == "quit":
            quit()
        value = int(value)
        enc = substitute(value)
        print(">> ", end="")
        print(enc)
    except ValueError:
        print("Invalid input. ")
```

`nc crypto.2021.chall.actf.co 21601`

## Overview

The meat of the problem is here:
```python
def substitute(value):
    return (reduce(lambda x, y: x * value + y, key)) % 691
```

There are already tons of writeups for this problem so I won't go in detail,
but basically this can just be solved as a system of linear equations.

Solve script in `solve.sage`. Output:
```
$ export PWNLIB_NOTERM=true
$ sage test1.sage
b'actf{polynomials_20a829322766642530cf69}'
b'\x00actf{polynomials_20a829322766642530cf69}'
b'\x00\x00actf{polynomials_20a829322766642530cf69}'
b'\x00\x00\x00actf{polynomials_20a829322766642530cf69}'
b'\x00\x00\x00\x00actf{polynomials_20a829322766642530cf69}'
...
```
