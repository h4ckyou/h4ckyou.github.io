def decrypt(message):
    decrypted = ""
    for char in message:
        c = ord(char) ^ 23
        b = (c + 7) // 3
        a = (b - 5) ^ 42
        d = (a - 10) // 2
        decrypted += chr(d)
    
    return decrypted

with open('flag.txt.enc', 'r') as fp:
    flag = fp.read()

decoded = decrypt(flag)

print(decoded)
