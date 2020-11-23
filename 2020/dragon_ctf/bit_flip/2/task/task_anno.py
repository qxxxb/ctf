#!/usr/bin/python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
import hashlib
import os
import base64
from gmpy2 import is_prime
import pprint

FLAG = open("flag").read()
FLAG += (16 - (len(FLAG) % 16))*" "


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

my_prime = 11391379263766066030135918376562538981196391001827571715194865455842376327512086588913712210956579206753407897779606205522510652032504825336272563672326153

class DiffieHellman:
  def gen_prime(self):
    return my_prime
    prime = self.rng.getbits(512)
    iter = 0
    while not is_prime(prime):
      iter += 1
      prime = self.rng.getbits(512)
    print("Generated after", iter, "iterations")
    return prime

  def __init__(self, seed, prime=None, secret=None):
    self.rng = Rng(seed)
    if prime is None:
      prime = self.gen_prime()
    self.prime = prime

    if secret is None:
      self.my_secret = self.rng.getbits()
    else:
      self.my_secret = secret

    self.my_number = pow(5, self.my_secret, prime)
    self.shared = 1337

  def set_other(self, x):
    self.shared ^= pow(x, self.my_secret, self.prime)

def pad32(x):
  return (b"\x00"*32+x)[-32:]

def xor32(a, b):
  return bytes(x^y for x, y in zip(pad32(a), pad32(b)))

def bit_flip(x):
  print("bit-flip str:")
  flip_str = base64.b64decode(input().strip())
  return xor32(flip_str, x)

def subgroup(g, p):
    x = g
    subgroup = {x}
    while True:
        if len(subgroup) > 2 ** 16:
            return {}

        x = (x * g) % p
        if x == 1:
            return subgroup
        else:
            subgroup.add(x)

threshold = 2 ** 16

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


alice_seed = os.urandom(16)

while 1:
  ws = [2, 3, 67, 109, 229, 1621]
  w = ws[2]
  q = (my_prime - 1) // w

  alice = DiffieHellman(alice_seed, secret=q)
  pprint.pprint(vars(alice))
  bob = DiffieHellman(os.urandom(16), alice.prime)

  alice.set_other(bob.my_number)
  bob.set_other(alice.my_number)

  pprint.pprint(vars(bob))

  iv = os.urandom(16)
  print(base64.b64encode(iv).decode())

  key = long_to_bytes(alice.shared, 16)[:16]
  print(key)

  cipher = AES.new(key, AES.MODE_CBC, IV=iv)
  enc_flag = cipher.encrypt(FLAG.encode())
  print(base64.b64encode(enc_flag).decode())

  real_shared = bob.shared ^ 1337
  print(order(real_shared, my_prime))
  print(subgroup(real_shared, my_prime))
