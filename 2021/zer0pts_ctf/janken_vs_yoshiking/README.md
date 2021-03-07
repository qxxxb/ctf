# janken vs yoshiking

**Category**: Crypto \
**Points**: 143 (44 solves) \
**Author**: theoldmoon0602

## Challenge

Yoshiking knows the flag. He will give the flag to who has gold luck. Let's play
the janken with Yoshiking and prove your luck!

`nc crypto.ctf.zer0pts.com 10463`

Attachments: `janken_vs_yoshiking.tar.gz`

## Solution

Here's the challenge:
```python
import random
import signal
from flag import flag
from Crypto.Util.number import getStrongPrime, inverse

HANDNAMES = {
    1: "Rock",
    2: "Scissors",
    3: "Paper"
}

def commit(m, key):
    (g, p), (x, _) = key
    r = random.randint(2, p-1)
    c1 = pow(g, r, p)
    c2 = m * pow(g, r*x, p) % p
    return (c1, c2)


def decrypt(c, key):
    c1, c2 = c
    _, (x, p)= key
    m = c2 * inverse(pow(c1, x, p), p) % p
    return m


def keygen(size):
    p = getStrongPrime(size)
    g = random.randint(2, p-1)
    x = random.randint(2, p-1)

    return (g, p), (x, p)


signal.alarm(3600)
key = keygen(1024)
(g, p), _ = key
print("[yoshiking]: Hello! Let's play Janken(RPS)")
print("[yoshiking]: Here is g: {}, and p: {}".format(g, p))

round = 0
wins = 0
while True:
    round += 1
    print("[system]: ROUND {}".format(round))

    yoshiking_hand = random.randint(1, 3)
    c = commit(yoshiking_hand, key)
    print("[yoshiking]: my commitment is={}".format(c))

    hand = input("[system]: your hand(1-3): ")
    print("")
    try:
        hand = int(hand)
        if not (1 <= hand <= 3):
            raise ValueError()
    except ValueError:
        print("[yoshiking]: Ohhhhhhhhhhhhhhhh no! :(")
        exit()

    yoshiking_hand = decrypt(c, key)
    print("[yoshiking]: My hand is ... {}".format(HANDNAMES[yoshiking_hand]))
    print("[yoshiking]: Your hand is ... {}".format(HANDNAMES[hand]))
    result = (yoshiking_hand - hand + 3) % 3
    if result == 0:
        print("[yoshiking]: Draw, draw, draw!!!")
    elif result == 1:
        print("[yoshiking]: Yo! You win!!! Ho!")
        wins += 1
        print("[system]: wins: {}".format(wins))

        if wins >= 100:
            break
    elif result == 2:
        print("[yoshiking]: Ahahahaha! I'm the winnnnnnner!!!!")
        print("[yoshiking]: You, good loser!")
        print("[system]: you can check that yoshiking doesn't cheat")
        print("[system]: here's the private key: {}".format(key[1][0]))
        exit()

print("[yoshiking]: Wow! You are the king of roshambo!")
print("[yoshiking]: suge- flag ageru")
print(flag)
```

