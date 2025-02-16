"""
python print([int(gdb.parse_and_eval(f'*(int*)({hex(0x555555617750 + i*4)})')) for i in range(33)])
"""

import string

def isAlpha(a1):
    return (a1 > 96 and a1 <= 112) or (a1 > 64 and a1 <= 90)

def isLower(a1):
    return (a1 > 96 and a1 <= 112)

def isUpper(a1):
    return isAlpha(a1) & (not isLower(a1))

def valid(byte, val):
    if (byte == 123):
        return 125
    elif (byte == 125):
        return 123
    else:
        return val

def cipher(byte, idx):
    key = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
    val = byte + key[idx]

    if isLower(byte):
        shift = 122
    elif isUpper(byte):
        shift = 90
    else:
        shift = byte

    while (val > shift):
        val -= 26

    return valid(byte, val)

def decrypt(enc):

    charset = string.ascii_letters + "_{}"
    size = len(enc)
    result = [0] * size

    for i in range(size):
        for j in charset:
            data = cipher(ord(j), i)
            if data == enc[i]:
                result[i] = ord(j)
                break

    print(bytes(result))

    
expected = b"IQHR}nxio_vtvk_aapbijsr_vnxwbbmm{"
flag = decrypt(expected)

"""
FLAG{well_keep_training_yourself}
"""
