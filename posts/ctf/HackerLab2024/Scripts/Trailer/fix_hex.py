with open('data', "r") as f:
    file = f.read().strip()

chunks = []

for i in range(0, len(file), 4):
    byte = file[i:i+4]
    first = byte[0:2]
    last = byte[2:4]
    chunks.append(last+first)


hex_string = "".join(chunks)

with open("chall.jpg", "wb") as f:
    f.write(bytes.fromhex(hex_string))
