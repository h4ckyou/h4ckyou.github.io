from pwn import *

def sell_cloth():
    io.sendline('2')
    io.sendline('y')
    io.sendline('2')
    io.sendline('y')

def idk():
    inp = [1, 5, 3, 0, 5, 2, 'y', 1, 1, 1, 3, 0, 0, 2]

    for i in inp:
        io.sendline(str(i))

def solve():
    idk()
    io.sendline('n')
    sell_cloth()

# io = process('./yooeyyeff')
io = remote('0.cloud.chals.io', '33146')
context.log_level = 'debug'

for i in range(25):
    solve()

io.sendline('4')

io.interactive()
