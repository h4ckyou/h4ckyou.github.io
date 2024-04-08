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
