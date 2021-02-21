import sys
import numpy as np
from heapq import heappush, heappop
from PIL import Image, ImageDraw, ImageFont


def all_square_pixels(row, col, square_h, square_w):
    # Every pixel for a single "square" (superpixel)
    # Note that different squares might have different dimensions in order to
    # not have extra pixels at the edge not in a square. Hence: int(round())
    for y in range(row * square_h, (row + 1) * square_h):
        for x in range(col * square_w, (col + 1) * square_w):
            yield y, x


def make_one_square(img, row, col, square_h, square_w):
    # Sets all the pixels in img for the square given by (row, col) to that
    # square's average color
    pixels = []

    # get all pixels
    for y, x in all_square_pixels(row, col, square_h, square_w):
        pixels.append(img[y][x])

    reds = np.array([p[0] for p in pixels])
    greens = np.array([p[1] for p in pixels])
    blues = np.array([p[2] for p in pixels])

    av_r =  np.average(reds)
    av_g =  np.average(greens)
    av_b =  np.average(blues)

    # set all pixels to that average color
    for y, x in all_square_pixels(row, col, square_h, square_w):
        img[y][x] = (av_r, av_g, av_b)


def pixelate(img, square_w, square_h):
    square_w = 5
    square_h = 5
    num_rows = img.shape[0] // square_w
    num_cols = img.shape[1] // square_h

    for row in range(num_rows):
        for col in range(num_cols):
            make_one_square(img, row, col, square_h, square_w)

    return img


def is_blank(line):
    # Only sample the middle row
    nrows = line.shape[0]
    half = nrows // 2
    rows = line[half : half + 1]
    rows = rows.flatten()
    return all(x == 255 for x in rows)


def split_lines(img):
    top_offset = 88
    bottom_offset = 44
    line_height = 26

    img = img[top_offset:-bottom_offset, ...]
    assert img.shape[0] % line_height == 0

    for i in range(0, img.shape[0], line_height):
        line = img[i: i + line_height]
        line = line[:, :612, :]  # Remove blank stuff to the right
        if is_blank(line):
            print("Detected blank line, exiting")
            break

        yield line


def prep_line(line):
    """Prep for pixelation"""
    hwhite = line[0:1]
    hpad = np.tile(hwhite, (13, 1, 1))
    line = np.vstack([hpad, line, hpad])

    vwhite = line[:, 0:1, :]
    vpad = np.tile(vwhite, (1, 3, 1))
    line = np.hstack([vpad, line, vpad])

    return line


def trim_pline(line):
    # It actuall should be 595
    return line[20:40, 10:610, :]


def compare_flag(line):
    def trim_to_match(small, big):
        if small.shape[1] <= big.shape[1]:
            return small, big[:, :small.shape[1], :]
        else:
            x, y = trim_to_match(big, small)
            return y, x

    offset = 5
    line = line[:, offset:, :]
    exp = flag
    line, exp = trim_to_match(line, exp)
    assert exp.shape == line.shape

    line = line.astype(int)
    exp = exp.astype(int)
    diff = line - exp
    diff = np.abs(diff)
    diff = np.clip(diff, 0, 255)
    diff = diff.astype(np.uint8)

    # diff_img = Image.fromarray(diff)
    # diff_img.show()
    diff = np.sum(diff)
    print(diff)
    return diff

"""
Size: 1473x145
x offset: 11
y offset: 50
"""

# img = Image.new("RGBA", (500, 50), (255, 255, 255, 255))
# fnt = ImageFont.truetype("consola.ttf", 16)
# d = ImageDraw.Draw(img)
# d.text((10, 10), "union{https://www.youtube.com/watch?v=Yxxxxxxxxxx}", font=fnt, fill=(0, 0, 0, 255))

flag = Image.open("imagec.png")
flag = np.array(flag)

img = Image.open("ss.png")
img = np.array(img)

pxlines = None
hdiffs = []

lines = split_lines(img)
for i, line in enumerate(lines):
    print(f"Line {i}")
    line = prep_line(line)

    x = 5
    line = pixelate(line, x, x)
    line = trim_pline(line)
    # print(line.shape)

    diff = compare_flag(line)
    heappush(hdiffs, (diff, i))

    if pxlines is None:
        pxlines = line
    else:
        pxlines = np.vstack([pxlines, line])

    # line_img = Image.fromarray(line)
    # fn = f"vars/{i}.png"
    # print(f"Saving {fn}")
    # line_img.show()
    # line_img.save(fn)

diffs = [heappop(hdiffs) for i in range(len(hdiffs))]
print("Diffs")
print(diffs)

pxlines_img = Image.fromarray(pxlines)
pxlines_img.show()
pxlines_img.save("vars.png")

s = open("guess.txt").read().strip()
cs = [s[i] for diff, i in diffs]
cs = "".join(cs)
print(cs)
