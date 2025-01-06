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

This means there's no UAF bug (Use After Free) present.






