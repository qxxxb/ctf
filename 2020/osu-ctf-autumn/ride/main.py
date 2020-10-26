with open('ride.txt') as f:
    with open('ride_col.txt', 'w') as fout:
        is_x = True
        for l in f.readlines():
            fout.write(l.strip())
            if is_x:
                fout.write(",")
            else:
                fout.write("\n")

            is_x ^= 1
