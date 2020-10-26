import base64
import json
import re
from itertools import chain
import requests

TARGET_URL = "http://pwn.osucyber.club:13375"

def split_blocks(data):
    return [data[s:s + 16] for s in range(0, len(data), 16)]


def merge_blocks(blocks):
    return bytes(chain.from_iterable(blocks))


def pkcs7(data: bytes, blocksize: int = 16) -> bytes:
    d = bytearray(data)
    padding_len = blocksize - len(d) % blocksize
    d.extend(padding_len for _ in range(padding_len))
    return bytes(d)


def get_cookie(name):
    res = requests.post(f"{TARGET_URL}/login", {"username": name}, allow_redirects=False)
    for cookie in res.cookies:
        if cookie.name == 'SESSIONID1':
            return cookie.value
    return None


def make_cleartext(name):
    session = {'name': name, 'role': 'users'}
    return pkcs7(json.dumps(session, separators=(',', ':')).encode('ascii', errors='replace'))


def get_flag(cookie):
    res = requests.get(f"{TARGET_URL}/flag", cookies={'SESSIONID1': cookie}, allow_redirects=False)
    print(*re.findall(r'osuctf{.*}', res.text), sep='\n')


# Get a few specially chosen cookies
names = [
    # For the block containing '"administrators"' (The quotes let us go past the 20-character limit)
    # {"name":"AAAA\"\"administrators","role":"users"}PPPPPPPPPPPPPPPP
    # #-------1-------#-------2-------#-------3-------#-------4-------
    "AAAA\"\"administrators",
    # For the blocks containing '{"name":"AAAAAAAAAAAAAA","role":' (ending just before the "users" string)
    # {"name":"AAAAAAAAAAAAAA","role":"users"}PPPPPPPP
    # #-------1-------#-------2-------#-------3-------
    "AAAAAAAAAAAAAA",
    # For the block containing '}PPPPPPPPPPPPPPP'
    # {"name":"AAAAAAA","role":"users"}PPPPPPPPPPPPPPP
    # #-------1-------#-------2-------#-------3-------
    "AAAAAAA"
]
# Get a cookie for each name and store it along with the cleartext cookie
cookies = {make_cleartext(name): base64.b64decode(get_cookie(name)) for name in names}

# Create a dict of all the cleartext/ciphertext block pairs we have
strings = {}
for cleartext, ciphertext in cookies.items():
    strings.update({a: b for a, b in zip(split_blocks(cleartext), split_blocks(ciphertext))})

# Assemble a new encrypted cookie from the ciphertext blocks collected
# {"name":"AAAAAAAAAAAAAA","role":"administrators"}PPPPPPPPPPPPPPP
# #-------1-------#-------2-------#-------3-------#-------4-------
new_cookie_data = pkcs7(b'{"name":"AAAAAAAAAAAAAA","role":"administrators"}')
new_cookie = base64.b64encode(merge_blocks(strings[b] for b in split_blocks(new_cookie_data))).decode('ascii')
print(f"Cookie: {new_cookie}")
get_flag(new_cookie)


