with open("xokambior.csv", "r") as file:
    bits = [line.strip() for line in file]

bit_str = bits[::31]
enc = "".join(bit_str)

flag = ""

for i in range(0, len(enc), 8):
    byte = enc[i:i+8]
    flag += chr(int(byte, 2))

print(flag)
