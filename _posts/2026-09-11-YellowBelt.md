---
title: Gaining the Yellow Belt @ Pwn.College
date: 2026-09-11 20:38:00 +0100
categories: [Blog]
tags: [pwnable]
math: true
mermaid: true
media_subpath: /assets/posts/2026-09-11-yellow-belt
image:
  path: preview.png
---

## Program Security

### Overview

Over the past few years I've been studying pwn/re occasionally, using [pwn.college](https://pwn.college/) as my main platform of study.

I won't go into detail about what made me start studying binary exploitation (aka pwn), but I pretty much enjoy doing it.

I worked on completing the **Program Security** dojo, which gives you the **Yellow Belt**.

I recommend completing this without AI of course (the challenge solving), the goal is to understand, and to do so well. Trust me, pwn.college is painful, but definitely worth it.

In total, I solved *159* challenges ranging across:
- Shellcoding
- Memory corruption
- Crackmes
- Patching
- Custom Virtual Machine reversing & exploitation
- Return Oriented Programming (ROP)
- Stack Pivoting
- Glibc's allocator exploitation
- Use After Free
- Metadata corruption

I actually finished the majority of these challenges months ago, but was left with 2 more REs.

Those were tough. The Yan85 VM gave me trouble ngl, but in the end it was worth breaking it.

Pwn.college is a really good resource for studying. I like the fact that the challenges at the end are usually tougher.

Here's an example:

```c
00000000 struct registers // sizeof=0x7
00000000 {                                       // XREF: context/r
00000000     uint8_t r1;
00000001     uint8_t r2;
00000002     uint8_t r3;
00000003     uint8_t r4;
00000004     uint8_t sp;
00000005     uint8_t pc;
00000006     uint8_t flags;
00000007 };

00000001 typedef unsigned __int8 uint8_t;        // XREF: registers/r
00000001                                         // registers/r ...

00000000 struct context // sizeof=0x407
00000000 {                                       // XREF: main/r
00000000     char mem[256];
00000100     char code[768];
00000400     registers regs;
00000407 };

int __fastcall interpret_sys(context *vm, __int16 args)
{
  const char *v2; // rax
  unsigned __int8 v3; // al
  unsigned __int64 r3; // rax
  unsigned __int8 v5; // al
  unsigned __int64 v6; // rax
  unsigned __int8 v7; // al
  unsigned __int8 v8; // al
  int result; // eax
  int v10; // ebx
  const char *v11; // rax

  v2 = describe_register(HIBYTE(args));
  printf("[s] SYS %#hhx %s\n", args, v2);
  if ( (args & 2) != 0 )
  {
    puts("[s] ... open");
    v3 = sys_open(vm, &vm->mem[vm->regs.r1], vm->regs.r2, vm->regs.r3);
    write_register(vm, HIBYTE(args), v3);
  }
  if ( (args & 1) != 0 )
    crash(vm, "Disallowed system call: SYS_READ_CODE");
  if ( (args & 0x10) != 0 )
  {
    puts("[s] ... read_memory");
    r3 = vm->regs.r3;
    if ( 256 - vm->regs.r2 <= r3 )
      LOBYTE(r3) = -vm->regs.r2;
    v5 = sys_read(vm, vm->regs.r1, &vm->mem[vm->regs.r2], r3);
    write_register(vm, HIBYTE(args), v5);
  }
  if ( (args & 0x20) != 0 )
  {
    puts("[s] ... write");
    v6 = vm->regs.r3;
    if ( 256 - vm->regs.r2 <= v6 )
      LOBYTE(v6) = -vm->regs.r2;
    v7 = sys_write(vm, vm->regs.r1, &vm->mem[vm->regs.r2], v6);
    write_register(vm, HIBYTE(args), v7);
  }
  if ( (args & 4) != 0 )
  {
    puts("[s] ... sleep");
    v8 = sys_sleep(vm, vm->regs.r1);
    write_register(vm, HIBYTE(args), v8);
  }
  if ( (args & 8) != 0 )
  {
    puts("[s] ... exit");
    sys_exit(vm, vm->regs.r1);
  }
  result = HIBYTE(args);
  if ( HIBYTE(args) )
  {
    v10 = read_register(vm, HIBYTE(args));
    v11 = describe_register(HIBYTE(args));
    return printf("[s] ... return value (in register %s): %#hhx\n", v11, v10);
  }
  return result;
}
```

Can you spot the bug in the code given above? If you can, then you've got some idea of how the last challenges usually are :)

> This is the handler for system calls in the VM.

After this, I plan on finishing the Blue Belt.. almost done with that haha... I've been a bit occupied with other stuff, which is why I haven't worked on it completely.

![done](done.png)
![preview](preview.png)

Thanks all for today!

ありがとうございます！😊