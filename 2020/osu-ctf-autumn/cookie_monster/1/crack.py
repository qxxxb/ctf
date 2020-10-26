import base64


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


if __name__ == '__main__':
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

    u = '我_xxxxxxxxxxxxxxx'
    cookies['fullpad'] = 'PWcy62SAOrsP5g6T3NFrE0ZkqLs0DTmDwwwpyQuQqMKHcnoJvwNYEQ6loImPxfrbcHeHlz/WN/Bwz+p0sC7ojg=='

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
    ans = base64.b64encode(ans).decode()

    print()
    print(ans)
