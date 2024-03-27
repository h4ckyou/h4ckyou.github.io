from pwn import *

context.log_level = 'debug'

io = process("./guessing_game.sh")

io.recvline()

def binarySearch(N):
    left, right = 0, N

    io.recvline()

    while left <= right:
        middle = left + (right - left) // 2

        io.sendline(str(middle))
        
        recv = io.recvline().decode().split()[0]

        if recv == "Lower!":
            right = middle - 1

        elif recv == "Higher!":
            left = middle + 1

        else:
            recv = io.recvline()
            return recv.decode()


N = 1000

binarySearch(N)

io.interactive()
