<h3> GreyHat 2023 CTF </h3>

Here are the writeups to the pwn challenges I solved:
- Babypwn


#### Babypwn

After downloading the attached file checking the file type shows this

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a38b5ee8-e0e5-4f05-8715-500ea7b58bb5)

So we're working with a x64 binary which is dynamically linked, not stripped and has all protections enabled

I'll run the binary to know what it does:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3b54bef9-ace8-4052-b279-07e02d56b5da)

Seems to be some banking system that allows us withdraw & deposit money 

We can't find the vuln yet so let us look at the decompiled code

I'll be using ghidra
