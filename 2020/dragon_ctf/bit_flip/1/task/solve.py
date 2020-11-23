from Crypto.Util.number import long_to_bytes, bytes_to_long
import pwn
import base64
import re
import flag_decrypt
import subprocess


def get_bit(n, pos):
    return (n >> pos) & 1


def set_bit(n, pos):
    return n | (1 << pos)


# Note: This is not provided in the real challenge, but may be useful for
# debugging
seed_regex = re.compile(r'seed: (.*)\n', re.MULTILINE)

gen_regex = re.compile(r'Generated after (\d*) iterations', re.MULTILINE)
bob_regex = re.compile(r'bob number (\d*)\n', re.MULTILINE)
iv_regex = re.compile(r'bob .*\n(.*)\n', re.MULTILINE)
enc_flag_regex = re.compile(r'bob .*\n.*\n(.*)\n', re.MULTILINE)

anno = False
remote = True


def send(flip):
    payload = base64.b64encode(long_to_bytes(flip))
    sh.sendline(payload)
    output = sh.recvuntilS('bit-flip str:')
    n_iters = int(gen_regex.search(output).group(1))
    if anno:
        seed = seed_regex.search(output).group(1)
        seed = bytes.fromhex(seed)
        seed = bytes_to_long(seed)
    else:
        seed = None
    return (n_iters, seed)


def send_get_all(flip):
    payload = base64.b64encode(long_to_bytes(flip))
    sh.sendline(payload)
    output = sh.recvuntilS('bit-flip str:')

    n_iters = int(gen_regex.search(output).group(1))

    if anno:
        seed = seed_regex.search(output).group(1)
        seed = bytes.fromhex(seed)
        seed = bytes_to_long(seed)
    else:
        seed = None

    bob_number = int(bob_regex.search(output).group(1))

    iv = iv_regex.search(output).group(1)
    iv = base64.b64decode(iv)

    enc_flag = enc_flag_regex.search(output).group(1)
    enc_flag = base64.b64decode(enc_flag)

    return {
        'n_iters': n_iters,
        'seed': seed,
        'bob_number': bob_number,
        'iv': iv,
        'enc_flag': enc_flag
    }


if remote:
    sh = pwn.remote('bitflip1.hackable.software', 1337)
else:
    if anno:
        sh = pwn.process('./task_anno.py')
    else:
        sh = pwn.process('./task.py')

if remote:
    hashcash_regex = r'.* Proof of Work: (.*)\n'
    output = sh.recvline(hashcash_regex).decode()
    hashcash_cmd = re.search(hashcash_regex, output).group(1)

    print('Running hashcash cmd:', hashcash_cmd)
    hashcash_token = subprocess.check_output(hashcash_cmd, shell=True).decode().strip()
    print('Got hashcash token:', hashcash_token)
    sh.sendline(hashcash_token)

if anno:
    output = sh.recvuntilS('bit-flip str:')
    alice_seed = re.search(r'alice_seed: (.*)\n', output).group(1)
    alice_seed = bytes.fromhex(alice_seed)
    alice_seed = bytes_to_long(alice_seed)
else:
    print('Starting bit flipping')
    output = sh.recvuntilS('bit-flip str:')

orig_n_iters = send(0)[0]
print('Original number of iters:', orig_n_iters)

guess = 0
for i in range(1, 128):
    # 3 2 1 0
    # x 1 1 0
    des = set_bit(0, i) - 2
    flip = guess ^ des
    (x_n_iters, x_seed) = send(flip)

    # 3 2 1 0
    # x 0 0 0
    flip = guess | set_bit(0, i)
    (y_n_iters, y_seed) = send(flip)

    if x_n_iters == y_n_iters + 1:
        # It's zero
        pass
    else:
        guess = set_bit(guess, i)

    print('.', end='', flush=True)

print()

guesses = [guess, guess + 1]
for guess in guesses:
    response = send_get_all(0)
    print(flag_decrypt.get_flag(response, guess))
