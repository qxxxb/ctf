from flask import Flask, render_template, request, redirect, url_for, current_app, send_file
import os
import json
import base64
import binascii
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__,
            static_url_path='',
            template_folder="templates",
            static_folder="static")
app.config['NAME'] = "CookieMonster Pt. 0"
app.config['FLAG'] = os.environ['PART_ZERO_FLAG']
app.config['COOKIE_ID'] = 'SESSIONID0'


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
    Creates a new session cookie with the given username
    :param username: The username to create the session with
    :return: The encrypted and b64 encoded cookie
    """
    if 5 <= len(username) <= 20:
        session = {
            'name': username,
            'role': 'users'
        }
        cookie_data = json.dumps(session, separators=(',', ':'), sort_keys=True).encode('ascii', errors='replace')
        return base64.b64encode(cookie_data)
    else:
        raise SessionError("Username must be 5 to 20 characters")


def get_session(cookie: str) -> dict:
    """
    Parses a session cookie
    :param cookie: The base64 encoded cookie string
    :return: A decoded session object
    """
    try:
        return json.loads(base64.b64decode(cookie))
    except (json.JSONDecodeError, UnicodeError, binascii.Error, AttributeError, Exception):
        raise SessionError("Error parsing session")


if __name__ == '__main__':
    app.run()
