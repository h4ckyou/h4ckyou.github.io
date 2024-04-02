from pwn import *

io = remote("titan.picoctf.net", 61923)

io.sendline("E")
io.sendline(p8(0x2))
io.recvuntil("n) ")
ct1 = int(io.recvline().decode())

with open("password.enc", "r") as fp:
    ct2 = fp.read()

print(ct1)
print(ct2)


io.interactive()
