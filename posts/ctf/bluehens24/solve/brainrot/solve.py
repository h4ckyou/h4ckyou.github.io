from pwn import xor

flag = bytearray(51)
prefix = b"udctf{"
suffix = 0x7d

for idx, val in enumerate(prefix):
    flag[idx] = val

flag[len(flag) - 1] = suffix

fanum = [0x47, 0x4a, 0x13, 0x42, 0x58, 0x57, 0x1b]
cmp1 = b"r!zz13r"
simp = xor(fanum, cmp1)
flag[29:29 + len(simp)] = simp

cmp2 = b"5ki8idi"
vibe = xor(fanum, cmp2)
flag[43:43 + len(cmp2)] = vibe

woke = [0x40,0x05,0x5c,0x48,0x59,0x0f,0x5a,0x5b,0x00]
drip = xor(woke, cmp2)
flag[15:15 + len(woke)] = drip

zest = [0x62,0x6e,0x60,0x75,0x69,0x34]
clout = [(i - 1) for i in zest]
flag[8:8 + len(zest)] = bytes(clout)

lose = [0x05,0x17,0x01,0x01,0x1d,0x00]
snack = xor(lose, zest)
flag[37:37 + len(lose)] = snack

flag[26] = flag[44]
flag[6] = flag[31]
flag[7] = flag[10]
flag[14] = ord("_")
flag[28] = flag[14]
flag[36] = flag[14]
flag[23] = flag[14]
flag[42] = flag[14]
flag[24] = flag[19]
flag[27] = flag[24]
flag[25] = ord("h")

for i in range(len(flag)):
    if flag[i] == 0:
        print(i)

print(flag.decode()) 
