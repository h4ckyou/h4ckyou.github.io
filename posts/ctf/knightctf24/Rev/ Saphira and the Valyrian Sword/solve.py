from pwn import *
from warnings import filterwarnings
filterwarnings("ignore")

def generate(v6):
    v3 = 0
    a1 = v6

    while a1 > 0:
        v3 = 10 * v3 + a1 % 0xa
        a1 //= 0xa

    print(f"[v3, {v3}]")

    return v3

def transform(timestamp, user):
    user = user
    v3 = 0
    for i in range(len(user)):
        v3 += user[i]
    
    
    v6 = 0
    v7 = 1
    i = timestamp

    while i > 0:
        v5 = i % 10
        v6 += v7 * (v3 ^ v5)
        v7 *= 10
        i //= 10
    
    print(f"[v6, v7] = [{v6}, {v7}]")

    return timestamp ^ generate(v6)
    
io = remote("198.58.104.183", "21337")
context.log_level = "info"

io.recvuntil("known as ")
name = io.recvline().split()[0][:-1]

io.recvuntil("had slain ")
timestamp = int(io.recvline().split()[0])

print([name, timestamp])

password = transform(timestamp, name)

io.recvuntil("password:")
io.sendline(str(password))

print(io.recvall())

# KCTF{k1LL_tHE_Saphira_dRAgon_wITH_thE_sWORD} #
