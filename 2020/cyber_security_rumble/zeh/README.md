# zeh

Points: 100

Looking at the code here:
```c
    k = k ^ e;

    if(k == 53225)
        puts("Success");
    else
        puts("Fail");
```

Since we control `e` and `k` has a deterministic value, let's just plug in 0 for
an initial value of `k` and see what it ends up being.

Using `gdb`, I found that it was `1804289383`. Then:
```
53225 = 1804289383 ^ e
e = 53225 ^ 1804289383
e = 1804307086
```

Thus the payload is `0 1804307086`.
