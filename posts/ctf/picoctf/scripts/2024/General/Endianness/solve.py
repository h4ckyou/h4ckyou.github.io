from pwn import *

io = remote("titan.picoctf.net", "63041")

io.recvuntil(b"Word: ")
word = io.recvline().strip()

little = [hex(i)[2:] for i in word[::-1]]
little_end = ''.join(little)

big = [hex(i)[2:] for i in word]
big_end = ''.join(big)

io.sendline(little_end.encode())
io.sendline(big_end.encode())

io.recvuntil(b"is: ")
flag = io.recvline()

info(flag)
io.close()
