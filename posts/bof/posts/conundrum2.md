<h3> Conundrum 2 </h3>

Hi there, some months ago I was given some set of challenges made by `mug3njutsu` for a ctf he wrote challenges for but it got no solve
![image](https://github.com/user-attachments/assets/fa8fff24-d0ed-4eeb-8872-0e5d51771af0)

So I decided to tackle them and was able to solve 3/4 of the challenges for which i made a solution [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/writeup.md)

The last one i wasn't able to do it
![image](https://github.com/user-attachments/assets/4fa437ad-10f4-4fa1-8a08-0adb088bb05f)

At that time i wasn't so much familiar with various techniques so i thought it was a format string one shot sort of exploitation (maybe that's still possible im just not that good yet! 😅)

I still had the challenge file saved and while scrolling through challenges i should tackle today i came across it and decided to give it a shot
![image](https://github.com/user-attachments/assets/9ca2ec2f-51ab-44fc-bcd2-f722bb76d09b)

Now then let's start :)

The challenge came with its glibc file and linker, so the first thing I did was patch it to ensure the same libc would be used on my device as on the remote
![image](https://github.com/user-attachments/assets/830a5e52-5eb0-4b59-95ee-93970a7e6747)

```
pwninit --bin conundrum_v2 --libc libc.so.6 --ld ld-linux-x86-64.so.2 --no-template
```

Next thing is to get an idea as to what type of file we are working with and the protection enabled on it
![image](https://github.com/user-attachments/assets/570f7798-cc6b-48b7-9852-b1ebbb85cd9f)

We can see that it is a 64 bits executable which is dynamically linked and not stripped and from the protections enabled it's clear that only the stack canary is disblaed

Now i ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/9a53e7ee-9c3d-46bc-9525-584b49ec9b4b)

It seems to print some menu, receives our choice and based on the choice provided does some other stuffs

With that in mind it's time to figure out the vulnerability

Using IDA (ofc) i decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/23f960fc-1c0e-4062-9810-c87c3c442909)

First it calls the `setup` function which disables buffering on `stdout`
![image](https://github.com/user-attachments/assets/9a50f60a-ddd6-41a8-beea-6f7a49c1c440)

Then it prints out some text which is the menu thingy

After that it reads in our input and checks this:
- If we give it 1 it would exit
- If we give it anything aside 1 or 2 it would exit
- If we give it 2 it would call the `question` function

We now know that our vulnerability lies in the question function. Here's the decompiled code
![image](https://github.com/user-attachments/assets/2c344559-3806-468e-a7eb-35d77d93f330)

```c
int question()
{
  char s[128]; // [rsp+0h] [rbp-80h] BYREF

  memset(s, 0, sizeof(s));
  write(1, "Educate me, what's so interesting about pointers: ", 0x32uLL);
  read(0, s, 0x8CuLL);
  return printf(s);
}
```

It looks awfully small :) 

From this we know that:
- It would clear up the buffer `s` up to 128 bytes filling it with null bytes
- Prints out some texts
- Receives our input which is stored in s
- Prints out input
- Returns the number of bytes returned from calling `printf`

Ok good so the bug is pretty obvious:
- We have a buffer overflow
- And a format string bug

The buffer overflow occurs because we are reading up to 140 bytes into the buffer, while the buffer `s` can hold only a maximum of 128 bytes

Additionally, there is a format string vulnerability (FSB) because the code uses `printf` on `s` without specifying a format string

But looking at the overflow we can see that we can't fully control the return address due to the fact that we have only 4 bytes overwrite

```
140 - 128 = 12
12 - 8 = 4 (8 bytes for the saved rbp)
4 bytes for the saved return address
```

Regardless of that we don't know the memory mapping of the binary itself due to `PIE` that means we need to leak it to be able to pivot around memory

Ideally we could exploit the fsb to get code execution but that requires multiple arbitrary write and this is not the case since we only have one shot to calling `printf`

So what now?

Well this is how i went around this

First we need memory leaks and that's really important and i leveraged the fsb for that

But thinking further we also need a way to call the `question` function again if possible multiple times 

What do i mean, well we could get memory leaks using the fsb but here's what happens
![image](https://github.com/user-attachments/assets/f4043d82-0852-40eb-83b9-6ca0cf9cc801)

See!!, it would just exit so this means we have to call the `question` function again and to do that i leveraged a partial overwrite using the overflow

Here's what i mean, before the function is about to return this is how the memory looks like
![image](https://github.com/user-attachments/assets/5c65bfd6-c44c-459f-bde5-c0a044f31580)

```
pwndbg> x/50gx $rsp
0x7ffc5281c090:	0x4141414141414141	0x0000000000000000
0x7ffc5281c0a0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c0b0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c0c0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c0d0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c0e0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c0f0:	0x0000000000000000	0x0000000000000000
0x7ffc5281c100:	0x0000000000000000	0x0000000000000000
0x7ffc5281c110:	0x00007ffc5281c130	0x000055f4a360094d
```

Basically this is the stack view
![image](https://github.com/user-attachments/assets/f87e96df-17cf-43a1-b6f3-438c889b7187)

```
buffer -> saved rbp -> return address
```

We can see that the binary is actually going to return back to `0x000055f4a360094d` and that points to `main+114`
![image](https://github.com/user-attachments/assets/71c866f6-2b79-476a-a803-b3d6e2d4db7f)

So our goal is that instead of overwritting the 4 bytes of the return address we would overwrite just the lsb 
![image](https://github.com/user-attachments/assets/1cffe83a-6a8d-4914-a205-11dcff298b82)

I looked for a suitable offset to target, and `main+134` seemed to be the best choice because it zeros out the eax register and calls the question function

Why is this the best choice, you might ask? The reason is simply that it falls within the same address range as the address the question function returns to

We could have considered jumping back to main, but that would require nibble-level brute-forcing. This is because, even if the last 3 nibbles of an address are the same, the upper bytes are randomized due to ASLR and PIE

It's best to avoid brute-forcing in order to make the exploit more reliable

With that in mind, our goal becomes straightforward:
- Fill the buffer
- Overwrite the saved rbp
- Overwrite one byte of the return address to point to `main+134`

However, we won’t simply fill the buffer with junk. Instead, we’ll use some format string specifiers such that after it's passed to `printf` it would give us memory leaks

But what offset should we actually leak from because we can't spam the buffer with `%p.` though that works but i prefer not doing it that way because it could overwrite some pointers on the stack and those points might be important addresses mapping to libc, ld, etc















