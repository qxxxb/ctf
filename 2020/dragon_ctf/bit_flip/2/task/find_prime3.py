#!/usr/bin/python3

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


class DiffieHellman:
  def gen_strong_prime(self):
    prime = self.rng.getbits(512)
    iter = 0
    strong_prime = 2*prime+1
    while not (prime % 5 == 4) or not is_prime(prime) or not is_prime(strong_prime):
      iter += 1
      prime = self.rng.getbits(512)
      strong_prime = 2*prime+1
    print("Generated after", iter, "iterations")
    return strong_prime

  def __init__(self, seed, prime=None):
    self.rng = Rng(seed)
    if prime is None:
      prime = self.gen_strong_prime()

    self.prime = prime
    self.my_secret = self.rng.getbits()
    self.my_number = pow(5, self.my_secret, prime)
    self.shared = 1337

  def set_other(self, x):
    self.shared ^= pow(x, self.my_secret, self.prime)


threshold = 2 ** 16

def find_cycle(g, p):
  x = g
  group = {x}
  while True:
    if len(group) > threshold:
      return -1

    x = (x * g) % p
    if x in group:
      break
    else:
      group.add(x)

  return len(group)

def main():
  while True:
    alice_seed = os.urandom(32)
    alice = DiffieHellman(alice_seed)

    q = (alice.prime - 1) // 2
    w = q
    tmp = (alice.prime - 1) // w  # 2
    print(tmp)
    if alice.my_secret % tmp == 0:
      print('Promising')
      bob = DiffieHellman(os.urandom(16), alice.prime)
      alice.set_other(bob.my_number)
      bob.set_other(alice.my_number)

      order = find_cycle(alice.shared, alice.prime)
      if order != -1:
        print("Found small subgroup with order", w)
        print("alice_seed:", alice_seed)
        pprint.pprint(vars(alice))
        return
      else:
        print("Subgroup too big")
    else:
      print('*')

main()
