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











This CTF was an interesting one and I meet tons of cool people there 
