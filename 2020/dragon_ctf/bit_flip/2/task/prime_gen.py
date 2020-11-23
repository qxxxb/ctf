from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
import hashlib
import os
import base64
from gmpy2 import is_prime, next_prime
import pprint

class Rng:
  def __init__(self, seed):
    self.seed = seed
    self.generated = b""
    self.num = 0

  def more_bytes(self):
    self.generated += hashlib.sha256(self.seed).digest()
    self.seed = long_to_bytes(bytes_to_long(self.seed) + 1, 32)
    self.num += 256

  def getbits(self, num=64):
    while (self.num < num):
      self.more_bytes()
    x = bytes_to_long(self.generated)
    self.num -= num
    self.generated = b""
    if self.num > 0:
      self.generated = long_to_bytes(x >> num, self.num // 8)
    return x & ((1 << num) - 1)

def small_primes(n):
  ans = []
  p = 1
  for i in range(n):
    p = next_prime(p)
    ans.append(p)
  return ans

ps = small_primes(400)
threshold = 2 ** 20

def factor(n):
  ans = []
  for p in ps:
    while n % p == 0:
      n //= p
      ans.append(p)
  print(n)
  if n < threshold:
    print("Small!")
  return ans

rng = Rng(b'\x00')

while True:
  p = rng.getbits(512)
  if is_prime(p):
    print(p)
    small_factors = factor(p - 1)
    print(small_factors)
