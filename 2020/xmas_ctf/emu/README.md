# EMU 1.0

**Category**: Emulation \
**Points**: 462 \
**Author**: trupples

## Challenge

Solved with NOT_MASTER08.

The EMU 1.0 digitisation project, lead in 2005 by Tahlia E., aimed to
immortalise the almost forgotten EMU 1.0 architecture's program collection.
They did not fully succeed, and all their work fell to obscurity, but a naughty
elf got their hands on Tahlia's manual and a few of her programs. The current
issue is they can't find a working EMU 1.0 machine to actually run the
programs. Figure out how the computer worked and get the code running!

**Hint!** Don't get bogged down with the described details! You only need to
emulate the overall behaviour of the instructions, not necessarily imitate
their exact implementation. High-level emulation works as well.

## Solution

We are given `mandelbrot.rom` and a manual explaining how to build an emulator
to run it.

After building the [emulator](https://github.com/qxxxb/emu/), I tried to run the ROM.

```
$ ~/Downloads/pypy3.7-v7.3.3-linux64/bin/pypy3 emu.py roms/mandelflag.rom
pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
Hello from the pygame community. https://www.pygame.org/contribute.html
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
........................................................................,,,,,,,,,,,.............................................
................................................................,,,,,,,,,,,,,,,,,,,,,,,,,,......................................
...........................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.................................
.......................................................,,,,,,,,,,,,,,,,,,,,,---,,,,,,,,,,,,,,,,,,,..............................
....................................................,,,,,,,,,,,,,,,,,,,,,,,,--~--,,,,,,,,,,,,,,,,,,,............................
.................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,--##------,,,,,,,,,,,,,,,,..........................
..............................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,----~#-~##--,,,,,,,,,,,,,,,,,........................
...........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#~-----,,,,,,,,,,,,,,,,,,......................
........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---#--#####~----,,,,,,,,,,,,,,,,,,,,....................
.....................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###########~#~---,,,,,,,,,,,,,,,,,,,...................
...................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~###########~----,,,,,,,,,,,,,,,,,,,..................
................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----------#############------,,,,,,,,,,,,,,,,,,.................
.............................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----~----------~###########~---------------,,,,,,,,,,................
..........................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###~~---#####################~###--------#--,,,,,,,,,...............
......................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---##################################~~-~##~~###,,,,,,,,,,..............
...................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~##########################################-,,,,,,,,,,,.............
...............,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,--------~#########################################--,,,,,,,,,,,,............
...........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~############################################~----,,,,,,,,,,,,...........
........,,,,,,,,,,,,,,,,,,,,,---------------------------~#############################################----,,,,,,,,,,,...........
.....,,,,,,,,,,,,,,,,,,,,,,,,--~#--------#~------------##################################################~-,,,,,,,,,,,..........
...,,,,,,,,,,,,,,,,,,,,,,,,,,---#~#~#---~###~-#-------~##################################################--,,,,,,,,,,,..........
..,,,,,,,,,,,,,,,,,,,,,,,,,------~###############~---~#################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#################~~####################################################-,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,-------~#######################################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,----~----~#########################################################################-,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,--------~############################################################################---,,,,,,,,,,,,,,,........
,,,,,,,---------------#-~###########################################################################~---,,,,,,,,,,,,,,,,........
##################################################################################################~-----,,,,,,,,,,,,,,,,........
,,,,,,,---------------#-~###########################################################################~---,,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,--------~############################################################################---,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,,,,,----~----~#########################################################################-,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,,,,,,,,-------~#######################################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#################~~####################################################-,,,,,,,,,,,,,.........
..,,,,,,,,,,,,,,,,,,,,,,,,,------~###############~---~#################################################---,,,,,,,,,,,,,.........
...,,,,,,,,,,,,,,,,,,,,,,,,,,---#~#~#---~###~-#-------~##################################################--,,,,,,,,,,,..........
.....,,,,,,,,,,,,,,,,,,,,,,,,--~#--------#~------------##################################################~-,,,,,,,,,,,..........
........,,,,,,,,,,,,,,,,,,,,,---------------------------~#############################################----,,,,,,,,,,,...........
...........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~############################################~----,,,,,,,,,,,,...........
...............,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,--------~#########################################--,,,,,,,,,,,,............
...................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~##########################################-,,,,,,,,,,,.............
......................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---##################################~~-~##~~###,,,,,,,,,,..............
..........................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###~~---#####################~###--------#--,,,,,,,,,...............
.............................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----~----------~###########~---------------,,,,,,,,,,................
................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----------#############------,,,,,,,,,,,,,,,,,,.................
...................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~###########~----,,,,,,,,,,,,,,,,,,,..................
.....................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###########~#~---,,,,,,,,,,,,,,,,,,,...................
........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---#--#####~----,,,,,,,,,,,,,,,,,,,,....................
...........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#~-----,,,,,,,,,,,,,,,,,,......................
..............................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,----~#-~##--,,,,,,,,,,,,,,,,,........................
.................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,--##------,,,,,,,,,,,,,,,,..........................
....................................................,,,,,,,,,,,,,,,,,,,,,,,,--~--,,,,,,,,,,,,,,,,,,,............................
.......................................................,,,,,,,,,,,,,,,,,,,,,---,,,,,,,,,,,,,,,,,,,..............................
...........................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.................................
................................................................,,,,,,,,,,,,,,,,,,,,,,,,,,......................................
........................................................................,,,,,,,,,,,.............................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
HEY
HEY KID
WANT SUM...FLAG?
> MAYBE
_3CP Z.G#7$[G[ND5~N#VEEHNI|Y
```

After the mandelbrot is printed, I'm prompted for input.
I didn't know what to type, so I wrote `MAYBE`.
Apparently that was not the correct response, because I got some garbage
printed back.
Looks like some kind XOR or ROT cipher.

Taking a look at the disassembly we see this:
```asm
0257:   LBL    1537, 0
0258:   IO     r1, SERIAL_INCOMING, r0
0259:   CMPUG  r1, 3
0260: - JUP    1537, r0
0261:   IO     r60, SERIAL_READ, r0
0262:   IO     r61, SERIAL_READ, r0
0263:   IO     r0, SERIAL_READ, r0
0264:   IO     r0, SERIAL_READ, r0
```

The `SERIAL_INCOMING` device returns the number characters that can be read.
We can see that it loops until more than 3 characters are buffered.
Then it reads the first two characters and discards the next two.

Since only two characters are used, we can just bruteforce all possible bigrams
instead of reversing the encryption.

To do this, I saved the machine state using Python `pickle` after the mandelbrot
was printed. Then in a separate script, I repeatedly loaded the saved state
back and tried different inputs until the output contained `X-MAS`, the flag
prefix.

```python
with open('emu_state.pkl', 'rb') as f:
    emu = pickle.load(f)

for bigram in itertools.product(serial_dict, repeat=2):
    payload = ''.join(bigram) + 'AA'
    m = copy.deepcopy(emu)
    m.out = io.StringIO()
    m.buffer = payload
    m.run()
    output = m.out.getvalue()
    print('{}: {}'.format(payload, output))
```

Eventually it found it:
```
...
Y{AA: ^AG$*=$MD[/G/ND5~N#VE4+HRX-
Y}AA: }M8OW(V56IN1G1ND5~N#VEB4JJ#)
Y#AA: X-MAS{EMU~L3G3ND5~N#VER_D1E}
```

# Talkative

**Category**: Emulation \
**Points**: 490 \
**Author**: trupples

## Challenge

Now that you have an EMU 1.0 emulator, go make a network card and come chat
with us! \ \
P.S. you don't need to implement the server card to get the flag

Target: `nc challs.xmas.htsp.ro 5100`

**Hint!** While you don't need to implement a server network card, to get the
flag you still need to understand what the server does to your messages.

## Solution

I disassembled `talkative-server-redacted.rom` and annotated it:
```asm
000:   ADDI   r12, r0, 61
001:   ADDI   r13, r0, 36
002:   LBL    512, 0
003:   ADDI   r1, r0, 2
004:   IO     r0, ENET_CONN_CTRL, r1
005:   IO     r1, ENET_INCOMING, r0
006:   CMPUL  r1, 40
007: + JUP    512, r0 # If we have less than 40 chars, keep reading

008:   ADDI   r50, r0, 62 # Store the first 4 chars (username?)
009:   IO     r8, ENET_RECV, r0
010:   IO     r9, ENET_RECV, r0
011:   IO     r10, ENET_RECV, r0
012:   IO     r11, ENET_RECV, r0
013:   ADDI   r2, r0, 14

# Recv payload to registers r14 to r50 (exclusive)
014:   LBL    513, 0
015:   IO     r1, ENET_RECV, r0
016:   ST     [r2+0], r1
017:   ADDI   r2, r2, 1
018:   CMPUL  r2, 50

# Print to username and payload
020:   ADDI   r2, r0, 8
021:   LBL    513, 0
022:   LD     r1, [r2+0]
023:   IO     r0, SERIAL_WRITE, r1
024:   ADDI   r2, r2, 1
025:   CMPUL  r2, 51
026: + JUP    513, r0

027:   CMPEQ  r0, r0
028: + CMPEQ  r24, 36 # Must pass all these checks
029: + CMPEQ  r21, 36
030: + CMPEQ  r40, 10
031: + CMPEQ  r45, 21
032: + CMPEQ  r11, 28
033: + CMPEQ  r27, 29
034: + CMPEQ  r23, 14
035: + CMPEQ  r39, 22
036: + CMPEQ  r34, 10
037: + CMPEQ  r29, 14
038: + CMPEQ  r14, 18
039: + CMPEQ  r35, 23
040: + CMPEQ  r43, 21
041: + CMPEQ  r9, 22
042: + CMPEQ  r8, 34
043: + CMPEQ  r17, 18
044: + CMPEQ  r18, 16
045: + CMPEQ  r36, 36
046: + CMPEQ  r47, 21
047: + CMPEQ  r20, 29
048: + CMPEQ  r44, 24
049: + CMPEQ  r16, 22
050: + CMPEQ  r15, 36
051: + CMPEQ  r22, 11
052: + CMPEQ  r38, 38
053: + CMPEQ  r48, 24
054: + CMPEQ  r26, 14
055: + CMPEQ  r49, 21
056: + CMPEQ  r37, 33
057: + CMPEQ  r46, 24
058: + CMPEQ  r32, 29
059: + CMPEQ  r25, 11
060: + CMPEQ  r41, 28
061: + CMPEQ  r19, 17
062: + CMPEQ  r33, 17
063: + CMPEQ  r31, 36
064: + CMPEQ  r28, 29
065: + CMPEQ  r10, 10
066: + CMPEQ  r42, 36
067: + CMPEQ  r30, 27
068: + JDN    4095, r0 # Jump to flag
...
```

The important parts are the `CMPEQ` instructions from `028` to `067`.
The get the flag we just need a payload to pass those checks.

I wrote a [script](https://github.com/qxxxb/emu/blob/master/talkative.py) to
automate this. This was the correct payload
```
USERNAME: YMAS
PAYLOAD: I MIGHT BE BETTER THAN X-MAS LOLOLOL
```

# GAMEBREAK + Demo Party

**Category**: Emulation \
**Points**: 500 \
**Author**: trupples, Milkdrop

## Challenge

The greatest step towards the popularization of the EMU 1.0 was its entry into
the home entertainment market, starting with the release of the Pluton
GAMEBREAK extension. We don't have much to go on but a crumpled up reference
card from a developer, a picture of a retail box, a ROM that supposedly uses
the graphics and memory extensions, and a reconstructed picture of what it
should display.

The external memory seemed to have had 256k slots which are 18-bit addresable.
The old screens are 64x64 with 6 bit color (2 bits per channel), and the
Joysticks have an 8-direction stick and two buttons (X, Y).

Implement the GAMEBREAK devices and make a nice demo to get some points!

## Solution

After implementing the MEM, GPU, and D-PAD devices, I was able to run
`win.rom`:

![](win.png)

The next challenge was to create my own ROM.

I like Nyan Cat, so went to [www.nyan.cat](http://www.nyan.cat/) and
got an Xmas Nyan.
Next I scaled it down to fit inside the 64x64 window and then split in into
frames.
```
convert -coalesce xmas_small.gif f.png
```

I wrote a script to read the pixels from each frame. The idea was to hard-code
each pixel into the tape and store the entire animation in the memory unit.

It ended up looking something like this:
```python
def mem_write_imm(i):
    return [
        Ins.from_values(Op.ADDI, Cond.UN, 1, 0, i),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_WRITE, 1),
    ]

tape = []
for f in frames:
    for row in f:
        for px in row:
            c = unscale_color(px)  # EMU uses 64-bit color
            tape += mem_write_imm(c)
```

To draw a row, I wrote this function:
```python
def draw_row():
    color = temp_reg()
    x = temp_reg()  # gpu_x + offset
    (la, lb) = new_label()

    return [
        # Loop through GPU X from 0..width
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),

        # offset = 14
        Ins.from_values(Op.ADDI, Cond.UN, x, rs['gpu_x'], 14),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_X, x),

        # Get pixel color from frames stored in memory unit
        Ins.from_io(Cond.UN, color, IoDevice.MEM_READ, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_DRAW, color),

        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], rs['gpu_x'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_x'], width),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),
    ]
```

To draw a frame, I could just re-use the `draw_row` function but increment
`GPU_Y` on each iteration.
```python
def draw_frame():
    ans = []

    y = temp_reg()  # gpu_y + offset
    (la, lb) = new_label()

    ans += [
        # Loop through GPU Y from 0..height
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),

        Ins.from_values(Op.ADDI, Cond.UN, y, rs['gpu_y'], 18),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_Y, y),
    ]

    ans += draw_row()

    ans += [
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], rs['gpu_y'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_y'], height),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),
    ]

    return ans
```

Finally, to draw the animation frame-by-frame, I could re-use the `draw_frame`
function.

```python
def draw_frames():
    ans = []
    (la, lb) = new_label()
    wait = new_label()
    cl = temp_reg()  # Clock reset

    ans += [
        # Loop frame index from 0..n_frames
        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),
    ]

    ans += draw_frame()

    ans += [
        # Reset clock to draw frame.
        # The screen is updated when the clock is reset.
        Ins.from_values(Op.ADDI, Cond.UN, cl, 0, 1),
        Ins.from_io(Cond.UN, 0, IoDevice.CLOCK_LO_CS, cl),

        # Wait 0.08 seconds before drawing next frame
        Ins.from_values(Op.LBL, Cond.UN, wait[0], wait[1], 0),
        Ins.from_io(Cond.UN, cl, IoDevice.CLOCK_LO_CS, 0),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.UL, cl, 8),
        Ins.from_values(Op.JUP, Cond.TR, wait[0], wait[1], 0),

        # Next frame
        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], rs['frame_i'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['frame_i'], n_frames),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),

        # Loop the animation

        # Set frame index to 0
        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], 0, 0),

        # Reset memory pointer
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_HI, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_MID, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_LO, 0),

        Ins.from_values(Op.JUP, Cond.UN, la, lb, 0),
    ]

    return ans
```

The full script is [here](https://github.com/qxxxb/emu/blob/master/nyan.py).
This is the final output:

![](https://raw.githubusercontent.com/qxxxb/emu/master/imgs/output.gif)
