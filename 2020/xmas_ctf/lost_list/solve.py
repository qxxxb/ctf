import pwn
from Crypto.Util.number import long_to_bytes


def pad(s):
    '''PKCS #7 padding'''
    pad_len = 16 - (len(s) % 16)
    return s + long_to_bytes(pad_len) * pad_len


known_payload = bytes.fromhex(
    '53616e74612773313333374956343230ab0c288b0ae26eaf8adbcf00bddf35fa'
)
# b'Santa's1337IV420\xab\x0c(\x8b\n\xe2n\xaf\x8a\xdb\xcf\x00\xbd\xdf5\xfa'

known_iv = known_payload[:16]
known_ct = known_payload[16:]
known_pt = pad(b'ls')
known_imm = pwn.xor(known_iv, known_pt)  # imm = immediate state


def forge_iv(pt):
    return pwn.xor(known_imm, pad(pt.encode()))


def enc(pt):
    return (forge_iv(pt) + known_ct).hex()


if __name__ == '__main__':
    io = pwn.remote('challs.xmas.htsp.ro', 1002)
    while True:
        try:
            print(io.recvS(), end='')
        except EOFError:
            io = pwn.remote('challs.xmas.htsp.ro', 1002)
            print(io.recvS(), end='')

        s = input()
        p = enc(s)
        io.sendline(p)
