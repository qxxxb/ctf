# License Check

**Category**: [PEGASUS], reverse engineering \
**Author**: [kcolley](https://github.com/kjcolley7) \
**Points**: 200

I started working on this problem at 12 AM but unfortunately wasn't able to
solve it by 9 AM, which was when the CTF ended. Luckily I was eventually able
solve it after asking some questions on the CTF Discord.

For this problem, I started by running the executable:
```
 ./runpeg -p peg_rev_checker.so LicenseChecker.peg
Email: test
License key: 12345
Invalid email or license key.
```

Let's see what options we have here:
```
 ./runpeg -h
Usage: ./runpeg [-dfhptv] input1.peg {inputN.peg...}
Options:
    -h, --help      Show this help message
    -p, --plugin    [string] Path to a plugin library to load as a checker module
    -f, --function  [string] Resolve the named symbol and call it as a function
    -d, --debug     Enable the EAR debugger
    -t, --trace     Print every instruction as it runs
    -v, --verbose   Enable verbose mode for EAR emulator
```

Running it in debug mode gives me a gdb-like program where I can step through
instructions, set breakpoints, dump memory, and most importantly, disassemble
instructions.

After [annotating the assembly](../notes.md), I had this pseudocode:
```c
void main() {
    puts("Email: ");
    char email[30];
    gets(&email);

    // Note: The challenge author later pointed out to me that it's actually
    // strlen(email) <= 30

    if (strlen(email) != 30) exit(1);

    puts("License key: ");
    char license_key[30];
    gets(&license_key);
    if (strlen(license_key) != 30) exit(1);

    if (check_license_key(license_key) && check_email(email)) {
        print_flag();
    }
}
```

Ok, looks pretty simple on the surface.

After annotating and stepping through `check_license_key`, I got this
pseudocode:
```python
def check_license_key(key):
    n = 8
    i = 0
    j = 0

    while n != 0:
        n -= 1

        r5 = key[i] + 0x80
        i += 1

        # Use bitmask because we only care about the first byte
        r5 = (r5 - 235) & 0xff
        if r5 > 0xf:
            return False

        r6 = key[i] + 0x80
        i += 1

        r6 = r6 & 0x7f  # Take the first 7 bits
        r6 = (r6 - 0x41) & 0xff
        if r6 > 0xf:
            return False

        # Not sure why this is here yet, but it won't affect the next iteration
        r6 = r6 << 4
        r5 = r5 | r6

        key[j] = r5
        j += 1

    return True
```

So all we needed to do was satisfy `r5 <= 0xf` and `r6 <= 0xf` for the first 8
bytes of the license key.

As I stepped through the program again, I noticed that the hexdump of my license
key didn't seem to match the actual hex encoding of my text. For example, when I
entered `pancakes_dont_taste_bad_maybe` as my license key:

```
Expected:
fac4: 7061 6e63 616b 6573 5f64 6f6e 745f 7461
fad4: 7374 655f 6261 645f 6d61 7962 6500

Got:
fac4: f0e1 eee3 e1eb e5f3 dfe4 efee f4df f4e1
fad4: f3f4 e5df e2e1 e4df ede1 f9e2 6500
```

After some searching, I found these lines in  `gets`:
```asm
0115.0000: ORR     R6, 0x80 ; For some reason all inputs are OR'd with 0x80
0119.0000: STB     [RV], R6
```

The OR with 0x80 will set the highest bit of the byte for all inputs read using
this function. That also explains all the weird `AND ZERO RV, 0x80` checks
sprinkled throughought the code.

Knowing this, I was able to reverse the `check_license_key` function and produce
this license key that passed:
```
kAkAkAkAkAkAkAkAkAkAkAkAkAkAkA
```

Next I started reversing `check_email` but got stuck right at the start of the
function:
```asm
; Move R5 one index past the tail of `email`
017F.0000: LDB     RV, [R5]       ; RV = email[R5]
0181.0000: AND     ZERO, RV, 0x80 ; Make sure it's not 0x80
0186.0000: INC.NE  R5, 1          ; R5 += 1
0188.0000: BRR.NE  0xFFF4         ; Jump to 017f

...

; What the heck
0198.0000: LDB     RV, [R5]  ; RV = email[R5]
019A.0000: INC     R5, -1    ; R5 -= 1
019C.0000: SUB     RV, 0x72  ; if RV != 0x72: FAIL
01A0.0000: BRA.NE  RD, RA
```

I thought every byte read through `gets` would get OR'd with `0x80`. If that's
the case, then R5 should be pointing to one index past the tail of `email` in
no-mans land, making `[R5] == 0x00`. This means that the second block, which
requires `[R5] == 0x72`, would always fail.

I was stuck here for a few hours until I read through `gets` carefully again.
```asm
; if R5 == '\n':
;     [RV] = last_char
;     return
0107.0000: CMP     R5,  0xA
010B.0000: STB.EQ  [RV], R6
010D.0000: BRR.EQ  0x20
```

So if the last char is a newline character, then we just set the 2nd to last
character (without getting OR'd with `0x80`!) and return.

Going back to `check_email`, this means that `[R5]` will be pointing to the
character before the newline character since its highest bit isn't set. The
char corresponding to `0x72` is `r`, so that must be the character before the
newline.

After reversing the a few more lines, I had this potential email payload, where
the `\x00`s represented unknown characters:
```python
email = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xf0\xe5\xe7\xae\xe5\xe1r\n')
```

I managed to reach this point at 7:30 AM. I spent the next 1 and half hours
feverishly working on the final portion of the `check_email` function:
```asm
; R3 = &license_key[0]
; R4 = &email[0]
; R6 = &email[28]
01E8.0000: MOV     R5, R4      ; R5 = &email[0]
01EA.0000: MOV     R7, ZERO    ; R7 = 0
01EC.0000: AND     RV, R7, 0x7 ; RV = R7 & 0x7 (highest bit)
01F1.0000: ADD     RV, R3      ; RV += R3
01F3.0000: LDB     R4, [R5]    ; R4 = *R5
01F5.0000: LDB     TMP, [RV]   ; TMP = *RV
01F7.0000: ADD     TMP, R4     ; TMP += R4
01F9.0000: STB     [RV], TMP   ; *RV = TMP
01FB.0000: INC     R5, 1       ; R5++
01FD.0000: INC     R7, 1       ; R7++
01FF.0000: CMP     R5,  R6     ; if R5 > R6: break
0201.0000: BRR.LE  0xFFE8

; Check that the first 8 bytes of `license_key` are 0
0204.0000: MOV     RV, ZERO
0206.0000: MOV     R7, ZERO
0208.0000: ADD     R5, R3, R7
020B.0000: LDB     R5, [R5]
020D.0000: ORR     RV, R5
020F.0000: CMP     R7,  0x7
0213.0000: INC.LT  R7, 1
0215.0000: BRR.LT  0xFFF0 ; Jump to 0208
0218.0000: BRA     RD, RA ; RET
```

Unfortunately, by the time 9 AM rolled around, I wasn't able to make any
meaningful progress and the CTF ended.

One of the main things I got stuck on was that since my email payload now
contained non-printable characters, copy-pasting my payloads into the debugger
was no longer an option. There also didn't seem to be any mechanism for piping
input from a file into the debugger. Because of this, I tried to write some
Python to replicate the behavior of the two blocks so that I could do some
reversing from there. Unfortunately, due to several misread instructions and
programming errors, I wasn't able to get it to work.

After posting a few questions on the CTF Discord, I was told that I could use
pwntools to start the `runpeg` debugger, set breakpoints, send the payloads, and
go back to interactive mode. The challenge author also helped me fix a few
errors in my Python code.

I gave this challenge another shot a few days later and was finally able to
write a working Python script that emulated the first block of the
`check_email` function. I also found that using `bytearray` instead of a string
of raw bytes made it much easier to work with in Python.
```python
def scramble(stack):
    license = 0  # R3 = &license[0]
    email = 30  # R4 = &email[0]
    email_tail = 30 + 28  # R6 = &email[28]

    email_i = email  # R5
    license_i = 0  # R7
    while True:
        # license_i: 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, ...
        RV = license + (license_i & 0b111)

        # email[0], email[1], email[2], ... , email[28]
        email = stack[email_i]
        stack[RV] = (stack[RV] + email) & 0xff

        email_i += 1
        license_i += 1
        if email_i > email_tail:
            break
```

From the code, I was able to see that we basically iterated through `email` byte
by byte. For each byte, we added it to one of the first 8 bytes in the license
key. The goal was to ensure that all 8 bytes in the license key were zero, so I
decided to try an arbitrary payload, record the result, and try to tweak it so
that we could gets zeros in the first 8 bytes of the license key.

I chose the same payloads I used previously:
```python
email = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xf0\xe5\xe7\xae\xe5\xe1r\n')
license_key = b'kAkAkAkAkAkAkAkAkAkAkAkAkAkAkA'
```

This resulted in the following hexdump:
```xxd
fac4: 672e 6561 f2c0 f0e5 ebc1 ebc1 ebc1 ebc1  g.ea............
fad4: ebc1 ebc1 ebc1 ebc1 ebc1 ebc1 eb00 8080  ................
fae4: 8080 8080 8080 8080 8080 8080 8080 8080  ................
faf4: 8080 80c0 f0e5 e7ae e5e1 7200            ..........r.
```

The first 30 bytes were the license key, and the latter 30 bytes were the email.
Currently the first 8 bytes of the license key were: `672e 6561 f2c0 f0e5`

Focusing on the first byte, we can see that its value is `0x67`. We can set this
to zero by adding `0x99` because `0x67 + 0x99 = 0x100` and we only care about
the first byte: `0x00`.

Since the first byte of the email (currently `0x80`) is added to `0x67`, we can
increment it by `0x99` which gives us `0x80 + 0x99 = 0x119`. However, `0x119` is
too big to fit in one byte. To resolve this, we can split it across the first
and eighth bytes, which both get added to the first byte of the license key. So
we'll have:
```
email[0] = 0x80 + 0x7f = 0xff
email[7] = 0x80 + 0x1a = 0x9a
```

Notice that the highest bits of both bytes are 1, so there are no issues with
it being OR'd with `0x80` from `gets`.

Repeat this process for the first 8 bytes in the license key and we should be
good to go. Finally, after a solid 11 hours of work, I was able to solve this
challenge.

```python
import pwn
import sys


def parse_hexdump(hexdump):
    ans = bytearray()
    for line in hexdump.splitlines():
        tokens = line.split()
        tokens = tokens[1:-1]  # Discard first and last
        for token in tokens:
            # Iterate each token two chars at a time
            for i in range(0, len(token), 2):
                byte_str = token[i: i + 2]
                byte = int(byte_str, 16)
                ans.append(byte)
    return ans


def hexdump(stack, addr=0x0, addr_max_width=4):
    # Print 16 bytes per row
    for i in range(0, len(stack), 16):
        sub = stack[i: i + 16]

        pair_strs = []

        # Read 2 bytes at time
        for j in range(0, len(sub), 2):
            pair = sub[j: j + 2]
            pair_strs.append(pair.hex())

        s = " ".join(pair_strs)

        # Insert spaces every 4 characters
        addr_str = "{:x}".format(addr).rjust(addr_max_width, '0')
        print('{}: {}'.format(addr_str, s))
        addr += 16


def scramble(stack):
    license = 0  # R3 = &license[0]
    email = 30  # R4 = &email[0]
    email_tail = 30 + 28  # R6 = &email[28]

    email_i = email  # R5
    license_i = 0  # R7
    while True:
        # license_i: 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, ...
        RV = license + (license_i & 0b111)

        # email[0], email[1], email[2], ... , email[28]
        email = stack[email_i]
        stack[RV] = (stack[RV] + email) & 0xff

        email_i += 1
        license_i += 1
        if email_i > email_tail:
            break


def measure_diffs(stack):
    # Measure the differences required to make the first 8 bytes of the license
    # key zero
    ans = [0] * 8
    for i in range(0, 8):
        ans[i] = 0x100 - stack[i]
    return ans


def split_diffs(diffs):
    # Split the differences that exceed the size of one byte
    ans = []
    for i, diff in enumerate(diffs):
        fixes = []
        max_inc = 0xff - 0x80
        while (diff + 0x80) > 0xff:
            diff -= max_inc
            fixes.append(max_inc)
        fixes.append(diff)
        ans.append(fixes)

    return ans


def apply_diffs(email, fixes):
    # Apply the differences among the email bytes
    for i, fix in enumerate(fixes):
        for j, inc in enumerate(fix):
            email[i + (j * 8)] += inc


license = ([b'k'] + [b'A']) * 15
email = bytearray(30)
email[-1] = ord('\n')
email[-2] = ord('r')
email[-3] = 0xe1
email[-4] = 0xe5
email[-5] = 0xae
email[-6] = 0xe7
email[-7] = 0xe5
email[-8] = 0xf0
email[-9] = 0xc0

with open('dump', 'r') as f:
    s = f.read()
    stack = parse_hexdump(s)

    scramble(stack)
    print('Hexdump post-scramble:')
    hexdump(stack, addr=0xfac4)
    print()

    diffs = measure_diffs(stack)
    diffs = split_diffs(diffs)
    apply_diffs(email, diffs)

    print("New email:")
    hexdump(email)

if len(sys.argv) > 1:
    # Only do the IO stuff if we run with args (doesn't matter what).
    # This is so we can test the functions above without intializing pwntools
    # every time.

    if sys.argv[1] == 'r':
        # Run on remote
        p = pwn.remote('chal.2020.sunshinectf.org', port=10001)
    else:
        # Debug local process
        p = pwn.process(
            './runpeg -p peg_rev_checker.so LicenseChecker.peg -d',
            shell=True
        )

        p.recvuntil('EAR debugger')
        p.sendline('')
        p.recvuntil('(dbg) ')

        p.sendline('b 0x01E8')
        p.sendline('c')

    p.recvuntil('Email: ')
    p.send(email)

    p.recvuntil('License key: ')
    license = b''.join(license)
    p.send(license)

    if sys.argv[1] == 'r':
        print(p.recvall(timeout=2).decode())
    else:
        p.interactive()
```

Output:
```
 python3 main1.py r
Hexdump post-scramble:
fac4: 672e 6561 f2c0 f0e5 ebc1 ebc1 ebc1 ebc1
fad4: ebc1 ebc1 ebc1 ebc1 ebc1 ebc1 eb00 8080
fae4: 8080 8080 8080 8080 8080 8080 8080 8080
faf4: 8080 80c0 f0e5 e7ae e5e1 7200

New email:
0000: 7f7f 7f7f 0e40 101b 1a53 1c20 0000 0000
0010: 0000 0000 00c0 f0e5 e7ae e5e1 720a

[+] Opening connection to chal.2020.sunshinectf.org on port 10001: Done
[+] Receiving all data: Done (53B)
[*] Closed connection to chal.2020.sunshinectf.org port 10001
sun{wh47_15_7h15,_4RM_bu7_w17h_v4rl3n_1n57ruc710n5?}
```

---

## Additional notes:

I talked to the challenge author after posting this write-up and it turns out I
made this problem a lot more difficult than it probably should've been.

First of all, the emails and license keys only need to be *up to* 30
bytes, not exactly 30 bytes.

Secondly, if I had read the [PEGASUS.md](../PEGASUS.md) document more
carefully, I would've noticed that it described a type called `lestring` which
was exactly the format used by `gets()`.

Finally, the `LicenseChecker.peg` actually came with symbols so I could've been
able to see function names and other good stuff, which would've made
disassembling easier. This also would have allowed me to notice that the
`check_license_key` function is actually named `decode_b16` which does the
following:

> If you notice, it's overwriting bytes in the license key as it loops through.
> That function is effectively decoding a string from hexadecimal to bytes,
> except instead of using 0-9a-f for the hex characters I decided to use k-zA-P

[PEGASUS]: https://github.com/kjcolley7/PEGASUS
