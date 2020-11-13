## authbot

Points: 50

This was a shitty challenge authored by me.

You can't talk to the bot in the CTF server (as that would reveal the answers
to other users), but you can message the bot through DM. You can try out each
command to see what it does.

In particular, the `$auth` command seems to require a password.  Another
interesting command is `$info`, which will send a link to a GitHub of the bot's
[source code](https://github.com/qxxxb/auth_bot).

Looking through the source code, you'll notice a command that isn't mentioned
in `$help`: `$debug_log`. Running this gives us:
```
2020-10-23 23:39:08 INFO     Logged in as authbot#4452
2020-10-23 23:39:13 DEBUG    User ath0#0294 authed as admin with password hash c023d5796452ad1d80263a05d11dc2a42b8c19c5d7c88c0e84ae3731b73a3d34
```

You can then plug `c023d5796452ad1d80263a05d11dc2a42b8c19c5d7c88c0e84ae3731b73a3d34` into a hash
cracker like https://hashes.com/en/decrypt/hash.

This will tell you that the password is `gobucks`. After running `$auth gobucks`,
you'll get this message:
```
Successfully authenticated as admin on BuckeyeCTF
```

You can then go back to the CTF server and see that you now have the
`authenticated` role, which gives you access to the `authbot-flag` text
channel, where you can find the flag:

```
osuctf{d0n7_lOG_y0UR_Au7h_57r1Ngs}
```
