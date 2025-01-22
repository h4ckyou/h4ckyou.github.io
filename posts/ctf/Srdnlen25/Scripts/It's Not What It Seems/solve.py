import struct
from pwn import xor

buf = [0x3B2E252C2E243233, 0x32341F327336732E, 0x1F7328141F347535, 0x2E35261F2E71742D, 0x3D2E707134232E35]
key = 0x40
enc = b""

for i in buf:
    enc += struct.pack("<Q", i)

print(xor(enc, key))