<h2> Binary Exploitation </h2>

    - Chall Name: Ecostorage
     - CTF: THCON22

This was a very cool challenge that took me some amount of hours to solve and I learnt something new while solving it

It shows that not all pwn related challenge involves popping of shells 🐚 as there are other various things one can do while exploiting a vulnerability in a program

Let's start shell we?

First thing I do always is to know what type of file I'm working with and the protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/481ca51d-f842-4047-9446-7e1ae444c5f1)

Cool we are working with a 64bits binary which is dynamically linked and not stripped

The following protections are enabled:
- Full Relro
- Stack Canary
- No-Execute
- PIE

What a hassle all protections are enabled!!

To get an overview of what the binary does I ran it and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/519ef7e1-a6b7-4b50-a323-23e98dcc241e)

So it seems we can:
- Read File
- Go Premium
- Exit

  