Ok cool, let's try playing:
```
$ nc crypto.ctf.zer0pts.com 10463
[yoshiking]: Hello! Let's play Janken(RPS)
[yoshiking]: Here is g: 93246466493691290620182341454221633182460738434093815614077634080811517316341693745452680006974397748549073183117736391520888357272614864106181802187021183835474370489602909536063062232676255474901456464530906809271865057165340499683065369727180882086646017049438362596410504704204860951104447125103398714724, and p: 175260510573199640037642339820283538897541297874737572855697757265705383191213854343948586106190401497192681772568271208606712764847196343016562688822513491034608107038867961034265033527052343132581506482292841372716055224460126927165986190540381376918906475686409173155989992550341788186503659560888692515471
[system]: ROUND 1
[yoshiking]: my commitment is=(112651872829754024283473409318843778681638126351770042582374400478440525882886726719756618379935417439904071214109877213367442204160375946345454767709109803229236401357963557510315011234912272481048752200427546337153367523061616451042946744469337075954710436426439652334987967376487425331704233306024655105176, 115245909685214127944207618842326314178160285396719345903403728951651310138928930238377788066374467272423096900457550327395478903539795679566608658438289761945940485296317857085518101487728973674459127879074084185532790425810710996037585628864608127918624790524605037353276382371539473645236236933680909482701)
[system]: your hand(1-3): 1

[yoshiking]: My hand is ... Scissors
[yoshiking]: Your hand is ... Rock
[yoshiking]: Yo! You win!!! Ho!
[system]: wins: 1
[system]: ROUND 2
[yoshiking]: my commitment is=(161403278591040354605417036011896951435134275207122273129458056487290363740948660606229221525160025068245437176171796581510885742819286478423908399887420750642822138770465844085806830129108172249919419369892417952381609714792030850041269560520979904064951433491793355600089020675980462504700892374092872950002, 92715687382822328798263887951852472168705583088419371689873971982065659870782921182332562059144193113377771897365564067387318554789009354400379903941568475701306865902660861859832518436661644938305251862797437660152585947595604457533665840102936250016674173358362720153964609438763516488467077157766086764564)
[system]: your hand(1-3): 2

[yoshiking]: My hand is ... Scissors
[yoshiking]: Your hand is ... Scissors
[yoshiking]: Draw, draw, draw!!!
[system]: ROUND 3
[yoshiking]: my commitment is=(162648139983079039210429983992623031636987459728763727233622096497635372303027173615732409588355323020966239590464490063815748578967233983434270795501590768933949445098071710642727266259389395766655769999516542485629442587738235298651085427923008449646529019430628498677842888872941279221981837513128334531096, 142848696422881868056551200689837064864660889473467350378995958190417128882419210201110373735508636775322371867419985699588028425792545024113316008697817062844624119711500249828738416381927190489065357183025698362852535365166470686627594277018931077962239541743836289607729514802886672509183557913570493069143)
[system]: your hand(1-3): 2

[yoshiking]: My hand is ... Scissors
[yoshiking]: Your hand is ... Paper
[yoshiking]: Ahahahaha! I'm the winnnnnnner!!!!
[yoshiking]: You, good loser!
[system]: you can check that yoshiking doesn't cheat
[system]: here's the private key: 64374958372873310433110749433773684872150993622043711610669809604637278767761286233154066185796824212804867670985223698719896990586340990462229819212484386522137010301983420276730792959563081181574872642810981970937405142279352548848302624141126634775271664453741169343121168240221765094331538329803386574402
```

So all we have to do is win 100 rounds of rock paper scissors. On each round,
they give us two ciphertexts (`c1` and `c2`) that encrypt yoshiking's hand,
which could be either 1 (rock), 2 (scissors), or 3 (paper).

This challenge seems to use a home-rolled cryptosystem based on Diffie-Hellman
over the multiplicative group modulo a prime.

We're given a strong prime `p` and a generator `g`. There is also a private `x`,
but we don't know its value:
```python
def keygen(size):
    p = getStrongPrime(size)
    g = random.randint(2, p-1)
    x = random.randint(2, p-1)
    return (g, p), (x, p)
```

Next, the encryption picks a random `r`, which serves as an obscuring factor.
Then we're given `g^r` and `m * g^(rx)`.
```python
def commit(m, key):
    (g, p), (x, _) = key
    r = random.randint(2, p-1)
    c1 = pow(g, r, p)
    c2 = m * pow(g, r*x, p) % p
    return (c1, c2)
```

Due to the hardness of the discrete logarithm problem, we can't compute `r` or
`r * x`.

Finally, the decryption step is like this:
```
m === c2 / c1^x
m === m * g^(rx) / g^(rx)
m === m
```
In code:
```python
def decrypt(c, key):
    c1, c2 = c
    _, (x, p)= key
    m = c2 * inverse(pow(c1, x, p), p) % p
    return m
```

