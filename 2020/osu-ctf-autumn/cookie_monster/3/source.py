from flask import Flask, render_template, request, redirect, url_for, current_app, send_file
import os
import json
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Protocol.KDF import PBKDF2
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__,
            static_url_path='',
            template_folder="templates",
            static_folder="static")
app.config['NAME'] = "CookieMonster Pt. 3"
app.config['FLAG'] = os.environ['PART_THREE_FLAG']
app.config['KEY'] = PBKDF2(os.environ['COOKIE_JAR_KEY'], bytes(os.environ['PART_THREE_FLAG'], 'ascii'), 16, count=1000000)
app.config['COOKIE_ID'] = 'SESSIONID3'
app.config['SUPER_SECRET_STRING'] = os.environ['SUPER_SECRET_STRING']


class SessionError(Exception):
    """Represents an error creating or parsing a session cookie"""
    pass


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/source')
def source():
    return send_file(__file__)


@app.route('/flag')
def flag():
    if session := request.cookies.get(current_app.config.get('COOKIE_ID', 'SESSIONID')):
        try:
            session = get_session(session)
        except SessionError as e:
            res = redirect(url_for('login', err=e.args))
            res.set_cookie(current_app.config.get('COOKIE_ID', 'SESSIONID'), '', max_age=0)
            return res

        flag_text = "Sorry, you must be an administrator to see the flag."
        if session.get('role', 'users') == 'admin':
            flag_text = current_app.config['FLAG']

        return render_template("flag.html", flag=flag_text, name=session.get('name', ''))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = redirect(url_for('flag'))
        if form := request.form:
            try:
                cookie = create_session(form.get('username', ''))
                res.set_cookie(current_app.config.get('COOKIE_ID', 'SESSIONID'), cookie.decode('ascii'), max_age=3600)
            except SessionError as e:
                return redirect(url_for('login', err=e.args))
        return res
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    res = redirect(url_for('login'))
    res.set_cookie(current_app.config.get('COOKIE_ID', 'SESSIONID'), '', max_age=0)
    return res


def create_session(username: str) -> bytes:
    """
    Creates a new encrypted session cookie with the given username
    :param username: The username to create the session with
    :return: The encrypted and b64 encoded cookie
    """
    if 5 <= len(username) <= 20:
        session = {
            'name': username,
            'q': current_app.config['SUPER_SECRET_STRING'],
            'role': 'users'
        }
        iv = bytes(random.randint(0, 255) for _ in range(16))
        cookie = bytearray(iv)
        cookie_data = json.dumps(session, separators=(',', ':'), sort_keys=True).encode('ascii', errors='replace')
        cipher = AES.new(key=current_app.config['KEY'], mode=AES.MODE_CBC, iv=iv)
        cookie.extend(cipher.encrypt(pkcs7_pad(cookie_data)))
        return base64.b64encode(bytes(cookie))
    else:
        raise SessionError("Username must be 5 to 20 characters")


def get_session(cookie: str) -> dict:
    """
    Decrypts and parses a session cookie
    :param cookie: The base64 encoded cookie string
    :return: A decoded session object
    """
    try:
        cookie_data = base64.b64decode(cookie)
        cipher = AES.new(key=current_app.config['KEY'], mode=AES.MODE_CBC, iv=cookie_data[:16])
        cookie_data = pkcs7_unpad(cipher.decrypt(cookie_data[16:]))
        session = json.loads(cookie_data.decode('ascii', errors='replace'))
        if session.pop('q', None) != current_app.config['SUPER_SECRET_STRING']:
            raise SessionError("No Tampering!")
        return session
    except (json.JSONDecodeError, UnicodeError, binascii.Error, AttributeError):
        raise SessionError("Error parsing session")


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
        raise SessionError("Invalid Padding")
    elif not (0x00 < data[-1] <= blocksize):
        raise SessionError("Invalid Padding")
    elif any(data[-1-i] != data[-1] for i in range(data[-1])):
        raise SessionError("Invalid Padding")
    else:
        return data[:-data[-1]]


if __name__ == '__main__':
    app.run()
