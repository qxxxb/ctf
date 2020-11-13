b 0x294
aaaabaaacaaadaaaeaaafaaagaaahaAAAABAAACAAADAAAEAAAFAAAGAAAHA
zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁkÁ
zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzkAkAkAkAkAkAkAkAkAkAkAkAkAkAkA

Finally the license key works!
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrkAkAkAkAkAkAkAkAkAkAkAkAkAkAkA

rrrrrrrrrrrrrrrrrrrrrrrrrrrrr
pancakes_dont_taste_bad_maybe
rrrrrrrrrrrrrrrrrrrrrrrrrråár
kAkAkAkAkAkAkAkAkAkAkAkAkAkAkA

hexdump r 0xfae2 30

ord('A') - 0xC1 = -128
ord('1') - 0xB1 = -128
ord('1') + 128 = 0xb1

We need
ord(x) + 128 > 235
ord(x) > 235 - 128
x > chr(235 - 128)

AAAABAAACAAADAAAEAAAFAAAGAAAHA

cm = c | 0x80
r6 = cm & 0x7f
r6 = r6 - 0x41

- How did the null byte get set in recv_str?
	- Answer: It is initialized with null bytes
- Can we abuse BRA, RD, DC, RV to return where we want?
	- Write 0x80 in the email

- recv_str has an error with newline: 1 byte can bypass the 0x80 OR
- But using this makes the length 29 instead of 30
- What about the OR stuff from check_license_key?

0xfae2 + 30 == 0xfb00

0000-0100: R=00 W=00 X=00 fault=0000
0100-0300: R=12 W=00 X=12 fault=0000
0300-EA00: R=00 W=00 X=00 fault=0000
EA00-EB00: R=00 W=00 X=00 fault=F000
EB00-FB00: R=02 W=02 X=00 fault=0000
FB00-FC00: R=00 W=00 X=00 fault=FB00
FC00-FFFF: R=FC W=FC X=00 fault=0000

0xfb00 is right at the start of a new page
Also, why is FB00 set as the fault handler?
