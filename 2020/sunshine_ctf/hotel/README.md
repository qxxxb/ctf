# Hotel Door Puzzle

**Category**: Reverse engineering \
**Author**: [Helithumper](https://github.com/helithumper) \
**Points**: 100

I started by decompiling it with [Cutter](https://cutter.re/) and found this
crazy function:
```c
undefined8 check_flag(char *arg1)
{
    int64_t iVar1;
    undefined8 uVar2;
    char *s;

    iVar1 = strlen(arg1);
    if (iVar1 == 0x1d) {
        if (arg1[0x13] == '6') {
            arg1[6] = arg1[6] + '\x03';
            if (arg1[0x10] == 'n') {
                arg1[0x14] = arg1[0x14] + -8;
                arg1[0x1a] = arg1[0x1a] + -6;
                if (arg1[0xd] == 'r') {
                    if (arg1[0x14] == '%') {
                        if (arg1[0xf] == 'n') {
...
```

I didn't know how to do this besides slowly going through the entire function
and reversing the single branch that returned true.

Script:
```python
def dec(c, d):
    return chr(ord(c) - d)

arg1 = ["+"] * 29

arg1[0x13] = '6'
arg1[0x10] = 'n'
arg1[0xd] = 'r'
arg1[0x14] = dec('%', -8)
arg1[0xf] = 'n'
arg1[10] = 'p'
arg1[0x10] = dec('u', 7)
arg1[3] = '{'
arg1[0x13] = '6'
arg1[0x15] = 'q'
arg1[2] = 'n'
arg1[0] = 's'
arg1[7] = 'l'
arg1[0xe] = 'u'
arg1[0xc] = dec(',', -1)
arg1[4] = 'b'
arg1[6] = dec('o', 3)
arg1[0x12] = 'n'
arg1[0x16] = dec('z', 5)
arg1[0x17] = '1'
arg1[1] = 'u'
arg1[5] = dec('8', 5)
arg1[8] = dec('f', 3 + 4 - 9)
arg1[0xb] = dec('<', 7)
arg1[0x11] = dec('-', 6 - 8 + ord('\t') - 5 - 6)
arg1[9] = dec(',', 1 + 2 - 7)
arg1[0x18] = dec('Y', -10 - 8 + ord('\b'))
arg1[0x19] = dec('w', 5 + ord('\a'))
arg1[0x1a] = dec('m', -6 + ord('\a'))
arg1[0x1b] = 'y'
arg1[0x1c] = '}'

for i, c in enumerate(arg1):
    print(i, c)

print()

key = "".join(arg1)
print(key)

with open('key.txt', 'w') as f:
    f.write(key)
```

This gave me:
```
 python3 main.py
0 s
1 u
2 n
3 {
4 b
5 3
6 l
7 l
8 h
9 0
10 p
11 5
12 -
13 r
14 u
15 n
16 n
17 1
18 n
19 6
20 -
21 q
22 u
23 1
24 c
25 k
26 l
27 y
28 }

sun{b3llh0p5-runn1n6-qu1ckly}
```

I later found that one my teammates solved this problem using [angr.io](https://angr.io/):
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,angr

def main(argv):

    binary_path = "./hotel_key_puzzle"
    proj = angr.Project(binary_path)


    initial_state = proj.factory.entry_state(add_options={angr.options.LAZY_SOLVES})

    simgr = proj.factory.simulation_manager(initial_state)

    print_good_address =  0x4022ba# :integer (hex)

    simgr.explore(find=print_good_address)

    if simgr.found:
        solution_state = simgr.found[0]
        print(solution_state.posix.dumps(sys.stdin.fileno()))
    else:
        raise Exception('Could not find the solution')

if __name__ == '__main__':
    main(sys.argv)
```
