import base64

cookies = {}

u = 'xxxxxxx'
cookies['name'] = 'gLeo7iVSypsn/drBfy3RbNqzjyybmzeMf7kRLIBfjMOw5q6quh7obDIhswwefiJ/'

u = '我_xxxxxx'
cookies['name_to_role'] = 'PWcy62SAOrsP5g6T3NFrE30kGeiwGNdQMVb1PUmSSIuUUEeu2MALDRwSEM/HUPvE'

u = '我_administrators'
cookies['admins'] = 'PWcy62SAOrsP5g6T3NFrE7D7rtDFzVt3hvNeWiz0otGzyCGGy/RtajYLllJgyL40'

u = '我"zzzzzzzzzzzzzzz'
cookies['zzz'] = 'U2l/OSWmJxArnhzkfE7elbHB6v0jFqSd7KzxFzedWXras48sm5s3jH+5ESyAX4zDsOauqroe6GwyIbMMHn4ifw=='

u = '我":              '
cookies['quote_colon'] = 'U2l/OSWmJxArnhzkfE7elVllHkQOfGWG7yCYJzrclBfas48sm5s3jH+5ESyAX4zDsOauqroe6GwyIbMMHn4ifw=='

u = '我"               '
cookies['quote'] = 'U2l/OSWmJxArnhzkfE7elT4irMNU1cVFIEzx4Mm5Y9Tas48sm5s3jH+5ESyAX4zDsOauqroe6GwyIbMMHn4ifw=='

u = '我_}               '
cookies['closing_bracket'] = 'PWcy62SAOrsP5g6T3NFrE3fvkbcAz1yplNd9r2En5wvas48sm5s3jH+5ESyAX4zDsOauqroe6GwyIbMMHn4ifw=='

for name, value in cookies:
    cookies[name] = base64.b64decode(value)

print(cookies)
