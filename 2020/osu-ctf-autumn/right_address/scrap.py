def filler(n, start):
    step = 0x11
    max_steps = 8

    x = start
    n_steps = 0

    for i in range(n):
        yield x.to_bytes(1, byteorder='big')

        n_steps += 1
        if n_steps == max_steps:
            n_steps = 0
            x = start
        else:
            x += step
