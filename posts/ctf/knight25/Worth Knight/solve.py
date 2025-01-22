import string
import itertools
import hashlib
from pwn import rol

flag = [0] * 10
flag[1] = 106
flag[0] = flag[1] ^ 36
flag[3] = 83
flag[2] = flag[3] ^ 56
flag[7] = 97
flag[6] = flag[7] ^ 56
flag[9] = 105
flag[8] = flag[9] ^ 32

charset = string.printable
match = "33a3192ba92b5a4803c9a9ed70ea5a9c"

for i in itertools.product(charset, repeat=2):
    value = ''.join(i)
    value = rol(value, 8)
    hashed = hashlib.md5(str(value).encode()).hexdigest()
    if hashed == match:
        flag[4] = ord(value[1])
        flag[5] = ord(value[0])
        print(bytes(flag)) 
