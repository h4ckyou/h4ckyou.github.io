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
