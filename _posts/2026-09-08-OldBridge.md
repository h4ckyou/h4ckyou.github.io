---
title: Old Bridge
date: 2026-09-08 20:38:00 +0100
categories: [CTF, HackTheBox]
tags: [pwnable]
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

The program's code is really short and the vulnerability is obvious.

It in