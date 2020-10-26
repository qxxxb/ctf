## Hash Mash

Points: 25

Formatting the text slightly, we get this:

```
3e2e95f5ad970eadfa7e17eaf73da97024aa5359
2346ad27d7568ba9896f1b7da6b5991251debdf2
b47f363e2b430c0647f14deea3eced9b0ef300ce
fc19318dd13128ce14344d066510a982269c241b
8fcd25a39d2037183044a8897e9a5333d727fded
b295d117135a9763da282e7dae73a5ca7d3e5b11
```

Since each of these consist of 40 hex digits, we can assume that they were generated from SHA-1. We can then use https://hashes.com/en/decrypt/hash to decode them. This gives us:
`osuctf{potato_hash_is_good_with_salt}`
