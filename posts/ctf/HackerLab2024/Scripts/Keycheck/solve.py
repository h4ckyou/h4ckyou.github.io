from pwn import *

io = remote("135.125.107.236", "2300")
# io = process("./keygen1")
#context.log_level = 'debug'

io.recvuntil("username :")
io.sendline("BJIZ-HACKERLAB")

# io.recvuntil("key :")
io.sendline("V1IMVE4PBwkHGFB1BiRMBABxdRQKAwEAGlBVDFI=")

io.interactive()
