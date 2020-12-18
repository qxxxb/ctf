import matplotlib.pyplot as plt
import numpy as np
import re

us = []
vs = []
with open('data.txt') as f:
    for line in f:
        s = line.split('; ')
        x, y = re.search(r'z = (.*) \+ (.*) \* i', s[1]).groups()
        x, y = float(x), float(y)

        left, right = re.search(r'. = (.*) \* x \+ (.*) \* y', s[0]).groups()
        is_u = s[0][0] == 'u'
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
        us.append(u)
        vs.append(-v)

plt.scatter(us, vs, cmap='viridis', c=np.arange(len(us)))
plt.show()
