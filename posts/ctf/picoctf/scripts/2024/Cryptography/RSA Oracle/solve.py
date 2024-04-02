from pwn import *
from Crypto.Util.number import long_to_bytes
from warnings import filterwarnings

io = remote("titan.picoctf.net", 61923)
filterwarnings("ignore")

io.sendline("E")
io.sendline(p8(0x2))
io.recvuntil("n) ")

ct1 = int(io.recvline().decode())
ct2 = 2575135950983117315234568522857995277662113128076071837763492069763989760018604733813265929772245292223046288098298720343542517375538185662305577375746934
C = ct1 * ct2
# print(ct1)
# print(ct2)

io.sendline("D")
io.sendline(str(C))

io.recvuntil(": ")
pt = long_to_bytes(int((io.recvline().decode().split()[-1]), 16) // 2)
print(f"AES Password: {pt}")

io.close()
