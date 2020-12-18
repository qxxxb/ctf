# Santa's ELF holomorphing machine

**Category**: Programming \
**Points**: 424 \
**Author**: PinkiePie1189

## Challenge

We have intercepted the blueprints and a memory dump for another of Santa's
wicked contraptions. What is the old man hiding this time around?

File: `blueprint.pdf`
File: `data.txt`

## Solution

Basically we have 802 complex numbers from `data.txt`. We calculate
```
# z is complex number from data.txt
Let u(x, y): R -> R
Let v(x, y): R -> R
Let f(z) = u(Re(z), Im(z)) + v(Re(z), Im(z))
Let zm = f(z)
plot(Re(zm), Im(zm))
```

Our goal is to get the entire plot.
However, for each row, we only have `z` and either `u` or `v` but not both.
How can we find `u` given `v` and vice versa?

Since `f(z)` is a holomorphic function, it satisfies the Cauchy-Riemann equations:
```
du/dx = dv/dy
du/dy = -dv/dx
```

By looking at `data.txt`, `u` and `v` are both linear functions. This means
that we can fully recover `u` and `v` for every row.

```python
if is_u:
    a, b = int(left), int(right)
    c = -b
    d = a
else:
    c, d = int(left), int(right)
    a = d
    b = -c

u = a*x + b*y
v = c*x + d*y
```

Full script in `solve.py`

![](p.png)
