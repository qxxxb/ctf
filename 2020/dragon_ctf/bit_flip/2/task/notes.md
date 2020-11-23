# Bit Flip 2

This is exactly the same as Bit Flip 1 except this time we don't know `bob.my_number` ($g^j$).

From Bit Flip 1, here is what we have:
- We know `alice_seed`
- We can control `alice_seed`
  - This gives us some control over $k$ and $p$

Here's what we need:
- We need to find $g^{jk}$
- We know $g$, $k$, and $p$
- We have some control over $k$ and $p$

Differences between Bit Flip 3:
- Bit Flip 3 uses safer primes: $p = 2q + 1$
- In other words, $p - 1 = 2q$ where $q$ is a 512 bit prime
- Thus the order of $g$ has a large prime factor $q$, preventing [Pohlig-Hellman](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)
  - This hint may be the technique for solving Bit Flip 2
- Bit Flip 3 also requires that `q % 5 == 4`. What is the purpose of this?

Possible leads:
- https://crypto.stackexchange.com/q/66119
  - Pick an insecure $p$
    - Pick seeds until `Rng(seed)` gives us an insecure prime
    - Use the seed for the exploit

We're using $\mathbb{Z}_p^*$, the multiplicative group of integers modulo $p$.
If $p$ is prime (`is_prime` only uses probabilistic checks), then group has order $p - 1$.
This value of $p - 1$ is important for this group.
However, the code makes no checks about the value of $p - 1$.

## Pohlig-Hellman

Used to compute discrete logarithms of $\mathbb{Z}_p^*$

### Discrete logarithms

$log_b a = k$ where $b^k = a$.

For our purposes:
$g^j \equiv a \mod{p}$

We want to find $j$. However, we don't even know $g^j$, so what can we do?

Is it possible to pick a prime $p$ such that the order of $g$ is small enough that we can brute-force $(g^k)^j$? We could check all possible values of $g^{jk}$.

## Lagrange's Theorem

If a group $E$ has a subgroup $E'$, then the order of $E$ is divisible by the order of $E'$.

For example, the Curve25519 group has order $hq$ where $h = 8$ and $q$ is a large prime. Then every Curve25519 group element must have order $1$, $2$, $4$, $8$, $q$, $2q$, $4q$. In this scenario, if we can get a subgroup with order $1$, $2$, $4$, or $8$, then we can brute-force its subgroup.

For Diffie-Hellman in $\mathbb{Z}_p^*$, we know that $p - 1$ will be even (because $p$ is prime). So factors of $p - 1$ include $1$, $2$, $q$, $2q$ at the very least, where $p - 1 = 2q$.

## Small subgroup confinement attack

The scenario described above is the small subgroup confinement attack.
One possible attack for this problem is to find a $p$ such that the order of $g^k$ is small enough that we can brute-force it. However, using a simple generate-and-test program, I've found that these are very hard to find even for 128 bit primes.

Maybe instead of choosing a special $p$, we can try choosing a special $k$.as described [here](https://crypto.stackexchange.com/q/27584).

Attack:
- Create a list of small primes `ws`
- Generate random primes $p$ using a seed
- Find which `ws` elements divide $p - 1$. Store in `ws_div`
- For each `w` in `ws_div`, compute `tmp = (p - 1) // w`
  - Check if `k` is a multiple of `tmp`
  - If so, we know that `shared` will be in a small subgroup of size `w`
 - This doesn't work because `tmp` will be much larger than `k`.
  
Attack (currenlty running):
- Generate random primes $p$ using a seed
- Check if $k$ is prime
- Check if $k$ divides $p - 1$
- If so, then we know the shared key belongs to a subgroup of size $k$
- It seems highly unlikely that $k$ itself will divide $p - 1$
- In fact, it's relatively infrequent that $k$ is prime
- How do ensure that `tmp` is small?
- $p$ is 512 bits
  - $k$ is 64 bits
  - We want $w$ on the order of 20 bits
  - In order for $k$ to be a multiple of `tmp`, `tmp` must be smaller than 64 bits
  - In order for `tmp` to be small, $w$ must be large.
  - Goal: Find a large prime $w$ that divides $p - 1$
  - This seems hard for Bit Flip 2. But doesn't Bit Flip 3 rely on a large prime $q$ such that $2q = p - 1$? Can't we leverage this?
    - Tried it, but doesn't seem to work. When I actually search within the `shared` subgroup, it's too big

Notes from https://tools.ietf.org/html/:
- Compute `y^q mod p`. If the result is 1, the key is valid. Otherwise the key is invalid.
