<h2> Binary Exploitation </h2>

    - Chall Name: WhereAmI
     - CTF: Angstrom22

This challenge is basically just ret2libc but with a twist.

The catch is that there's a global variable counter that makes sure we don't get to call `main()` again but i bypassed that by decrementing the value stored in the global variable

Let's start shall we?

As usual we get the file type and protections enabled. The libc was also attached so i already patched it with `pwninit`.
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4b72c7e4-0051-4077-9f93-80380ab5eb4f)

So we're working with a x64 binary which is dynamically linked and not stripped

The only protection enabled is NX

I ran the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d19c5419-a02f-442c-a9e8-b936844ea098)

It receives our input then the program exists

Loading the binary up in Ghidra and looking at the main function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3cc64162-dd05-41c9-83f6-874033724791)

```c

undefined8 main(void)

{
  char buffer [60];
  __gid_t egid;
  
  setbuf(stdout,(char *)0x0);
  egid = getegid();
  setresgid(egid,egid,egid);
  puts("I\'m so lost.");
  printf("Who are you? ");
  if (0 < counter) {
    exit(1);
  }
  counter = counter + 1;
  gets(buffer);
  puts("I hope you find yourself too.");
  return 0;
}
```

There's no other function aside that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90baa1c7-f43c-441b-981a-6d346fa634a1)

So concerning the main function here's what it does:
- Gets the current effective group id and sets the real user id to the value returned
- It checks if the `counter` which is a global variable is greater than `0` and if it is the program exits with return code of `1`
- If the program doesn't exit it will increment the counter by `1` and receive our input using `gets()` then finally return

The vulnerability is pretty obvious to spot since the usage of `gets()` leads to buffer overflow

At first I tried to leak libc using `puts()` and jump to the next instruction which tends to increment the counter 

It worked but after I provide input the program crashes?
