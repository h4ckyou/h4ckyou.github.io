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

Loading it up in IDA Pro, here's the disassembly:

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

void __fastcall recall(mem_t *mem)
{
  fwrite(mem, mem->count, 1uLL, stdout);
  fflush(stdout);
}

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

The main function first allocates a heap chunk using `calloc`. If the allocation succeeds, it reads user input into this chunk, up to a maximum of 0x20 bytes, matching the allocated size.

As input is processed, it checks for the closing brace `}` and validates the beginning of the flag against the flag format prefix `HTB{`. If the check passes, it sets `v6.count` to `0LL` and sets `v6.data` back to the start of the `mem_t` structure.

After this initialization, the loop function is invoked with a pointer to the `mem_t` structure.

The program then enters a while (true) loop, continuously reading input until `EOF (-1)` is encountered. Once `EOF` is received, the loop terminates and the program exits.

There are three main components that make up the program's loop functionality: `remember`, `recall`, and `reset`.

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

The `remember` function takes a pointer to a `mem_t` structure as its argument. It first reads a user-controlled value `c` using `fgetc()` and checks whether it is less than or equal to 24.

If the check passes, the function enters a loop that iterates `c` times. During each iteration, a byte is read from `stdin` and written to the buffer pointed to by `mem->data`, provided that `mem->count` is less than or equal to 24.

After every successful write:
- `mem->data` is incremented
- `mem->count` is incremented

The loop continues until `c` reaches 0.

The `recall` function takes a pointer to a `mem_t` structure as its argument and prints the contents stored in the structure up to `mem->count` bytes.

```c
void __fastcall recall(mem_t *mem)
{
  fwrite(mem, mem->count, 1uLL, stdout);
  fflush(stdout);
}
```

The `reset` function restores the internal state of the `mem_t` structure by reinitializing both its counter and data pointer:

```c
void __fastcall reset(mem_t *mem)
{
  mem->count = 0LL;
  mem->data = (char *)mem;
}
```

It sets `mem->count` to 0, effectively clearing any recorded length, and resets `mem->data` to point back to the beginning of the `mem_t` structure itself.


### Exploitation

As you might have already seen, there's not much this program has to offer..

The vulnerability is fairly straightforward:
- an off-by-one write
- a signedness bug in input validation

What can we do with the off-by-one write?

Well, recall the `mem_t` structure:

```c
struct mem_t {
  char v6[24];
  long count;
  char *data;
}
```

With an off-by-one we can corrupt the `count` field of the structure.

How useful and exploitable is this though? After all, the program does ensure that count never exceeds 24.

Well, the interesting part is that the program increments `mem->data` after every write:

```c
*mem->data++ = v2;
```

This means that if we somehow manage to make `mem->data` point to itself (&mem->data), we can start partially overwriting the pointer itself and gain control over where future writes go.

At that point, we essentially get writes on the stack, which leads directly to memory corruption.

Thinking about it, there are two major problems we run into:
- we can only read up to `c` times, and there's a check ensuring it doesn't exceed 24
- once `count` becomes greater than 0x18, the program stops writing to `data`

That's where the actual vulnerability comes into play.

There's a signedness bug during input validation:

```c
char c; // [rsp+7h] [rbp-9h]

c = fgetc(stdin);
if ( c <= 24 )
{
  while ( c-- ) {...}
}
```

`c` is defined as a signed char, meaning its range is `-128` to `127`.

Because of this, values such as `-128` still satisfy the condition:

```c
c <= 24
```

And this allows the loop to iterate far more times than intended.

Why this matters is because, to perform the final partial overwrite on `mem->data`, we need a total of 33 bytes to be processed..something that normally shouldn't be possible with the 24 byte limit in place.

