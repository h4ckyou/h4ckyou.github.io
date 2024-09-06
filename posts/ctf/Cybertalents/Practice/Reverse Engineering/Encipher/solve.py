encrypted = "0a0c073c5a55072c117e442b0c60501627614efd"
key = 0x80
chunks = []

for i in range(0, len(encrypted), 2):
    chunks.append(encrypted[i:i+2])

flag = ""

for j in reversed(chunks):
    flag += chr(int(j, 16) ^ key)
    key = ord(flag[-1])

print(flag[::-1])
