def sub_4006A5(byte, shift, key):
    v3 = (byte - shift - key)
    return (v3 % 26) + shift

def sub_40064D(v1, v2):
    if (v1 > 96 and v1 <= 122):
        return sub_4006A5(v1, 97, v2)
    elif (v1 <= 64 or v1 > 90):
        return v1
    else:
        return sub_4006A5(v1, 65, v2)

def sub_4006F3(a1, a2):
    v4 = (a1 >> (a2 & 0x1F)) | (a1 << (-(a2 & 0x1F) & 0x1F))
    return v4 & 0xFFFFFFFF

enc = [0x726F756E, 0x0CABEE660, 0x0DDC1997D, 0x0AA93C38B, 0x87E21216]
flag = b""

for i in range(5):
    var = sub_4006F3(enc[i], i)
    value = var.to_bytes(4)
    for j in range(4):
        v5 = sub_40064D(value[j], i)
        flag += bytes([v5])

print(flag)
