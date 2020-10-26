import json

username = 'fart":"shiti}'

session = {
    'name': username,
    'role': 'users'
}

sj = json.dumps(session, separators=(',', ':'), sort_keys=True).encode('ascii', errors='replace')
print(sj)
