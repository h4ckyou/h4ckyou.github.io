from Crypto.Cipher import ARC4

Str2 = [85, 164, 230, 153, 218, 166, 110, 49, 146, 108, 192, 153, 8, 222, 170, 222, 93, 116, 34, 227, 22, 24, 253, 115]
v5 = [208, 161, 160, 236, 202, 244, 230, 202, 164, 167, 166, 161]
key = [0] * 12

for i in range(12):
    key[i] = (v5[i] ^ 0x95) & 0xff

key = bytes(key)
cipher = ARC4.new(key)
pt = cipher.decrypt(bytes(Str2))
print(pt)
