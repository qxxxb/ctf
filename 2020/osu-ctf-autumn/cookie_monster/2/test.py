from Crypto.Cipher import AES
from Crypto.Random import random
import requests

block_size = 16
config_key = b'1234567890123456'
target_url = "http://pwn.osucyber.club:13375"


def print_hex_blocks(ciphertext: bytes):
    for i in range(len(ciphertext)):
        b = ciphertext[i:i+1]
        print(b.hex(), end='')

        if i > 0:
            if (i + 1) % 16 == 0:
                print()
            elif (i + 1) % 2 == 0:
                print(end=' ')


def print_str_blocks(plaintext: str):
    for i, c in enumerate(plaintext):
        print(c, end='')

        if i > 0:
            if (i + 1) % 16 == 0:
                print()

    if (i + 1) % 16 != 0:
        print()


def split_blocks(data):
    return [data[s:s + 16] for s in range(0, len(data), 16)]


def slice_block(ciphertext: bytes, index: int) -> bytes:
    start_i = block_size * index
    end_i = start_i + block_size
    return ciphertext[start_i:end_i]


def encrypt(pt: bytes, iv: bytearray) -> bytes:
    cipher = AES.new(key=config_key, mode=AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pt)
    return ct


def decrypt(ct: bytes, iv: bytearray) -> bytes:
    cipher = AES.new(key=config_key, mode=AES.MODE_CBC, iv=iv)
    pt = cipher.decrypt(ct)
    return pt


def pre_str(pt: str) -> bytes:
    pt = pt.encode('ascii', errors='replace')
    pt = pkcs7_pad(pt)
    return pt


def post_str(pt: bytes) -> str:
    pt = pkcs7_unpad(pt)
    pt = pt.decode('ascii', errors='replace')
    return pt


def pkcs7_pad(data: bytes, blocksize: int = 16) -> bytes:
    """
    Implements PKCS7 padding
    :param data: The data to pad
    :param blocksize: The block size to calculate padding based on
    :return: Padded data
    """
    d = bytearray(data)
    padding_len = blocksize - len(d) % blocksize
    d.extend(padding_len for _ in range(padding_len))
    return bytes(d)


def pkcs7_unpad(data: bytes, blocksize: int = 16) -> bytes:
    """
    Validates and removes PKCS7 padding
    :param data: The padded data
    :param blocksize: The blocksize to validate padding based on
    :return: data with padding removed
    """
    if len(data) == 0 or len(data) % blocksize != 0:
        raise ValueError("Invalid Padding")
    elif not 0x00 < data[-1] <= blocksize:
        raise ValueError("Invalid Padding")
    elif any(data[-1-i] != data[-1] for i in range(data[-1])):
        raise ValueError("Invalid Padding")
    else:
        return data[:-data[-1]]


def xor(xs: bytes, ys: bytes) -> bytes:
    ans = [x ^ by for x, by in zip(xs, ys)]
    return bytes(ans)


# We're not supposed to be able to control this
random_iv = b'6543212987684321'


def arbitrary_ct_pair():
    pt = "arbitrary"
    pt = pre_str(pt)

    ct_prime = xor(pt, random_iv)
    ct = encrypt(pt, random_iv)
    return (ct, ct_prime)


def valid_padding(cookie):
    res = requests.get(f"{target_url}/flag",
                       cookies={'SESSIONID1': cookie}, allow_redirects=False)

    print(res.txt)
    return False


def padding_oracle_attack(payload: str):
    ciphertexts = bytes(random.randint(0, 255) for _ in range(16))
    plaintext_blocks = split_blocks(payload)

    for i in range(len(plaintext_blocks) - 1):
        two_block_str = [0] * block_size
        two_block_str += ciphertexts[0]

        for exp_pad in range(block_size + 1):
            for byte in range(256):
                two_block_str[block_size - exp_pad] = byte
                if valid_padding(two_block_str):
                    pass


def main():
    arb_ct, arb_ct_prime = arbitrary_ct_pair()

    desired_pt = '{"name":"123456","role":"admin"}'
    print_str_blocks(desired_pt)


main()
