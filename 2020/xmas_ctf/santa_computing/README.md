# Santa Computing

**Category**: Hardware \
**Points**: 388 \
**Author**: Milkdrop

## Challenge

Santa is still using that old hunk as his main computer huh? He keeps bragging
about how his laughably outdated hardware and software is immune to all these
fancy new modern vulnerabilities. While that might be true, someone please tell
him that speed might be a security issue as well...

Target: `nc challs.xmas.htsp.ro 5051`

## Solution

```
$ nc challs.xmas.htsp.ro 5051

     _________
    / ======= \
   / __________\
  | ___________ |
  | | -       | |
  | |         | |
  | |_________| |_________
  \=____________/         )
  / """"""""""" \        /
 / ::::::::::::: \   /T\'
(_________________)  \_/

HELLO SANTA.
PLEASE INPUT PASSWORD:
this is a guess
CHECKING... PLEASE WAIT.
PASSWORD REJECTED.
```

I connected to the server and was immediately prompted for a password. I tried
`this is a guess` and was rejected.

Based on the challenge description, this seems like a timing-related
side-channel attack.

We can guess that the server uses insecure string comparison like this:
```c
bool insecureStringCompare(const void *a, const void *b, size_t length) {
  const char *ca = a, *cb = b;
  for (size_t i = 0; i < length; i++)
    if (ca[i] != cb[i])
      return false;
  return true;
}
```

As soon as it reads an incorrect character, it aborts.

We know that flags start with `X-MAS` so let's try that

```
$ nc challs.xmas.htsp.ro 5051

     _________
    / ======= \
   / __________\
  | ___________ |
  | | -       | |
  | |         | |
  | |_________| |_________
  \=____________/         )
  / """"""""""" \        /
 / ::::::::::::: \   /T\'
(_________________)  \_/

HELLO SANTA.
PLEASE INPUT PASSWORD:
X-MAS
CHECKING... PLEASE WAIT.

~ took 3s
$
```

This time it closed the connection after three seconds.
Also, it didn't print `PASSWORD REJECTED`, which makes our exploit even easier.
Basically, the idea is to bruteforce each character one-by-one.
- If it says `PASSWORD REJECTED` then we know it's incorrect.
- If it doesn't say `PASSWORD REJECTED` and closes the connection instead, we
  know it's correct
- As the password gets longer, so does the response time

I wrote a script in `solve.py` to find the flag, which took around 15 minutes.
```
X-MAS{S1D3CH4NN3LZ?wtf!!}
```
