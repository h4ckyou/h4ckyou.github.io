from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from math import gcd
from warnings import filterwarnings
import subprocess

io = remote("titan.picoctf.net", 61923)
context.log_level = 'info'
filterwarnings("ignore")

m1 = b'a'
m2 = b'b'

io.sendline("E")
io.sendline(m1)
io.recvuntil("n) ")
c1 = int(io.recvline().decode())

io.sendline("E")
io.sendline(m2)
io.recvuntil("n) ")
c2 = int(io.recvline().decode())

e = 65537 

k1n = (bytes_to_long(m1) ** e) - c1
k2n = (bytes_to_long(m2) ** e) - c2

n = gcd(k1n, k2n)

assert c1 == pow(bytes_to_long(m1), e, n)

print(f"n: {n}")

with open("password.enc", "r") as fp:
    ct = fp.read()

pad = n + int(ct)
print(f"pad: {pad}")

io.sendline("D")
io.sendline(str(pad))

io.recvuntil(": ")
pt = bytes.fromhex(io.recvline().decode().split()[-1])
print(f"AES Password: {pt}")

io.close()
