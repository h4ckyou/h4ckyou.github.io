import hashlib
import base64
import zlib 

def gen(a):
    v3 = [0]*4
    for i in range(4):
        v3[i] = (a >> (8 * i)) & 0xff

    cstr = ""
    for j in v3:
        cstr += chr(j)

    return zlib.crc32(cstr.encode()) & 0xffff
    
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

username = b"BJIZ-HACKERLAB"
odd = gen_hash(username)
inp = b"3D88-9387-BC59-29FE-9609-6347"

r = xor(inp, odd)


with open("data", "wb") as f:
    f.write(username)
    f.write(b'\n')
    f.write(base64.b64encode(r.encode()))
    f.close()


# array = [1, 894, 1, 298, 447, 799236, 1, 223, -178, -1, 0, 1788]


i = 0
start = array[2 * i]
end = array[2 * i + 1]
# print([start, end])
chunk = {}

for j in range(start, end + 1):
    value = hex(gen(j ^ 0x37E))[2:].upper()

    if value in chunk:
        chunk[value] += 1
    else:
        chunk[value] = 1


for i, j in chunk.items():
    if j == 1: 
        print(i)
        break

print("\n")

# o = 0

# for i in range(256): # compute[1]
#     for j in range(256): # compute[2]
#         for k in range(256): # compute[3]
#             for l in range(256): # compute[4]
#                 for m in range(256): # compute[5]
#                     if (o * l + j  == (m + (5 * i) - k)):
#                         if (o + j < 1788):
#                             if (m - i * j < 895):
#                                 print([1, i, j, k, l, m])
                                # break

# 0 * compute[4] + compute[2] == (compute[5] + (5 * compute[1]) - compute[3])
# 0 + compute[2] < 1788
# compute[5] - compute[1] * compute[2] < 895        
# compute = [5, 5, 5, 5, 5, 5] works! but can't be exactly the generated crc values
        
# compute = [1, 1, 5]
# x == 0 + 5*1
# x == 5

# - https://www.openssl.org/docs/manmaster/man3/BIO_new_mem_buf.html
# - https://www.openssl.org/docs/man1.1.1/man3/BIO_f_base64.html
# - https://github.com/openbsd/src/blob/master/include/regex.h#L61