How can we attack this?
- Since `p` is a strong prime, attacks like Pohlig-Hellman or small subgroup
  attacks won't work.
- As mentioned earlier, even when we know `g`, `g^r`, and `g^(rx)`, we can't
  calculate `r` or `x`

However, since `m` can only be 1, 2, 3, maybe we don't need a full break of the
cryptosystem to find `m`. In the end, it boils down to being able to distinguish
between these values:
```
c2 === 1 * g^(rx)
c2 === 2 * g^(rx)
c2 === 3 * g^(rx)
```

This reminds me of the Decisional Diffie-Hellman assumption. After some quick
googling, it turns out that the DDH assumption **doesn't** hold in a
multiplicative group modulo a prime. Why is this?

Some quick background on quadratic residues (also check out the related
challenges on Cryptohack):

We say `a` is a quadratic residue if there's some `r` such that
`r^2 === a  (mod p)`. So basically, a quadratic residue is like a perfect square
`mod p`.

Also:
```
Abbreviate QR as any quadratic residue
 QR *  QR =  QR
!QR *  QR = !QR
!QR * !QR =  QR
```

Going back to the problem, let's say `g` is a QR. Then `g^anything` is also a
QR. This means `g^(rx)` will also be a QR.

We know that `1` is always a QR. (`1^2 === 1`). But `2` and `3` may or may not
be a QR depending on the value of `p`.

Let's say we get a `p` so that (we can reconnect to the challenge server until
we get one):
```
1 is a QR (always true)
2 is a QR
3 is not a QR
```

Then:
```
If m == 1: m * g^(rx) is a QR
If m == 2: m * g^(rx) is a QR
If m == 3: m * g^(rx) is not a QR
```

How can we check if something is a QR? Use the Legendre symbol, which can
be computed efficiently in Sage: `legendre_symbol(c2, p)`

Finally we can narrow down the value of `m` like so:
```python
if legendre_symbol(c2, p) == -1:
    return 3
else:
    # m is either 1 or 2
    pass
```

At this point, I was stuck for many hours. I tried all kinds of weird stuff to
distinguish between `m = 1` and `m = 2`, but couldn't find anything. Then I
realized that we actually *don't need to know* which one it is.

Remember that 1 is rock and 2 is scissors. If we always pick rock, then we can
at least force a tie and the game will continue. Since we just need to get 100
wins in total, this works fine:

```python
if legendre_symbol(c2, p) == -1:
    return 3
else:
    return 1  # Always pick rock
```

Here's my complete script:
```python
import pwn

pwn.context.log_level = "debug"


while True:
    io = pwn.remote("crypto.ctf.zer0pts.com", 10463)
    io.recvline()
    s = io.recvlineS()
    g, p = s.split(", and p: ")
    p, g = int(p), int(g[24:])
    if (
        legendre_symbol(g, p) == 1
        and legendre_symbol(2, p) == 1
        and legendre_symbol(3, p) == -1
    ):
        break

    print("Bad params, trying again")

print("Good pararms, starting exploit")

while True:
    io.recvuntilS("ROUND")
    io.recvline()
    s = io.recvlineS().strip()[31:-1]
    c1, c2 = s.split(", ")
    c1, c2 = int(c1), int(c2)

    """
    If the Legendre symbol is 1, it could either be 1 or 2. To force at
    least a tie, we always pick rock, which is 1
    """
    hand = 3 if legendre_symbol(c2, p) == -1 else 1
    io.sendlineafter("your hand(1-3):", str(hand))
```

