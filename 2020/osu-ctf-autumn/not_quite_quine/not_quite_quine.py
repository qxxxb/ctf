from functools import reduce
s=''
c=b'cC/txgU\x05@J\x1bT6\x18\x0b|\x07\x1d\x13QU*'
f=b''
print(s.format(s=repr(s),c=c,f=bytes(reduce(lambda a,b:a^ord(b),s[i:len(s):len(c)],c[i]) for i in range(len(c)))))
