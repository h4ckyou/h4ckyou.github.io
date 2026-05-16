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

Executing the binary doesn't reveal much on the program's behavious

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
