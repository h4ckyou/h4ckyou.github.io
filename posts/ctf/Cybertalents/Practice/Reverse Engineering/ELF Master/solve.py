array = [0xC6A9DDE2FEF8F5FF, 0xD5C6F2A9A9D5C6A8, 0xAAC6F7ADC6AAF2A8, 0xAAEDEAADD4C6DFD5, 0xE4EB]
key = 0x99
flag = ""

for i in range(len(array)):
    a = array[i].to_bytes((array[i].bit_length() + 7) // 8, byteorder='little')
    for j in a:
        flag += chr(j ^ key)
    
print(flag)
