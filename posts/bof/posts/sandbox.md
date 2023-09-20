<h3> Sandbox </h3>

This was a binary I saw saved on my laptop I usually do that cause in CTFs I might not be able to solve lot of the pwn or other challenges so I usually save it randomly in my filesystem 

While I was less busy I saw it and said hmm let me give this a shot!

So here we are and I'll give you my solution used to solve it

First thing we'll check the file type and the protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7fddcda1-be63-4323-a703-3766620adc46)

Ok we're working with a x64 bit binary which is dynamically linked and not stripped 

From the result of checksec we can see that all protections are enabled 

I ran it to have an understanding of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/985dd096-c94f-4d85-b76b-7e4347408a03)

It just receives our input and prints it out back and that's done in a while loop

To get the vulnerability and understand exactly what's happening I took it over to Ghidra and decompiled it

Since the binary isn't stripped we will get debug symbols like the function names 

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4ec45a5-02eb-4e7c-b633-b30c5553727c)

```c
undefined8 main(EVP_PKEY_CTX *param_1)

{
  init(param_1);
  echo();
  return 0;
}
```

Ok nothing much it just calls `init` which does some buffering
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1fc3f08e-be89-450f-8d8e-4da6f91f05b1)

Then it calls the `echo` function (I already renamed the variable names to understand it well)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f390840d-8de8-4336-b66b-4e1d312af8c7)

```c
undefined8 echo(void)

{
  long in_FS_OFFSET;
  char buffer [40];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  buffer._0_8_ = 0;
  buffer._8_8_ = 0;
  buffer._16_8_ = 0;
  buffer._24_8_ = 0;
  buffer._32_8_ = 0;
  while( true ) {
    write(1,"message: ",9);
    gets(buffer);
    printf(buffer);
    if (buffer[0] == 'x') break;
    putchar(10);
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Ok the binary if fairly simple in execution:
- It `writes` out `message` to `stdout`
- Receives our input using `gets()`
- Print our input
- If the `0th` index of our input starts from `x` it will break out of the loop and return

Ok from this we can tell the vulnerabilities here are:
- Buffer overflow
- Format String Bug

Cool! Ok back to the `init` function did I say nothing much is going on there 👀

Well I nearly skipped that lol but here's it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7cd92df8-468b-49fe-8f58-54c1b9b204ba)

It actually calls another function called `sandbox`

Here's the decompiled code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd01d611-20b1-4901-ab33-043c6bc14290)

```c
void sandbox(void)

{
  undefined8 rule;
  long in_FS_OFFSET;
  uint i;
  undefined4 bad [2];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  rule = seccomp_init(0x7fff0000);
  bad[0] = 0x3b;
  bad[1] = 0x142;
  for (i = 0; i < 2; i = i + 1) {
    seccomp_rule_add(rule,0,bad[(int)i],0);
  }
  seccomp_load(rule);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

This is basically `seccomp` which is a sandbox sort of thing

And we can see that it doesn't allow any syscall number with `0x3b & 0x142`

We can use [this](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit) to identify what syscall is that or we can also just `seccomp-tools`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a111717d-2003-482e-bc94-954fba76b5e4)

The disallowed syscall is `execve and execveat` and that prevents us from popping a shell :(

So we're going to ROP with another syscall which in this case I used `Open, Read and Write`

This is how the exploit flow would go:
- I'll first need to leak PIE, Libc base address
- Leak Canary
- Then I ROP

To calculate the PIE base address I'll need to leak any Binary Secton Address using the format string vuln
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d734af16-3cbc-468f-a831-002aa6fb1c97)

The address leaked is the Canary and a binary section address

To confirm that we can use GDB 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b68bab1-d1d0-47f5-87f2-5d4f8e238fd1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d922e73-fc9d-4c66-8a5a-402f23b4e5b8)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d4f5479a-9fd6-4c2e-bea9-151ebf56459b)

So our canary is at offset `37` and we have a binary section leak at address 40 we know that it's a binary section because from the result of `vmmap` it is within the range `0x000055fa7b000000 0x000055fa7b001000`

Ok what about libc leak well it's at offset `3` we can get any via fuzzing but luckily this one wasn't too far in range
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/35614d42-1cfa-4399-94aa-81d4a9aa5e3d)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/030dde92-3ea6-449d-90b9-0b1b643ce60b)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd42d1c0-6dc6-4e44-9bdb-078755b48eb5)

With that set we can basically know the offset to the libc or elf base address 

For the next step since it's a buffer overflow we'll need to overwrite the RIP

But remember there's canary, since we have the canary leaked we can basically overwrite it with it's right value and pad the saved rbp with 8bytes (we can just fill in junks)

For the ROP part basically since we'll be doing Open, Read and Write we need to know the syscall and the expected parameters

That can be gotten from the chromium syscall link above
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b7281477-6aa7-4d25-bb43-52a339f7cf0c)

- For Open we need the `rax` register to be `0x02`, the `rdi` register to be the file name, the `rsi` to be the mode.
- For Read we need the `rax` register to be `0x00`, the `rdi` register to be the file descriptor returned by `Open` , `rsi` register to be the file buffer where to store the opened file, `rdx` to be the size of the file buffer
- For Write we need the `rax` register to be `0x01`, the `rdi` register to be the file descriptor, the `rsi` register to be the char buffer, `rdx` register to be the size to write out

At this point the idea is clear but we need just few more things

We can't pass `flag.txt` into `open('flag.txt', 0)` 

So we to some how need to put `flag.txt` into memory and then use `open({memory}, 0)`

To do that I called `gets()` to receive our input then placed it in the `.data` section of the binary

With that said the last stage is getting rop gadgets

To do that I used `ropper` but unfortunately there was no `pop rdx` gadget in the binary
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f296bc15-e44b-45f3-bea4-73c7c88c681b)

But since we already leaked the libc base address we can also use gadgets from the libc file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e9efeef-347a-4324-97dd-0f0684cf5730)

That's all we need :P

Here's my exploit [script]()
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e72d45e9-f518-427b-9eb6-0756e3a3a14f)