Output:
```
Programs/zer0pts/janken_vs_yoshiking via 🐍 system pypy3.6-7.3.1 took 3s
$ export PWNLIB_NOTERM=true

Programs/zer0pts/janken_vs_yoshiking via 🐍 system pypy3.6-7.3.1
$ sage solve.sage
...

[x] Opening connection to crypto.ctf.zer0pts.com on port 10463
[x] Opening connection to crypto.ctf.zer0pts.com on port 10463: Trying 64.225.59.76
[+] Opening connection to crypto.ctf.zer0pts.com on port 10463: Done
[DEBUG] Received 0x56f bytes:
    b"[yoshiking]: Hello! Let's play Janken(RPS)\n"
    b'[yoshiking]: Here is g: 27821288031048497638040321441366934402724241867733654609380781519468353894312417097558338110815488446613855400848537707468325667521630064599131559919833907679336706983542547273990287177437490768527036635999298397143799087556049157481559053044527183876583934571600294562255172304210687393455444302548344965470, and p: 172213679200640475128065574192234498162317672997499408733466713668251680583340186760366499313486259038211444377830415417639625172925417500734119787733829027451993598051891138886718674789089506190579227639115200070868855462262418492102838187040511473038871997795416404535679247404826356931586745254973940694393\n'
    b'[system]: ROUND 1\n'
    b'[yoshiking]: my commitment is=(135081827361253404849814915454970728803287011764857593540436872647517872687567775396260287309814396550048127643570792587256050352163472479008941618270029167057027463845895040440226651269682499075274210084634022867564907374626771094067343048934111093491179344904537064388501918111915266345787669882762802342350, 117918766543864138696691444590790837016368372195220384335013229323468908058694465600257012838898418078284227914033083303949616340550650516247974706600033205227567049599341941233205343299865609196471862459839816610126285451743661621916524574399613123036452588181979518595221326190096230502188765423777108041373)\n'
    b'[system]: your hand(1-3): '
Good pararms, starting exploit
[DEBUG] Sent 0x2 bytes:
    b'3\n'
[DEBUG] Received 0x31f bytes:
    b'\n'
    b'[yoshiking]: My hand is ... Paper\n'
    b'[yoshiking]: Your hand is ... Paper\n'
    b'[yoshiking]: Draw, draw, draw!!!\n'
    b'[system]: ROUND 2\n'
    b'[yoshiking]: my commitment is=(66097170599603837124408025796041420612172170016417766439322589406251220607607606618199130438397156788523698275684290687812305710292459903024381750962760374863853729860562932795087534045977337142210527665114500393562590498678982081477613351650505102439355335127571090278928719937416606635306067892154710742342, 53766246218487733953260208431534217882490092303030889377893359820682129218770573761152275624076887624220962973988189548819149515209256292105064150406819326418637748116691815739378316236354408924343610515277471279772317788566928046510521283861391766659983117893802066432579531575617852175352548159764791124894)\n'

...

    b'[system]: your hand(1-3): '
[DEBUG] Sent 0x2 bytes:
    b'1\n'
[DEBUG] Received 0xf2 bytes:
    b'\n'
    b'[yoshiking]: My hand is ... Scissors\n'
    b'[yoshiking]: Your hand is ... Rock\n'
    b'[yoshiking]: Yo! You win!!! Ho!\n'
    b'[system]: wins: 100\n'
    b'[yoshiking]: Wow! You are the king of roshambo!\n'
    b'[yoshiking]: suge- flag ageru\n'
    b'zer0pts{jank3n-jank3n-0ne-m0r3-batt13}\n'
Traceback (most recent call last):
  File "solve.sage.py", line 30, in <module>
    io.recvuntilS("ROUND")
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/tube.py", line 1379, in wrapperS
    return context._decode(func(self, *a, **kw))
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/tube.py", line 310, in recvuntil
    res = self.recv(timeout=self.timeout)
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/tube.py", line 82, in recv
    return self._recv(numb, timeout) or b''
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/tube.py", line 160, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/tube.py", line 131, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
  File "/home/plushie/Programs/archive/pwntools/pwnlib/tubes/sock.py", line 56, in recv_raw
    raise EOFError
EOFError
```
