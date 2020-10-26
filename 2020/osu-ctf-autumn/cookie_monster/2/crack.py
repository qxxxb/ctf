from pwn import *
from paddingoracle import BadPaddingException, PaddingOracle
import json
from Crypto.Cipher import AES


class PadBuster(PaddingOracle):
    def oracle(self, data):
        while True:
            try:
                r = remote("http://pwn.osucyber.club:13376/login", 13376)
                r.recvuntil("cookie?")
                s = data
                s = str(data).encode("hex")
                r.sendline(s)
                out = r.recvall()
                if "Invalid Padding" in out:
                    raise BadPaddingException
                return
            except (socket.error, socket.gaierror, socket.herror, socket.timeout) as e:
                print str(e)


if __name__ == '__main__':
    d = {"role": "admin"}
    s = json.dumps(d)
    print s
    padbuster = PadBuster()
    encrypted = padbuster.encrypt(
        s, block_size=AES.block_size, iv="This is an IV456")

    print "Ciphertext: %r" % (str(encrypted).encode("hex"))
