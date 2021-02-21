# committee

**Category**: Misc \
**Points**: 304 (23 solves) \
**Author**: Aurel300

## Challenge

A committee was formed last year to decide the highly-sensitive contents of the
flag for this challenge. Our informant managed to leak some data, but he was
arrested within weeks of the committee's operation. All we have are the logs of
the committee's meetings.

Note: file fixed, please redownload

Author: Aurel300 \
Attachments: `committee.zip`

## Solution

Looking at `log.txt` we see:
```git
...

commit cb18d2984f9e99e69044d18fd3786c2bf6425733
Author: Peter G. Anderson <pepega@legal.committee>
Date:   Tue Apr 14 12:00:00 2020 +0000

    Proceedings of the flag-deciding committee: 32, 33, 34

commit dca4ca5150b82e541e2f5c42d00493ba8d4aa84a
Author: Christopher L. Hatch <crisscross.the.hatch@legal.committee>
Date:   Mon Mar 23 12:30:00 2020 +0000

    Proceedings of the flag-deciding committee: 8, 31, 36

commit c3e6c8ea777d50595a8b288cbbbd7a675c43b5df
Author: Pamela W. Mathews <pammy.emm@legal.committee>
Date:   Fri Mar 13 12:30:00 2020 +0000

    Proceedings of the flag-deciding committee: 18

commit 08e1f0dd3b9d710b1eea81f6b8f76c455f634e87
Author: Robert J. Lawful <boblaw@legal.committee>
Date:   Wed Mar 4 12:00:00 2020 +0000

    Initial formation of the flag-deciding committee.
```

There are 17 commits total. The `leak` folder contains a git repo starting at
the 3rd commit. Each commit message says which character indexes in the flag
changed. For example, the first 3 commits are like so:
```
union{*******3*********_************r****d**********} | 8, 31, 36
union{*****************_****************************} | 18
union{**********************************************} | Inital
```

Exploit:
- Since each commit only changes 3 characters, we can bruteforce all
  combinations
- If we use the same git message/author/committer/date and the `flag.txt` files
  match, then the commit hash will be equal as well. We use this to verify our
  guesses

Most of the flag was ASCII lowercase + digits + underscore, but there were a
few upper case characters. For these I had to look at the flag and manually
select which characters it would be possible—otherwise it would take too long
to bruteforce.

My messy script is in `solve.py`. I was stupid and implemented multithreading
to make it run as fast as possible, but that probably ended up being more
trouble than it was worth.

Flag:
```
union{c0mm1tt33_d3c1deD_bu7_SHA_d3t3rm1n3d_6a7c2619a}
```
