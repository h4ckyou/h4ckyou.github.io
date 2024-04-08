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



























