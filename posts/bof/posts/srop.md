<h2> Binary Exploitation </h2>

    - Chall Name: SROP
     - CTF: NoobzCTF

Hi everyone I'll be showing the solution to the SROP challenge from NoobzCTF 2023

Orignally I didn't solve it due to my lack of knowledge of the exploitation technique but I decided to give it a go since I learnt it recently.

Ok first thing is always to check the type of file we're dealing with and the protections enabled on it

In this case we're dealing with a 64bits linux executable which is statically linked and not stripped
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/272f7635-60a3-4238-8ed9-69dc3b386377)

And no protections are enabled on this binary :)

I ran the binary to get an overview of what it does and it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8acf51c0-01b6-4c37-80dd-b68befce9806)

So it seems to print out some text, receive our input then exit

Before I move on forward we should note that when a binary is statically linked, functions that are going to be called by the program would be in the binary usually making the file size much

That case doesn't apply here since the file size is too small (8992 bytes)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00c15b7d-45b7-41ea-84ce-f9e63b9963b2)

So that means it's likely written in assembly language and compiled rather than it being compiled in C language
