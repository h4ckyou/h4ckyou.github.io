import string
from pwn import *
import ast

charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "{}_"
enc_str = open("flag.txt").read().split()
enc = [int(item) for item in enc_str]
flag = ""


io = process("./re-incarnation")
io.sendline(charset.encode())
io.recvuntil(b": ")
r = io.recvall().splitlines()
io.close()

numbers = [int(item.strip()) for item in r if item != b""] 
mapping = {num: char for char, num in zip(charset, numbers)}
flag = ""

for val in enc:
    flag += mapping[val]

print(flag)
