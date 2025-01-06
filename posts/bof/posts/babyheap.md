<h3> Pwn Writeup </h3>

- BabyHeap (Dcquals 2019)
- File: [chall](https://github.com/guyinatuxedo/nightmare/tree/master/modules/29-tcache/dcquals19_babyheap)

Hi there, recently i've been trying to learn more on heap exploitation so i decided to make a writeup on how i was able to solve this challenge

#### Recon

We are given a binary and it's libc
![image](https://github.com/user-attachments/assets/57f89f86-3dca-4480-aa0f-3d5944d3624e)

The first thing I always do is patch the binary to use the provided libc. This ensures that I am working with the correct version, which matches the one used on the remote instance.
![image](https://github.com/user-attachments/assets/8928dfa7-3b12-4f11-94ec-22d2c7a198d7)

```
cmd: pwninit --bin babyheap --libc libc.so.6 --no-template
```

Now time to start, first i'll check the type of file i'm working with then the protections enabled.
![image](https://github.com/user-attachments/assets/f6c615a4-5c93-4d5f-ba55-6d788f790af1)

As you can see from the image above, we are working with a 64 bits executable and it has all protections enabled (sheesh!).

We also need to know the libc version we're working with
![image](https://github.com/user-attachments/assets/69602119-9485-4907-8451-5383c8733a1d)

This is `glibc 2.29` 

Running it we get this four options which we can choose from
![image](https://github.com/user-attachments/assets/928c903a-a01f-4b3d-8154-bba8c28d7d5d)

Time to fire up IDA to reverse this

```
Note: the binary was stripped so i had already renamed variables, data types, function names
```

#### Reverse Engineering

Loading it up in IDA, here's the main function

![image](https://github.com/user-attachments/assets/2b17f6c9-1ca5-4160-911e-d0d810f777d5)

```c
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 1, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  challenge();
}
```

Nothing much, it just disables buffering on `stdin, stdout & stderr` then it calls the `challenge` function

This is the `challenge` function

![image](https://github.com/user-attachments/assets/c5016285-9877-49a0-b194-083fd2e55443)
![image](https://github.com/user-attachments/assets/8f0160e2-8cf8-4212-981f-a64a60e0a19d)

From this, we can see that based on our choice, which can be either `M, F, S, or E`, it calls the corresponding function:
- allocate_memory()
- free_memory()
- show_memory()
- exit()

Our main goal is to work with the first 3 options since exiting at this point is of no use to us.

Function `allocate_memory()`:

![image](https://github.com/user-attachments/assets/10b3ff4e-f584-4f1f-8ad7-8c94e8c0892d)
![image](https://github.com/user-attachments/assets/531fcf52-53ac-477c-890f-703abce675f4)

```c
__int64 allocate_memory()
{
  _QWORD *v0; // rax
  unsigned int idx; // ebp
  uint32_t size; // r12d
  __int64 i; // rbx
  Heap *mem; // rbp
  char buf; // [rsp+7h] [rbp-21h] BYREF
  unsigned __int64 v7; // [rsp+8h] [rbp-20h]

  v7 = __readfsqword(0x28u);
  if ( ptr[0].content )
  {
    v0 = &global_var;
    for ( idx = 1; ; ++idx )
    {
      v0 += 2;                                  // somewhat keeps track of the idx to use!
      if ( !*(v0 - 2) )
        break;
    }
    if ( idx > 9 )
      return 0xFFFFFFFDLL;
  }
  else
  {
    idx = 0;
  }
  __printf_chk(1, "Size:\n> ");
  size = read_num();
  if ( size - 1 > 0x177 )
    return 0xFFFFFFFDLL;
  if ( size <= 0xF8 )
    ptr[idx].content = malloc(0xF8uLL);
  else
    ptr[idx].content = malloc(0x178uLL);
  if ( !ptr[idx].content )
    return 0xFFFFFFFDLL;
  ptr[idx].size = size;
  __printf_chk(1, "Content:\n> ");
  read(0, &buf, 1uLL);
  i = 0LL;
  mem = &ptr[idx];
  while ( buf != '\n' && buf )
  {
    mem->content[i] = buf;
    read(0, &buf, 1uLL);
    if ( size == i )
      return 0LL;
    ++i;
  }
  return 0LL;
}
```

The allocate_memory function does this:
- Get's the `idx` which is used to reference where it stores our data on the global variable `ptr`
- Reads in the size and makes sure it isn't greater than `0x177`
- If the size is less than or equal to `0xF8` it will allocate a dynamic memory via a call to `malloc()` of size `0xF8` else it allocates a dynamic memory of size `0x178`

Note that the global variable is of type Heap, which is a struct I defined myself.

```c
struct Heap {
char *content;
int size;
}

Heap ptr[10];
```

Moving on:
- It would set `ptr[idx].size` to our provided `size` and also `ptr[idx].content` to the address returned by the call to `malloc`
- Then it reads into `ptr[idx].content` some data until it meet's a new line or the number of bytes we've read in so far equals the size we provided

It looks all good but there's actually a vulnerability here:
- Off by one

```c
  read(0, &buf, 1uLL);
  i = 0LL;
  mem = &ptr[idx];
  while ( buf != '\n' && buf )
  {
    mem->content[i] = buf;
    read(0, &buf, 1uLL);
    if ( size == i )
      return 0LL;
    ++i;
  }
```

From the code above, we can see that `i` is set to `0` but the check is actually comparing `i` to `size`, since indexing of an array starts at `0` the comparism should have been `if (size - 1 == i)`

This leads to a one byte heap overflow hence off by one

Function `free_memory()`:

![image](https://github.com/user-attachments/assets/9ff2b232-b349-4d7f-a91f-a0557bd1d01f)

```c
__int64 __fastcall free_memory()
{
  unsigned int num; // eax
  __int64 idx; // rdx
  char *content; // rdi
  Heap *addr; // rbx

  puts("(Starting from 0) Index:\n> ");
  num = read_num();
  if ( num > 9 )
    return 0xFFFFFFFCLL;
  idx = num;
  content = ptr[idx].content;
  if ( !content )
    return 0xFFFFFFFCLL;
  addr = &ptr[idx];
  memset(content, 0, ptr[idx].size);
  free(addr->content);
  addr->size = 0;
  addr->content = 0LL;
  return 0LL;
}
```

The free_memory function does this:
- Receives the `idx` to use to access the `ptr` array
- If `ptr[idx].content` isn't null (i.e it contains a heap chunk), it zero's out `ptr[idx].size` then it frees `ptr[idx].content`
- After that is done, it clears out the pointer and the size that corresponds with the freed index

The implementation here is correct because after free'ing it null's out the memory address stored in the variable.

This means there's no UAF bug (Use After Free).

Function `show_memory()`:

![image](https://github.com/user-attachments/assets/d0f33bc2-a5a5-451a-a690-76292cab87ce)

```c
__int64 __fastcall show_memory()
{
  unsigned int idx; // eax
  char *content; // rdi

  __printf_chk(1, "(Starting from 0) Index:\n> ");
  idx = read_num();
  if ( idx > 9 )
    return 0xFFFFFFFBLL;
  content = ptr[idx].content;
  if ( !content )
    return 0xFFFFFFFBLL;
  puts(content);
  return 0LL;
}
```

The show_memory function does this:
- Based on the `idx` received it checks if `ptr[idx].content` isn't null
- Then it prints out the value stored in `ptr[idx].content`

So based on this we can tell this would probably be used as a read primitive to get leaks!

#### Exploitation

Based on the reverse engineering we've done we know that:
- We have a one byte heap overflow
- Maximum chunks that can be allocated is 10
- Ability to free a chunk
- Ability to print a chunk

First thing we would want is getting info leaks specifically libc!

Tcache was introduced in libc version 2.26

Each thread has a per-thread cache (called the tcache) containing a small collection of chunks which can be accessed without needing to lock an arena. These chunks are stored as an array of singly-linked lists, like fastbins, but with links pointing to the payload (user area) not the chunk header. Each bin contains one size chunk, so the array is indexed (indirectly) by chunk size. Unlike fastbins, the tcache is limited in how many chunks are allowed in each bin (tcache_count). If the tcache bin is empty for a given requested size, the next larger sized chunk is not used (could cause internal fragmentation), instead the fallback is to use the normal malloc routines i.e. locking the thread’s arena and working from there. [source](https://sourceware.org/glibc/wiki/MallocInternals#Thread_Local_Cache_.28tcache.29).

Based on how the ptmalloc allocator works, this is the algorithm used when allocating memory:
![image](https://github.com/user-attachments/assets/e5cedcf6-4e21-4ae9-904b-51154c5dc183)

And this is free algorithm
![image](https://github.com/user-attachments/assets/71d6d117-075b-4d63-94c8-e8b3ea308b32)

In a nutshell, free works like this:
- If there is room in the tcache, store the chunk there and return.
- If the chunk is small enough, place it in the appropriate fastbin.
- If the chunk was mmap'd, munmap it.
- See if this chunk is adjacent to another free chunk and coalesce if it is.
- Place the chunk in the unsorted list, unless it's now the "top" chunk.
- If the chunk is large enough, coalesce any fastbins and see if the top chunk is large enough to give some memory back to the system. Note that this step might be deferred, for performance reasons, and happen during a malloc or other call.

We would leverage how free works to place a chunk into the unsorted bin and the reason for doing that is if a freed chunk is the only chunk in unsorted bin, then it will hold a pointer to an arena. But in our program, there’s only 1 arena — the main arena. So we get a pointer to some fixed offset in libc.

To do that, we need to make an allocation such that, when freed and the tcache is filled up, it won't be small enough to be placed into the fastbin.

The fastbin holds freed chunk between size of `0x20 - 0x80` and by default the tcache list will only hold seven entries, which we can see in the [malloc.c](https://elixir.bootlin.com/glibc/glibc-2.29/source/malloc/malloc.c#L323) source code from this version of libc:

```c
#if USE_TCACHE
-------------------------------------------------------
....................Truncated .........................
-------------------------------------------------------
/* This is another arbitrary limit, which tunables can change.  Each
   tcache bin will hold at most this number of chunks.  */
# define TCACHE_FILL_COUNT 7
#endif
```

Since the size that can be allocated by the program is either `0xF8 | 0x177` this means if we make 8 allocations of size `0xF8` and then free it:
- 7 chunks will be placed in the tcache bin
- 1 chunk will be placed in the unsorted bin

But with that how do we get leak? Well if after getting a chunk into the unsorted bin the fd & bk will be pointing to the main_arena struct

```c
struct malloc_chunk {

  INTERNAL_SIZE_T      mchunk_prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */

  struct malloc_chunk* fd;         /* double links -- used only if free. */
  struct malloc_chunk* bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};

```

And if we reallocate it back we would get the chunk which was freed, only if the chunk which we are attempting to allocate is of the same size as the freed chunk

Also take note that the data structure used by the Tcache is (Last In First Out := LIFO)

This means if we get the chunk which was previously holding pointers to the libc region we can just set the first 8 bytes to some value and then when we use the `show_memory` function it would print out the data given + the pointer to the `main_arena`

That works because `puts()` will keep on printing until it meets a null terminator

Here's my poc for getting info leak:

```python
def solve():

    for i in range(10):
        allocate(0xf8, b"\x41" * 8)
    
    for j in range(9, -1, -1):
        free_memory(j)
    
    for i in range(10):
        allocate(0xf8, b"\x42" * 8)

    show_memory(7)
    io.recvuntil(b"B" * 8)
    main_arena = u64(io.recvline().strip().ljust(8, b"\x00")) - 0x350
    libc.address = main_arena - libc.sym["main_arena"]
    info("libc base: %#x", libc.address)
```











