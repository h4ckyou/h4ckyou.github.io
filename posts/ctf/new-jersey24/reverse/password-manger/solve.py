enc = [79, 70, 81, 67, 94, 82, 77, 22, 87, 22, 86, 122, 72, 101, 92, 101, 26, 88]
key = 0x25
flag = [i ^ key for i in enc]

print("".join(map(chr, flag)))
