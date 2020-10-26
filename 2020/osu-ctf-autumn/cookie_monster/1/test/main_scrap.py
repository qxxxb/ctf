# plaintext = '{"name":"12345","role":"users"}'

# for i in range(5, 20 + 1):
#     u = '😀' * i
#     cookie = create_session(u)
#     session = get_session(cookie)
#     # print(session)
#     print()

# u = "我_administrators\\\"}"

u = 'xxxxxxx'
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我_xxxxxx'
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我_administrators'
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我"zzzzzzzzzzzzzzz'
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我":              '
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我"               '
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我_}               '
cookie = create_session(u)
session = get_session(cookie)
print()

u = '我_xxxxxxxxxxxxxxx'
cookie = create_session(u)
session = get_session(cookie)
print()

# u = '我"x'
# cookie = create_session(u)
# session = get_session(cookie)
# print(session)

s = \
    '{"name":"xxxxxxx' + \
    'xxxxxx","role":"' + \
    'administrators",' + \
    '"zzzzzzzzzzzzzzz' + \
    '":              ' + \
    '"               ' + \
    '"               ' + \
    '}               ';
