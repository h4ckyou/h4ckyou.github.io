<h1> Ecowas CTF Final 2023 </h1>

Hi, I participated in this ctf final as `@Urahara` playing with team `error` from `Nigeria`

I'll give the solution to some of the challenges that I solved and maybe the ones that doesn't require an instance to connect to since most of them are currently down :(

### Binary Exploitation
- Offset
- Aslr 
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

Here's my solve script: [link]()



This CTF was an interesting one and I meet tons of cool people there 
