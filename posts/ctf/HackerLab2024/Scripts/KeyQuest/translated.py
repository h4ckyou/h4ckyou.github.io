from dis import dis
from hashlib import md5, sha1
import string

def hint():
    hint = "\n  password = whippin3(key)(real_password) to keep real_password safe\n  so crypted_password = dpjLgviGRJJN1IUUFeKu1ls8\n  I deleted real_password from this check function\n  "
    print(hint)
    
def whippin5(inpt):
    sh = md5()
    sh.update(inpt)
    return sh.hexdigest()

def whippin3(n):
    lc = string.ascii_lowercase
    uc = string.ascii_uppercase
    dc = string.digits
    
    trans = str.maketrans(
        lc + uc + dc,
        lc[n:] + lc[:n] + uc[n:] + uc[:n] + dc[n:] + dc[:n]
    )
    print(trans)

    return lambda s: str.translate(s, trans)

def whippin4(a, b):
    b_etx = len(a) // len(b) + 1

    return b''.join(
        chr(c ^ d).encode() for c, d in zip(a.encode(), (b * b_etx).encode())
    )

def check(username, y_key):
    real_password = ""
    
    if whippin5(whippin4(username, real_password)) == y_key:
        if username == 'BJIZ-HACKERLAB':
            print('Congratz, you can use this flag to validate : HLB2024{' + y_key + '}')
        else:
            print("Good, but the key of BJIZ-HACKERLAB' is the flag")
    else:
        print('Error, checking failed')

hint()
