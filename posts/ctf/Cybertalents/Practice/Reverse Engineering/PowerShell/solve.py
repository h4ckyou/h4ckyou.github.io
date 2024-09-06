import hashlib

version = "0.0.0.0"
hashed = hashlib.md5(version.encode()).digest()
arr = [int(i) for i in version.split('.')]
flag = bytearray(23)

flag[0] = hashed[9]  ^ 0xdf
flag[1] = hashed[4]  ^ 0xef
flag[2] = hashed[2]  ^ 0x18
flag[3] = hashed[10] ^ 0x17
flag[4] = hashed[4]  ^ 0xf8
flag[5] = hashed[13] ^ 0xa0
flag[6] = hashed[6]  ^ 0x8c
flag[7] = hashed[14] ^ 0xf5
flag[8] = hashed[12] ^ 0x31
flag[9] = hashed[10] ^ 0x2f
flag[10] = hashed[4] ^ 0xf6
flag[11] = hashed[1] ^ 0x81
flag[12] = hashed[5] ^ 0x25
flag[13] = hashed[9] ^ 0xf7
flag[14] = hashed[6] ^ 0xbd
flag[15] = hashed[0] ^ 0x90
flag[16] = hashed[12] ^ 0xb
flag[17] = hashed[6] ^ 0x91
flag[18] = hashed[8] ^ 0x5e
flag[19] = hashed[5] ^ 0x2f
flag[20] = hashed[14]  ^ 0xfa
flag[21] = hashed[15] ^ 0xe8
flag[22] = hashed[6] ^ 0x9f

print(flag.decode())
