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

