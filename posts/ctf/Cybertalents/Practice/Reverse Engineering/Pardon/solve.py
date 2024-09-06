"""
Binary is packed with: ConfuserEx

The decryption is easy to spot so i didn't bother trying to unpack, deobsfucate

The decryption schema is as follows:

Generates a random byte value which is used as xor key against a list of numbers

It's within 0 to 0xff so we can either brute force the key or recover it via property of xor

I went with recovering it since i knew the flag format was "Flag"

After retrieval we just xor the encrypted flag with the key.
"""
from pwn import xor

enc = [11, 1, 12, 10, 54, 25, 37, 36, 62, 4, 62, 5, 34, 58, 20, 34, 56, 9, 34, 4, 57, 5, 44, 53, 125, 63, 108, 55, 34, 125, 63, 55, 48]
arr = ''.join(list(map(chr, enc)))
key = xor(enc[0], 'F')

print(xor(arr, key).decode())
