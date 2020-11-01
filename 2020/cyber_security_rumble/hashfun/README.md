# Hashfun

Points: 100

This is a weird XOR cipher. If we didn't know anything about the flag, then this
would probably be unsolvable. However, we do know that the flag starts with
`CSR{`. This allows us to reverse the hash algorithm.

```python
def revhash(cipher):
    msg_len = len(c) + 4
    msg = ["."] * (msg_len + 1)
    msg[0:5] = "CSR{"

    ascii_start = ord(' ')
    ascii_end = ord('~')

    i = 4

    while i < msg_len:
        prev_msg_char = msg[i - 4]
        prev_msg_char_i = ord(prev_msg_char)
        prev_cipher_char_i = cipher[i - 4]

        found = False
        for guess_char_i in range(ascii_start, ascii_end + 1):
            if guess_char_i ^ prev_msg_char_i == prev_cipher_char_i:
                cur_char = chr(guess_char_i)
                print(cur_char)
                msg[i] = cur_char
                i += 1
                found = True
                break

        if not found:
            print("Couldn't find char")
            break

    print(msg)
    return "".join(msg)
```
