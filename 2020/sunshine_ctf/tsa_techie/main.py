import requests

url = 'https://device-registration.web.2020.sunshinectf.org/udid/verify'

with open('phase2.xml', 'r') as f:
    s = f.read()

print(s)
r = requests.post(url)
print(r.text)
