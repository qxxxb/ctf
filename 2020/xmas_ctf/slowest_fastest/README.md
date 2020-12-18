# Slowest Fastest

**Category**: Programming \
**Points**: 457 \
**Author**: Gabies, Nutu

## Challenge

This is an emergency, we need you to help us organize our gift building process. We're in a hurry so let's go!

Target: `nc challs.xmas.htsp.ro 6055`

## Solution

```
Hey, we've got a problem at the factory! As you well know we have N rooms in our factory, and in the i-th room we have v[i] gifts that have to be built.
Also, at the factory we have N mechagnomes of two possible types:
        K of them are the Fast-O-Bot type, which can build P gifts in a single day
        The rest of N - K bots are the Speed-O-Tron type which can build Q gifts in a single day.

Each day a mechagnome is assigned to a room, and that day it'll work all by itself in that room, building as many gifts as it can.
If there are no gifts to be built or he finishes all of them before the end of the day, the mechagnome goes idle. There cannot be two mechagnomes in the same room in the same day.
Since we're in a hurry, we need the minimum number of days we can build all gifts. Can you help us?
Just to be safe, we have to solve 100 such scenarios. We don't want to waste any time so we'll give you 60 seconds to solve everything.
Ah, and since our connection is so slow, we'll define v in the following way: v[i] = (a * v[i - 1] + c) % mod for all i = 2, n

Test number: 1/100
N = 10, K = 4
P = 118, Q = 134
v[1] = 91613, a = 71823, c = 30886, mod = 100001
```

Solved with Soronbe and stdnoerror.

Idea is to assign the fastest robots to the busiest rooms on each day.

To make it fast, we do a binary search on the possible number of days.
The `can_finish` function tells us whether it's possible to finish in a given
number of days.

The running time for `can_finish` is `O(n)` and binary search takes
`O(log(mod))` time, so the total running time is `O(n * log(mod))`.

This is much faster than direct simulation on each day, which would be
`O(n * days)`.

Full script in `solve.py`.
PyPy3 is required to finish within the time limit.

```
Attempt 99
[DEBUG] Received 0x28 bytes:
    b'Good, thats right!\n'
    b'Test number: 100/100\n'
[DEBUG] Received 0x6e bytes:
    b'N = 924488, K = 424143\n'
    b'P = 23448, Q = 13748\n'
    b'v[1] = 421614616, a = 545616627, c = 126523786, mod = 1000000001\n'
    b'\n'
[DEBUG] Sent 0x6 bytes:
    b'42648\n'
[*] Switching to interactive mode
[DEBUG] Received 0x7b bytes:
    b'Good, thats right!\n'
    b'Thanks for saving Christmas this year!\n'
    b"Here's the flag: X-MAS{l0l_h0w_15_7h1s_4_b1n4ry_s34rch_pr0bl3m?}\n"
Good, thats right!
Thanks for saving Christmas this year!
Here's the flag: X-MAS{l0l_h0w_15_7h1s_4_b1n4ry_s34rch_pr0bl3m?}
```
