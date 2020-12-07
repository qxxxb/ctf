from string import ascii_lowercase
from itertools import product
import gizeh
import numpy as np
import random

random.seed(1234)

alphabet = ascii_lowercase + "_"
bigrams = [''.join(bigram) for bigram in product(alphabet, repeat=2)]
random.shuffle(bigrams)

scale = 2
width = 512 * scale
height = 512 * scale


def draw(bs, name, theta_offset=0):
    surface = gizeh.Surface(width=width, height=height)

    r = width / 2 * 3/4
    offset = [width / 2, height / 2]
    theta_step = (2 * np.pi) / (len(bs))

    i = 0
    for theta in np.linspace(0, 2 * np.pi, len(bs) + 1)[:-1]:
        t = theta + (theta_offset * theta_step / 2)
        xy = [r * np.sin(t) + offset[0], r * np.cos(t) + offset[1]]
        text = gizeh.text(
            bs[i],
            fontfamily="monospace",
            fontsize=20 * scale,
            fill=(0, 0, 0),
            xy=xy,
            angle=0
        )
        text.draw(surface)
        i += 1

    surface.write_to_png("gen/" + name + ".png")


even = bigrams[:16]
even0 = [x for i, x in enumerate(even) if i % 2 == 0]
even1 = [x for i, x in enumerate(even) if i % 2 == 1]
bigrams = bigrams[16:]

draw(even, "even")
draw(even0, "even0")
draw(even1, "even1", theta_offset=1)

odd = bigrams[:15]
bigrams = bigrams[15:]

draw(odd, "odd")
