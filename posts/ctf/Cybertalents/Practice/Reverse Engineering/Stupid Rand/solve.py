import ctypes

libc = ctypes.CDLL("libc.so.6")
enc = open('enc', 'rb').read()

for seed in range(0, 0xffff):
    libc.srand(seed)
    decrypted = ""

    for j in enc:
        key = libc.rand()
        # print(hex(key), hex(j))
        decrypted += chr((key ^ j) & 0xff)
    
    if "flag" in decrypted:
        print(decrypted)
