## Ride

Points: 50

At first glance, it seems to be a huge list of floating point numbers. But upon
closer inspection is seems that the values between every other element only
seem to change slightly. Based on the context of the problem, these values seem
to be XY coordinates.

To take advantage of this, we can first reformat the file using a simple script:
```python
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
```

This formats the file like so:
```
39.9561702,-82.9998764
39.9561111,-82.9998112
39.9561122,-82.9995704
39.9561573,-82.9993301
...
```

Then we can load this value into Excel and plot it as a scatter plot.  The
resulting plot roughly resembles the `osuctf` prefix on the left, but is
somewhat indecipherable.  But you can actually flip the image vertically to get
a better view. After that, it becomes clear that the text says:
`osuctf{OUTSID3}`
