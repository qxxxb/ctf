# subdomain

Points: 50

Using [Sublist3r](https://github.com/aboul3la/Sublist3r) we can get a list of
subdomains. One that looks interesting is:
`9vyloyc3ojspmtuhtm6ejq.osucyber.club`. However, scanning it with `nmap` only
shows a few ports that don't seem to lead any where (`22`, `80`, `443`). Any
HTTP request returns a 404. But the challenge also mentions that the site was
recently taken down, so we can maybe check on `web.archive.org` to find an old
version. Indeed, we can find
https://web.archive.org/web/20201022183102/http://9vyloyc3ojspmtuhtm6ejq.osucyber.club/.
Inspecting the source of the page and searching for `osuctf`, we find: `<!--
osuctf{wayback_mach1n3_mucks_fichigan} -->`
