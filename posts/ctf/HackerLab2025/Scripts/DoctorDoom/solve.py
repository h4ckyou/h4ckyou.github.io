import ctypes

with open("flag.txt.enc", "rb") as f:
    enc = f.read()

n = len(enc)
libc = ctypes.CDLL("libc.so.6")

start = 1744998159-0x5000
end = 1744998159+0x1000

for seed in range(start, end):
    libc.srand(seed)
    data = bytearray(n)
    for i in range(n):
        key = libc.rand() & 0xffffffff
        data[i] = (enc[i] ^ key) & 0xff
    
    print(data) 
