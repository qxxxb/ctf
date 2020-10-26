import json
import base64
import binascii
from Crypto.Cipher import AES

config_key = b'1234567890123456'


def slice_block(ciphertext: bytes, index: int) -> bytes:
    block_size = 16
    start_i = block_size * index
    end_i = start_i + block_size
    return ciphertext[start_i:end_i]


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


def create_session(username: str) -> bytes:
    """
    Creates a new encrypted session cookie with the given username
    :param username: The username to create the session with
    :return: The encrypted and b64 encoded cookie
    """
    if 5 <= len(username) <= 20:
        session = {
            'name': username,
            'role': 'users'
        }

        cipher = AES.new(key=config_key, mode=AES.MODE_ECB)

        session_dump = json.dumps(
            session, separators=(',', ':'), sort_keys=True)

        cookie_data = session_dump.encode('ascii', errors='replace')
        print_str_blocks(session_dump)

        cookie_data = pkcs7_pad(cookie_data, 16)
        # print(cookie_data)

        cookie_data = cipher.encrypt(cookie_data)
        # print_hex_blocks(cookie_data)

        cookie_data = base64.b64encode(cookie_data)
        # print(cookie_data)

        return cookie_data
    else:
        raise ValueError("Username must be 5 to 20 characters")


def get_session(cookie: str) -> dict:
    """
    Decrypts and parses a session cookie
    :param cookie: The base64 encoded cookie string
    :return: A decoded session object
    """
    try:
        cipher = AES.new(key=config_key, mode=AES.MODE_ECB)
        cookie_data = pkcs7_unpad(cipher.decrypt(base64.b64decode(cookie)), 16)
        session_str = cookie_data.decode('ascii', errors='replace')
        # print(session_str)
        return json.loads(session_str)
    except (
        json.JSONDecodeError, UnicodeError, binascii.Error, AttributeError,
        Exception
    ):
        raise ValueError("Error parsing session")


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


if __name__ == '__main__':
    cookies = {}

    u = 'xxxxxxx'
    cookies['name'] = create_session(u).decode()

    u = '我_xxxxxx'
    cookies['name_to_role'] = create_session(u).decode()

    u = '我_administrators'
    cookies['admins'] = create_session(u).decode()

    u = '我"zzzzzzzzzzzzzzz'
    cookies['zzz'] = create_session(u).decode()

    u = '我":              '
    cookies['quote_colon'] = create_session(u).decode()

    u = '我"               '
    cookies['quote'] = create_session(u).decode()

    u = '我_}               '
    cookies['closing_bracket'] = create_session(u).decode()

    u = '我_xxxxxxxxxxxxxxx'
    cookies['fullpad'] = create_session(u).decode()

    def slice_index(k):
        return {
            'name': 0,
            'fullpad': 3,
        }.get(k, 1)

    widgets = {}
    for key in cookies:
        ciphertext = base64.b64decode(cookies[key])
        print_hex_blocks(ciphertext)
        print()

        si = slice_index(key)
        widget = slice_block(ciphertext, si)
        print_hex_blocks(widget)
        print("---")
        print()

        widgets[key] = widget

    ans = \
        widgets['name'] + \
        widgets['name_to_role'] + \
        widgets['admins'] + \
        widgets['zzz'] + \
        widgets['quote_colon'] + \
        widgets['quote'] + \
        widgets['quote'] + \
        widgets['closing_bracket'] + \
        widgets['fullpad']

    print_hex_blocks(ans)

    ans = base64.b64encode(ans)

    print()
    print(ans.decode())

    ans_dec = base64.b64decode(ans)
    print_hex_blocks(ans_dec)

    session = get_session(ans)
    print(session)
