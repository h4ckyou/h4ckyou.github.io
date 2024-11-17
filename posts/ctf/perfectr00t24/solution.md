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

This is because a newline is sent with our filename and `fgets()` would read it therefore `open` would also attempt reading the filename which is already appended with a newline which is going to return -1 because such file doesn't exit

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

```
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

Here's my solve [script]()
![image](https://github.com/user-attachments/assets/a27f804c-a1e7-4069-88c7-c554e5eeb41a)


```
Flag: r00t{h34p_0v3rfl0w_1n_th3_f0rc3_1ebfe9e04a01ac4b00d4bd194b1bd505}
```













