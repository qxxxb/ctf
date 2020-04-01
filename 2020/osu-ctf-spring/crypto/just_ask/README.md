# Just Ask

**Points**: 200

```
FTZDNBQPAGUESTQBNAAQNGNWDWDNMHCQNXOAEQSTFTZDDLNUEABUGAPIUESTQBNAMTPNOAAGDNDWDNMTXQMZ
```

This will be tough so here are a couple hints and tips. This is a Playfair
cipher, meaning good luck trying to find an online solver for this without the
key but you can utilize [this][solver] for faster decryption. I’ve given you a
hint within the title that can help you figure out the keyword and I’ve omitted
J.  The plaintext is the flag.

Hint 1. Somewhere in the flag (a fool)

Hint 2. The start of the flag (he who)

Note: flag is just the plaintext, there is no osuctf{...}. the flag also
contains spaces.

Note: the flag is case insensitive, don't bother entering
multiple variations of the same case

Problem by: Anna Yu

## Solution

The title and hints reminded me of a famous quote, so I googled `he who ask
fool`. I found this quote from [goodreads][quote]:

> The man who asks a question is a fool for a minute, the man who does not ask
> is a fool for life.

I tried a few variations of this but it didn't work. Looks like I had to solve
the cipher after all. Using the suggested [Playfair cipher solver][solver], I
eventually guessed that the cipher key was `question`, which gave me the
following plaintext:
```
HEWHOASKSAQUESTIONISAFOXOLFORFIVEMINUTESHEWHODOESNOTASKAQUESTIONREMAINSAFOOLFOREVERX
```

Because the Playfair cipher requires pairs of letters without duplicates, the
`X` characters were placeholders that needed to removed. After adding the
appropriate spaces, the flag was:

```
HE WHO ASKS A QUESTION IS A FOOL FOR FIVE MINUTES HE WHO DOES NOT ASK A QUESTION REMAINS A FOOL FOREVER
```

[solver]: https://testproject1-1210.appspot.com/playfair
[quote]: https://www.goodreads.com/quotes/184310-the-man-who-asks-a-question-is-a-fool-for
