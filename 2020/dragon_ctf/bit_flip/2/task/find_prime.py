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
  def gen_prime(self):
    prime = self.rng.getbits(512)
    iter = 0
    while not is_prime(prime):
      iter += 1
      prime = self.rng.getbits(512)
    return prime

  def __init__(self, seed, prime=None):
    self.rng = Rng(seed)
    if prime is None:
      prime = self.gen_prime()

    self.prime = prime
    self.my_secret = self.rng.getbits()
    self.my_number = pow(5, self.my_secret, prime)
    self.shared = 1337

  def set_other(self, x):
    self.shared ^= pow(x, self.my_secret, self.prime)


threshold = 2 ** 14

def order(g, p):
    r = 1
    x = g
    while True:
        if r > threshold:
            return -1

        x = (x * g) % p
        r += 1
        if x == 1:
            return r


def main():
  alice_seed = os.urandom(32)

  while True:
    alice = DiffieHellman(alice_seed)
    subgroup_order = order(alice.my_number, alice.prime)
    if subgroup_order != -1:
      print("alice_seed:", alice_seed)
      pprint.pprint(vars(alice))
      return
    else:
      print('*', end='', flush=True)

    alice_seed = alice.rng.seed

main()
