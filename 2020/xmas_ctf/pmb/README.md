# PMB

**Category**: Misc \
**Points**: 50 \
**Author**: yakuhito

## Challenge

The Python Math Bank is renowed for its 'choose your interest' plans.
Unfortunately, it also collaborates with law enforcement - can you get your
ransom payment out?

Target: `nc challs.xmas.htsp.ro 6002`

## Solution

```
$ nc challs.xmas.htsp.ro 6002
#########################
#  _____  __  __ ____   #
# |  __ \|  \/  |  _ \  #
# | |__) | \  / | |_) | #
# |  ___/| |\/| |  _ <  #
# | |    | |  | | |_) | #
# |_|    |_|  |_|____/  #
#                       #
#########################
Welcome to our hacker-friendly terminal service!
This program is a part of our 'friendlier products for hackers' initiative.
Please select an action:
1. Open account
2. Report account
*you select 1*
That's great! As you probably know, our bank provides anonymous choose-your-interest-rate accounts.
Please keep in mind that the interest rate can be *any* number as long as its modulus is less than 100.
Interest: 25
Creating your account...
*your account has been created*
Received $1000 with attached note: 'ransom payment'
Balance: $1000
*request money withdrawal*
*error: your account must be at least 4 months old*

Month 1
-------
Balance: $25000.0
Your account has been reported by an anonymous user. CIA confiscated your funds.
Balance: $0.0

Month 2
-------
Balance: $0.0
Your account has been reported by an anonymous user. FBI confiscated your funds.
Balance: $0.0

Month 3
-------
Balance: $0.0
Your account has been reported by an anonymous user. INTERPOL confiscated your funds.
Balance: $0.0

Month 4
-------
Balance: $0.0
*you want to buy a flag for $10 million*
ERROR: Not enough funds.
```

We can specify an interest and we are given an initial balance of `$1000`.
In summary:
```
Constraint: |interest| < 100
Goal: $1000 * (interest)**4 >= $10 million
```

The solution is to use an imaginary number such as `99j`
```
$ nc challs.xmas.htsp.ro 6002
#########################
#  _____  __  __ ____   #
# |  __ \|  \/  |  _ \  #
# | |__) | \  / | |_) | #
# |  ___/| |\/| |  _ <  #
# | |    | |  | | |_) | #
# |_|    |_|  |_|____/  #
#                       #
#########################
Welcome to our hacker-friendly terminal service!
This program is a part of our 'friendlier products for hackers' initiative.
Please select an action:
1. Open account
2. Report account
*you select 1*
That's great! As you probably know, our bank provides anonymous choose-your-interest-rate accounts.
Please keep in mind that the interest rate can be *any* number as long as its modulus is less than 100.
Interest: 99j
Creating your account...
*your account has been created*
Received $1000 with attached note: 'ransom payment'
Balance: $1000
*request money withdrawal*
*error: your account must be at least 4 months old*

Month 1
-------
Balance: $99000j
Your account has been reported by an anonymous user. CIA confiscated your funds.
Balance: $99000j

Month 2
-------
Balance: $-9801000.0
Your account has been reported by an anonymous user. FBI confiscated your funds.
Balance: $-9801000.0

Month 3
-------
Balance: $(-0-970299000j)
Your account has been reported by an anonymous user. INTERPOL confiscated your funds.
Balance: $(-0-970299000j)

Month 4
-------
Balance: $96059601000.0
*you want to buy a flag for $10 million*
GG!
X-MAS{th4t_1s_4n_1nt3r3st1ng_1nt3r3st_r4t3-0116c512b7615456}
```
