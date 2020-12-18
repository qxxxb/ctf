# Many Paths

**Category**: Programming \
**Points**: 167 \
**Author**: Gabies, Nutu

## Challenge

Today in Santa's course in Advanced Graph Algorithms, Santa told us about the
adjacency matrix of an undirected graph. I'm sure this last problem, he gave us
is unsolvable, but I don't know much, maybe you do.

Target: `nc challs.xmas.htsp.ro 6053`

## Solution

```
$ nc challs.xmas.htsp.ro 6053
I swear that Santa is going crazy with those problems, this time we're really screwed!
The new problem asks us the following:
Given an undirected graph of size N by its adjacency matrix and a set of forbidden nodes, tell me how many paths from node 1 to node N of exactly length L that don't pass through any of the forbidden nodes exist (please note that a node can be visited multiple times)?
And if that wasn't enough, we need to answer 40 of those problems in 45 seconds and to give each output modulo 666013. What does that even mean!?

Test number: 1/40
N = 3
adjacency matrix:
0,0,1
0,0,0
1,0,0
forbidden nodes: [2]
L = 4
```

Google this:
```
number of paths in a graph adjacency matrix
```

Find this: https://math.stackexchange.com/q/1890620

If `A` is the adjacency matrix of a graph, then `ij`'th entry of `A^k` will give
me the number of `k`-length paths connecting the vertices `i` and `j`.

For the forbidden nodes, we just remove them from the adjacency matrix by
zero-ing out their corresponding row and column.

Last thing to remember is to give the output modulo 666013. To avoid huge
numbers when `k` is large, take the modulus before each power.

Script in `solve.py`.
```
...
N = 43

[DEBUG] Received 0x372 bytes:
    b'1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n'
    b'0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0\n'
    b'0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0\n'
    b'0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1\n'
    b'0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0\n'
    b'0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0\n'
    b'1,0,0,0,0,1,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,1,0,0,1,0,1\n'
    b'1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0\n'
    b'0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0\n'
    b'0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0\n'
    b'forbidden nodes: [33,23]\n'
    b'L = 63371\n'
    b'\n'
[DEBUG] Sent 0x7 bytes:
    b'612830\n'
[DEBUG] Received 0xab bytes:
    b'Good, thats right!\n'
    b'I cannot believe you figured this one out, how does this code even work?\n'
    b"I'm baffled, here's the flag: X-MAS{n0b0dy_3xp3c73d_th3_m47r1x_3xp0n3n71a7i0n}\n"
[*] Switching to interactive mode
I cannot believe you figured this one out, how does this code even work?
I'm baffled, here's the flag: X-MAS{n0b0dy_3xp3c73d_th3_m47r1x_3xp0n3n71a7i0n}
```
