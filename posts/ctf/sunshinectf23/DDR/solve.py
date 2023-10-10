from pwn import *
from warnings import filterwarnings 

def ddr(io):
    try:
        io.recvuntil(b'ENTER To Start --')
        io.sendline()
        io.recvline()
        io.recvline()

        for i in range(0xff+1):
            arrows = io.recvline().decode().strip()
            mapping = {
                '⇧': 'w',
                '⇦': 'a',
                '⇩': 's',
                '⇨': 'd'
            }

            result = ''
            for arrow in arrows:
                if arrow in mapping:
                    result += mapping[arrow]

            io.sendline(result)
            print(f"Current index: {i}")
            if i == 255:
                break

        print(io.recvline())
        print(io.recvline())
        print(io.recvline())

        io.close()
        
    except EOFError:
        pass

def start():
    io = remote('chal.2023.sunshinectf.games', '23200')
    context.log_level = 'info'
    filterwarnings("ignore")

    return io

if __name__ == '__main__':
    io = start()
    ddr(io)  
