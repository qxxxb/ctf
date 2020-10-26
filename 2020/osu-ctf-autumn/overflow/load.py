c1 = "1234567890123456"
c3 = "\xbe\xba\xfe\xca"

load = c1 + c3

with open('load', 'w') as load_file:
    load_file.write(load)
