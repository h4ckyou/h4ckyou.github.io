import string
from hashlib import md5

def whippin4(a, b):
    b_etx = len(a) // len(b) + 1

    return b''.join(
        chr(c ^ d).encode() for c, d in zip(a.encode(), (b * b_etx).encode())
    )

def whippin5(inpt):
    sh = md5()
    sh.update(inpt)
    return sh.hexdigest()

def get_password():
    n = -9

    lc = string.ascii_lowercase
    uc = string.ascii_uppercase
    dc = string.digits

    rev_map = {}

    trans = str.maketrans(
        lc + uc + dc,
        lc[n:] + lc[:n] + uc[n:] + uc[:n] + dc[n:] + dc[:n]
    )

    for i, j in trans.items():
        rev_map[chr(j)] = chr(i)

    txt = "dpjLgviGRJJN1IUUFeKu1ls8"
    pwd = ""

    for i in txt:
        pwd += rev_map[i]

    return pwd

username = "BJIZ-HACKERLAB"
real_password = get_password()

print(real_password)

op1 = whippin4(username, real_password)
flag = "HLB2024{" + whippin5(op1) + "}"
print(flag)
