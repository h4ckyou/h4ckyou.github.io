import hashlib
import base64

def xor(a, b):
    r = ""
    for i, j in zip(a, b):
        r += chr(i ^ j)
    
    return r

def gen_hash(a):
    value = hashlib.sha256(a).hexdigest()
    r = ""
    i = 0
    for j in range(len(value)):
        if (j & 1 != 0):
            r += value[j]
            if (i == 29):
                break

    return r.encode()


username = "BJIZ-HACKERLAB"
odd = gen_hash(username.encode())
key = "AAAA-AAAA-AAAA-AAAA-AAAA-AAAA".encode()

r = xor(odd, key).encode()
uh = xor(r, odd)

print(username)
print(key)
print(base64.b64encode(r))
