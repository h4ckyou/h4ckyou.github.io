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


































