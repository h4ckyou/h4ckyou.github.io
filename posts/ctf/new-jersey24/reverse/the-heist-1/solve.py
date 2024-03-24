from pwn import *

def rol(value, shift):
    return ((value << shift) | (value >> (8 - shift))) & 0xFF

def ror(value, shift):
    return (value >> shift) | (value << (8 - shift)) & 0xff

def check(v4):
    r = (v4 + 96) & 0xff
    r = (~r) & 0xff
    r = (rol(r, 4)) & 0xff
    r = (r ^ 0x55) & 0xff
    return bytes([r])

buffer = p64(0xE383C3B3232383C3)
buffer += p64(0x0C33E3A3)

pin = ''

for i in range(len(buffer)):
    for j in range(0xff+1):
        if check(j) == p8(buffer[i]):
            pin += chr(j)
        
print(pin)
