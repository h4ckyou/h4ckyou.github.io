<h3> ABCCTF Final 2023 Writeup </h3>

Hi everyone, in this writeup I'll give just the solution of the challenges which had one solve and was blooded by me

#### Reveal (Binary Exploitation)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/789b992c-9104-4523-a619-9ea9ce03de54)

We are given a netcat instance and a zip file 

After downloading the zip file and unzipping it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2670ce77-db25-450e-8845-2026d8e4a54e)

So it has a binary and it's libc file

Since this is given I patched the binary to use that libc because that's what going to be running on the remote instance 

I patched it using [pwninit](https://github.com/io12/pwninit)

Time to start the real deal here :P

Checking the file type and protections enabled on the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aceced47-955e-4550-afbc-bf821519ee24)

We're working with a x64 binary which is dynamically linked and not stripped

All protections are enabled on this binary 💀

I decided to run it to get an idea of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d5d288bc-4795-49a4-9123-5d50ce235321)

Cool it seems to receive our input twice

Inorder to find the vulnerability we need to decompile the binary

At first when I used Ghidra and viewed the main function I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9400b066-f28f-4c51-b6fa-bbfe9e0ee4b5)

```c

undefined8 main(void)

{
  undefined buffer [56];
  long canary;
  
  setup();
  canary = 0x13371337132763b7;
  write(1,
        "Tell me something thrilling and i\'ll share my dirty little secrets, nothing porn related t hough xD: "
        ,100);
  read(0,buffer,0x40);
  printf("You: %s",buffer);
  write(1,"Please, do tell me more, i\'m dying to find out: ",0x30);
  read(0,buffer,100);
  if (canary != 0x13371337132763b7) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

- Ok looking at that we can see that it assigns 56 bytes to a buffer and then it stores up a value in the `canary` variable and receives `0x40` bytes of our input which is stored in the buffer
- Our input is then put to stdout using `printf` 
- Then it receives 100 bytes of our input which is stored in the buffer
- It then compares the value stored in `canary` with `0x13371337132763b7`

From this there are two vulnerability:
- We can leak the canary value because the first input receives `0x40 (64)` bytes which is stored in the buffer and the buffer can hold up only `56` bytes so we have additional `8` bytes to overwrite (but this isn't all too good cause it can just overwrite the saved rbp) then later on the buffer is displayed using `printf` and one thing about `printf` is that it would print out until it meets a null byte. Since the buffer will be terminated with a null byte we can fill the buffer up so as to overwrite the null byte then `printf` will keep on printing till it meets a new null byte and eventually it would actually leak the next value on the stack which happens to be the canary
- There's a buffer overflow in the second input cause we are reading `100` bytes to a buffer which can only hold up `56` bytes

With that said what can we do with this?

Well normally even if we can leak the canary we are still limited cause PIE is enabled so ROP isn't an option 

It almost seemed impossible until I looked at the assembly decompilation in ghidra and saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8371616f-80a6-478c-8f50-028ff3d5a479)

```
   0x00000000000011e6 <+4>:     push   rbp
   0x00000000000011e7 <+5>:     mov    rbp,rsp
   0x00000000000011ea <+8>:     sub    rsp,0x40
   0x00000000000011ee <+12>:    mov    eax,0x0
   0x00000000000011f3 <+17>:    call   0x11b9 <setup>
   0x00000000000011f8 <+22>:    mov    rax,QWORD PTR [rip+0x2de1]        # 0x3fe0
   0x00000000000011ff <+29>:    mov    rdx,rax
   0x0000000000001202 <+32>:    movabs rax,0x1337133713371337
   0x000000000000120c <+42>:    xor    rax,rdx
   0x000000000000120f <+45>:    mov    QWORD PTR [rbp-0x8],rax
```

So basically it will move the value of `printf@libc` to the `rax` register then mov `rax` to `rdx` i.e the value to `rdx`, then it moves `0x1337133713371337` to the `rax` and xors `rax` and `rdx` the value is then move to the `rax` register and is used as the canary value 

```
   0x00000000000012a0 <+190>:   mov    rax,QWORD PTR [rip+0x2d39]        # 0x3fe0
   0x00000000000012a7 <+197>:   mov    rdx,rax
   0x00000000000012aa <+200>:   movabs rax,0x1337133713371337
   0x00000000000012b4 <+210>:   xor    rax,rdx
   0x00000000000012b7 <+213>:   cmp    QWORD PTR [rbp-0x8],rax
   0x00000000000012bb <+217>:   je     0x12c7 <main+229>
   0x00000000000012bd <+219>:   mov    eax,0x0
   0x00000000000012c2 <+224>:   call   0x10a0 <__stack_chk_fail@plt>
   0x00000000000012c7 <+229>:   mov    eax,0x0
   0x00000000000012cc <+234>:   leave
   0x00000000000012cd <+235>:   ret
