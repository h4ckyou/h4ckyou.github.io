---
title: Memento
date: 2026-05-16 03:00:00 +0000
categories: [CTF, HackTheBox]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-05-16-memento
image:
  path: preview.png
---

## HackTheBox - Memento

### Background

I decided to work on the **Memento** pwn challenge on **Hack The Box** after it was recommended, especially since it was set to retire in just two days.

At first, I wasn't planning to spend too much time on it, but once I started digging into the challenge, I got completely hooked. Surprisingly, it ended up taking me a little over a day to finally solve.

### Overview

**Memento** is a hard-rated pwn challenge built around exploiting a single off-by-one vulnerability to achieve memory corruption.

The bug is eventually leveraged into a stack pivot, giving full control over the program's execution flow through a fairly involved ROP chain.

Unlike typical pwn challenges where achieving RCE is the final objective, the real goal here is to leak the flag directly from memory, where it resides on the heap.

### Program Analysis

We are given just a single file called **memento** which is a 64-bits executable.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/Memento$ file memento
memento: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=839f13e7ce5e7e34f16549d8d2cee2ce2004c537, for GNU/Linux 4.4.0, not stripped
mark@rwx:~/Desktop/Labs/HTB/Challenges/Memento$ checksec memento
[*] '/home/mark/Desktop/Labs/HTB/Challenges/Memento/memento'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
mark@rwx:~/Desktop/Labs/HTB/Challenges/Memento$ 
```

All protections are enabled on this binary.

Executing the binary doesn't reveal much on the program's behaviour

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/Memento$ ./memento
asdf
ls
hello
lsls
mmm
c
^C
mark@rwx:~/Desktop/Labs/HTB/Challenges/Memento$ 
```

Loading it up in IDA Pro, here's the main function:

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 i; // [rsp+10h] [rbp-40h]
  int v5; // [rsp+18h] [rbp-38h]
  mem_t v6; // [rsp+20h] [rbp-30h] BYREF
  unsigned __int64 v7; // [rsp+48h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  v6.data = (char *)calloc(1uLL, 0x20uLL);
  if ( v6.data )
  {
    for ( i = 0LL; i < 0x20; ++i )
    {
      v5 = fgetc(stdin);
      if ( v5 == -1 )
        break;
      v6.data[i] = v5;
      if ( (char)v5 == '}' )
      {
        if ( !strncmp("HTB{", v6.data, 4uLL) )
        {
          v6.count = 0LL;
          v6.data = (char *)&v6;
          loop(&v6);
        }
        break;
      }
    }
    fputs("fatal: could not get flag\n", stderr);
  }
  else
  {
    fputs("fatal: could not alloc\n", stderr);
  }
  return 1;
}
```

`loop` function:

```c
void __fastcall __noreturn loop(mem_t *mem)
{
  int c; // [rsp+4h] [rbp-Ch]

  while ( 1 )
  {
    c = fgetc(stdin);
    if ( c == -1 )
      break;
    switch ( c )
    {
      case 'A':
        remember(mem);
        break;
      case 'B':
        recall(mem);
        break;
      case 'C':
        reset(mem);
        break;
      default:
        fputs(":(", stderr);
        break;
    }
  }
  fputs(":/", stderr);
  exit(2);
}
```

`remember` function:

```c
void __fastcall remember(mem_t *mem)
{
  char v2; // [rsp+0h] [rbp-10h]
  char c; // [rsp+7h] [rbp-9h]

  c = fgetc(stdin);
  if ( c <= 24 )
  {
    while ( c-- )
    {
      v2 = fgetc(stdin);
      if ( mem->count <= 0x18uLL )
      {
        *mem->data++ = v2;
        ++mem->count;
      }
    }
  }
}
```

`recall` function:

```c
void __fastcall recall(mem_t *mem)
{
  fwrite(mem, mem->count, 1uLL, stdout);
  fflush(stdout);
}
```

`reset` function:

```c
void __fastcall reset(mem_t *mem)
{
  mem->count = 0LL;
  mem->data = (char *)mem;
}
```

> `Note`: The shown pseudocode is what i already did reverse (the structure...)
{: .prompt-tip }

Here's the structure the program uses:

```c
00000000 struct mem_t // sizeof=0x28
00000000 {                                       // XREF: main/r
00000000     char v6[24];
00000018     __int64 count;                      // XREF: main:loc_14CC/w
00000020     char *data;                         // XREF: main+2B/w main+31/r ...
00000028 };
```

The main function allocates a heap chunk via a call to `calloc`, then if it succeeds, it reads in user input to the chunk of at most `0x20` bytes which matches the size passed to `calloc`. Once the character provided matches `}` it then goes ahead and compare it with the flag format `HTB{`.

If the check is successful, it's going to update `v6.count` to `0LL` and then `v6.data` to the start of the `mem_t` structure.
