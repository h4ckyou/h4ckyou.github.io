from pwn import xor, string
import itertools

encrypted = bytes.fromhex("2300081348071a3a5a064a6c095c07136c70375f5a044a6c03205d136c59301f1d2b47031a580d106c4075015a2b55462b330f44416c3c5c1c55124e")
known = "flag{"
key_part = xor(known, encrypted[:len(known)])

for key in range(0xff):
    brute = key_part.decode() + chr(key)
    d = xor(encrypted, brute)
    print(d)
