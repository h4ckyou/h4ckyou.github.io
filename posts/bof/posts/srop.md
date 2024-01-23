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
mov eax, 0x1
mov edi,0x1
movabs rsi,0x402000
mov edx, 0xf
syscall
```

So it moves `1` to the `eax` register and eventually it does a syscall

In Linux system calls (syscall) are the way that you can make requests from user space into the Linux kernel.

This case when you trigger a syscall it will lookup the rax/eax register as to what it's value is then get it's syscall name 

In our case since the `eax` register isn't modified before the first syscall that means it's attempting to call `write()`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4022b5e-375a-440a-8121-ddf76f7ce250)

You can check out the list of syscalls [here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit)

And because it want's to call `write()`, it needs to setup the registers needed for `write()` to work which are:
- RDI --> File Descriptor
- RSI --> Address of buffer
- RDX --> Size

So in our case it puts the value of `0x1` to the `edi` register (Note: `edi` is the 32bits representation of the `rdi` register) 

And `0x1` which is the file descriptor stands for `standard output -> stdout`

Then it moves the address of `0x402000` to the `rsi` register, that address would be pointing to a string of the binary which we can confirm by examining it's content from `gdb`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09426b6b-688d-4803-8e7e-4683c347b6d0)

```
0x402000:       "Hello, world!!\n/bin/sh"
```





























