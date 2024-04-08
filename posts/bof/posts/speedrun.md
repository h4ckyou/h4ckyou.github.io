<h2> Binary Exploitation </h2>

    - Chall Name: Speedrun 4
     - CTF: Defcon Quals 2019
     
I got this challenge binary from [here](https://github.com/guyinatuxedo/nightmare/blob/master/modules/17-stack_pivot/dcquals19_speedrun4/speedrun-004)

You can follow along if you wish to do so!

First we start with some basic file checks
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df91bc99-58c6-46ab-9f6a-35ac1c8f3b8a)

We are working with a 64bits binary which is statically linked and stripped (oof)

The only protection enabled is the No Execute bit (NX)

So let's run the binary to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d40ac660-60a4-41fe-b657-b7b6fc2ccd36)

It seems to receive our input then exit

I opened the binary up in Ghidra inorder to reverse it and find the vulnerability

It sure did take some minutes for Ghidra to do it's stuff!

After that I viewed the main function which can be gotten from `entry` but the decompiled code was stripped so we don't get to know what exact function is being called

I had to renamed it and most of it was based on the output gotten when i ran the program

With that said here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b0deb6e-e32c-4412-9f24-3b220524d61e)

```c
undefined8
main(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,undefined8 param_5,
    undefined8 param_6)

{
  long fp;
  
  FUN_00410e30(PTR_DAT_006b97a0,0,2,0,param_5,param_6,param_2);
  fp = FUN_0040e840("DEBUG");
  if (fp == 0) {
    alarm(5);
  }
  say();
  get_input();
  bye();
  return 0;
}
```

The main part is in function `get_input()` as both `say & bye` just prints out some text

Looking at that function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/061ff97e-6636-4de3-82aa-59de945296df)

```c
void get_input(void)

{
  undefined input [9];
  undefined i;
  int size;
  
  puts("how much do you have to say?");
  read(0,input,9);
  i = 0;
  size = atoi(input);
  if (size < 1) {
    puts("That\'s not much to say.");
  }
  else if (size < 258) {
    get_input(size);
  }
  else {
    puts("That\'s too much to say!.");
  }
  return;
}
```

Basically this will receive our integer string then convert it to an integer using `atoi` and it makes sure the size is less than `258`

Our input is passed as the parameter to function `get_input()`

It's pretty weird as to why it's calling itself but I guess it's just the decompiler issue :)

Looking at the function shows an entirely different code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b7548040-3629-423c-96fb-fba31ba4c9fd)

```c

void get_input(int fp)

{
  undefined input [256];
  
  input[0] = 0;
  puts("Ok, what do you have to say for yourself?");
  read(0,input,(long)fp);
  printf("Interesting thought \"%s\", I\'ll take it into consideration.\n",input);
  return;
}
```

Ok so it defines a buffer called `input` which can hold up at most 256 bytes of data then it receives our input which is stored in the buffer with the size of what we initially choose?

Then it prints out the input and returns

From this we know that we can control the size of what we read in and looking at the buffer size we see that it can only hold up 256 bytes but we are allowed to use at most 257 bytes

This therefore leads to a one byte overflow

But what the hell can we do with just a byte?

First thing we need to know is that the one byte overflow is going to just overwrite the least signifcant bit of the saved rbp 

So we can't even control the program flow or can we?

Inorder to solve this we need to stack pivot so that we can then rop and spawn a shell

Before we get to that, we should know that every function aside main does this instruction before it returns

```asm
leave
ret
```

And the `leave` instruction is equivalent to:

```asm
mov rsp, rbp
pop rbp
```

The whole `leave; ret` instruction is then this:

```asm
mov rsp, rbp
pop rbp
pop rip
```

So basically if we can control the `rbp` register and it does a `leave; ret` instruction twice we can therefore control the instruction register because it does this:

```asm
mov rsp, rbp
pop rbp
pop rip
mov rsp, rbp
pop rbp
pop rip
```

In the second `leave; ret` instruction the `rip` register would hold the value stored at the top of the stack but notice that before it does that it will `mov` the value stored in the `rbp` register to the `rsp` register and from the first `leave; ret` instruction if we control the `rbp` we can therefore control the program flow since the value of `rbp` would be stored in `rsp`

But in this our case we can't overwrite the saved rbp nor the return address so what do we do?

Well we can't fully overwrite the saved rbp but we do control the lsb of the address

And also the second case should be how do we trigger another `leave; ret` instruction?

Luckily this function was called from another function that isn't `main` meaning the function would have a `leave; ret` instruction too

We can check it out
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/89197169-3804-42ab-be2e-12870c08cf41)

Ok cool 

Here's how my exploit plan would go:
- Since the offset between the saved rbp in the `get_input` stack frame differs with the `input` buffer with just the lsb we can overwrite the saved rbp lsb with that of our input buffer on the stack
- Then eventually the rip would point to the value of our input
- My input would contain rop gadget which would stored `/bin/sh` in memory and spawns a shell via `execve`
- Profit!
