```

But if you use IDA for decompilation it actually does a pretty good job decompiling it xD
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c479c6e7-23b9-44da-a298-02c03ddf1954)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char buf[56]; // [rsp+0h] [rbp-40h] BYREF
  unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  setup(argc, argv, envp);
  v5 = (unsigned __int64)&printf ^ 0x1337133713371337LL;
  write(
    1,
    "Tell me something thrilling and i'll share my dirty little secrets, nothing porn related though xD: ",
    0x64uLL);
  read(0, buf, 64uLL);
  printf("You: %s", buf);
  write(1, "Please, do tell me more, i'm dying to find out: ", 0x30uLL);
  read(0, buf, 100uLL);
  return 0;
}
```

So.... at this point we know that it's solvable because we can leak the canary therefore getting the `printf@libc` value because the value was xored with `0x1337133713371337` and from the property of xor we can retrieve the other value by just xoring `canary` with the hardcoded value `0x1337133713371337`

What next?

Well the point we have a libc leak means we can just calculate the libc base address and therefore using the second buffer overflow we can just rop or jump to a one_gadget

I tried ropping but I had stack allignment issue and there wasn't a `ret; ` instruction in the libc file so I decided to use a `one_gadget`

Let's get the one_gadget addresses
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4900c13e-648a-4ef1-abee-ebb62b2d54a9)

```

➜  revealZ one_gadget libc.so.6 
0x50a47 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL
  rbp == NULL || (u16)[rbp] == NULL

0xebc81 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

0xebc85 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL

0xebc88 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
➜  revealZ
```

When using one gadget we need to make sure the constraint are ok before using it else it won't work

I used the first address and I need to make sure `rbp == 0` 

The other register seems to work without setting it `0` for some reason (I did take a look at the register when the program was returning and it wasn't entirely null)

To get a gadget to use preferably a `pop rbp` gadget I used `ropper`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1312b0b5-0a9a-4ba1-b5ba-fd9b073ecf52)

```
ropper --file libc.so.6 --search "pop rbp; ret;"
```

With that it's all set 🙂

So our goal is to first leak canary, calculate libc base then jump to one_gadget

For the second stage of our exploit we need to first overwrite the canary value to its original value then overwrite saved rbp with some junk value of 8 bytes then finally our rop gadget with one_gadget

Here's my exploit: [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/abcctf23/reveal/solve.py)

Running it works locally
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b9c4a096-c1ab-4505-9c0f-13e9071d6576)

Doing the same remtotely works then we can grab our flag 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4fd41ce2-8699-439f-9f6a-c52ac1a45211)

```
Flag: abcctf{see_the_unseen_and_bring_the_flag_to_life}
```

#### Simple Calculator (Web Exploitation)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4ebe735-a838-4194-93c2-c7ed876c72cd)

Going over the web page shows this calculator sort of interface
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90ce0315-dec9-4d9d-8fde-1288044967a7)

Looking at the page source just shows a client side javascript being used by the calculator that helps evalutes the user input
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/85cdf9de-23e7-4a5b-8dc1-a924817fd4a1)

Since it's client side I didn't really bother checking it even though it uses `eval` but this javascript not nodejs also client side not serverside besides i don't think it's possible to execute system command with javascript

With that said I decided to look at the report a bug function this webapp provides
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/16a6a810-a75f-4ec4-a3d1-caf3af11aea6)

I tried using a random value but I noticed it doesn't seem to do anything
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/710d9ce6-79cd-441a-b1c7-3cbf897491b2)

At this point it became hard not because the challenge is hard itself but the text there was really misleading 😂

After spamming like various xss payload or anything that can make it do a callback to the webhook site, it didn't work

I fuzzed with any extension I could think of and various wordlist but still nothing!

So I left this challenge to work on other things

But eventually after some hours the creator @Muzec gave a hint saying "BLIND" 

Hmmmmmmm blind what exactly?

I decided to try command injection to invoke a sleep call

Doing that worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6100f600-cf0d-4c9b-adfe-b1dbb1f5937a)

So let's get a reverse shell shall we?

I hosted a http server which had a file `rev.sh` containing a reverse shell then did this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96fe03f7-ced9-4d80-bf3a-25cae2df2b9b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ab72c1f5-a596-4367-817b-a6495c06b119)

The flag was in the environment variable

```
Flag: abcctf{51MP13_r3P0r7_607_Y0U_7H3_F146}
```

This is all I believe I don't need to make a writeup on the remaining ones I solvef cause it's pretty much solvable by anyone just `strings & grep`

Welp that's all I did 😛

After the end of the ctf I came out first 🙏
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/675ceaee-1a38-4998-bbd2-f14667f9562a)


