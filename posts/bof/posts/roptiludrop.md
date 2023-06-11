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

