<h3> PicoCTF 2025 </h3>

Hi `0x1337` here, I participated with team `M3V7R` and we placed first on the Africa scoreboard
![image](https://github.com/user-attachments/assets/365896bd-7924-42c1-950b-bd22d3e8845b)
![image](https://github.com/user-attachments/assets/a5701d5b-a8de-42c8-97f6-67249b04812a)

I tackled mostly the pwn and rev challenges and this writeup contains the solution to them all

<h3> Challenge Solved </h3>

## Binary Exploitation
- PIE Time 1
- PIE Time 2
- Hash Only 1
- Hash Only 2
- Echo Valley
- Handoff

## Reverse Engineering
- Flag Hunters
- Quantum Scrambler
- Chronohack
- Tap into Hash
- Binary Instrumentation 1
- Binary Instrumentation 2
- Perplexed

### Binary Exploitation

#### PIE Time 1

![image](https://github.com/user-attachments/assets/4e895ce7-3bc4-405a-98d9-043d809ec49e)

We are given the source code and binary

Reading the source code, in the main function 
![image](https://github.com/user-attachments/assets/d9a9ccfc-84f4-4ff8-b85a-67d661f003a9)

This would:
- Give us an elf section leak specically the `main` function address
- Receives a hex value and casts it as a function pointer which is later called

The program has a win function which would print the flag
![image](https://github.com/user-attachments/assets/e2aec084-042b-41d8-9637-5a5f67ad0e9c)

We simply just need to jump to function

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2025/Binary%20Exploitation/PIE%20Time%201/solve.py)

![image](https://github.com/user-attachments/assets/81993aca-c2f7-4913-b926-1959816c3382)

Running it, we get the flag
![image](https://github.com/user-attachments/assets/eedb3f6f-264e-4f2d-8505-cf1669799c30)


#### PIE Time 2

![image](https://github.com/user-attachments/assets/6c95b2e2-8a39-4762-b48e-19c7eb9d49b7)

Same as the previous challenge we are also provided with the source code and binary

Starting from the main function we see it calls the `call_functions` function
![image](https://github.com/user-attachments/assets/bb48a252-a8da-4c02-ae39-3e63ee12946f)

Here's what the function does
![image](https://github.com/user-attachments/assets/71c22757-a1dc-41ff-98a4-85d2cce00e32)

So first it:
- Receives our input and then prints it out
- Receives a hex value which is casted as a function pointer and later called

This also has a win function
![image](https://github.com/user-attachments/assets/236746ed-f131-425a-ade3-5ed0ad774aa6)

Our goal is to jump there yet again

But this time we are not given any memory leaks, and checking the protection enabled on the binary we get this
![image](https://github.com/user-attachments/assets/2adfd7cd-1fae-4b3f-9cd7-15075796b67e)

This means we need to leak some memory address

There's an obvious format string bug since it uses `printf` on our controlled buffer without using a format specifier

We will leverage that to get memory leaks

To calculate the offset where a pointer to the elf section is on the stack i'll use gdb 

Using `gdb-pwndbg` and setting a breakpoint at `b *call_functions+80`
![image](https://github.com/user-attachments/assets/dd29fe46-ef95-415f-9c94-702a1338c65f)

Here's how the stack looks like
![image](https://github.com/user-attachments/assets/5122f6e2-70ac-45fb-a6eb-b10c493db89d)

We can see at offset 19 holds a pointer to the `elf` section
![image](https://github.com/user-attachments/assets/82741b9d-6c01-4f53-9d7a-bfdbc276d134)

Now we calculate the offset of that address to the pie base
![image](https://github.com/user-attachments/assets/2fc7f85e-81ae-47eb-8434-a4a3a26dde5b)

This means if we the address at offset 19 and subtract it with `0x1441` that would be the pie base

And with that we can easily just jump to the win function address

Here's my [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2025/Binary%20Exploitation/PIE%20Time%202/solve.py)
![image](https://github.com/user-attachments/assets/91df4ae7-983a-46bf-8728-f9663223940b)

Running it works
![image](https://github.com/user-attachments/assets/1328eefd-cbdb-40d5-aaa0-a6b7e975147c)


#### Hash Only 1

![image](https://github.com/user-attachments/assets/5b71a020-aec2-4d03-a17d-ca1b5cdf5f89)

We are given an ssh instance to connect to and also an alternative command to copy the `flaghasher` binary from the remote host to our local host

Let us first take a look at what the binary does on the remote instance
![image](https://github.com/user-attachments/assets/961bc6d3-9436-4e74-b693-d52f802229a8)

Running it we see it computes the md5 hash of the `/root/flag.txt` file

We obviously can't derive the content of the flag from just the hash so we need to some how figure a way around this

To copy the binary to our host we use this command

```
scp -P 53610 ctf-player@shape-facility.picoctf.net:~/flaghasher .
```

After the transfer, checking the file type shows it's a 64 bits binary
![image](https://github.com/user-attachments/assets/645bec08-f6ba-45b8-ab4b-d5c226161391)

Running strings on it we can infer it's a c++ compiled binary
![image](https://github.com/user-attachments/assets/a9be228e-31c9-4841-8645-97e0cde481c0)

Using IDA to decompile here's the main function

















