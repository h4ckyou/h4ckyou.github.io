<h3> PicoCTF 2025 </h3>

Hi `h4cky0u` here, I participated with team `M3V7R` and we placed first on the Africa scoreboard
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

This means if we get the address at offset 19 and subtract it with `0x1441` that would give the pie base

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
![image](https://github.com/user-attachments/assets/438d4c3e-e6dd-4f9a-9c9b-6918e4ca3811)
![image](https://github.com/user-attachments/assets/35b48d7f-349b-42f4-84b5-6310cb8416ba)

The program first prints a message to the terminal and pauses for two seconds. It then defines a command string containing `/bin/bash -c 'md5sum /root/flag.txt'`. After that, it escalates privileges by setting both the group ID (gid) and user ID (uid) to 0. Finally, it executes the command using the system function.

This basically just calculates the `md5sum` value of the file `/root/flag.txt`

The issue here is the way the `md5sum` binary is being used, it doesn't specify the full path thus we can hijack the binary so that it executes something else

The first step is to create a malicious `md5sum` binary, i just did something really easy
![image](https://github.com/user-attachments/assets/7b38f6b1-a4bc-440c-b388-1cc29cf4e887)

Next we add our current directory to the environment `PATH` variable
![image](https://github.com/user-attachments/assets/304f90a4-4378-445d-8088-e9e3924ea0af)

```
echo "cat /root/flag.txt > a.txt"  > md5sum
chmod +x md5sum
export PATH=/home/ctf-player:$PATH
```

We can see that on executing the `flaghasher` binary we get the flag!

#### Hash Only 2

![image](https://github.com/user-attachments/assets/6f67310d-7107-4d51-8175-fc21083c0c51)

Connecting to the ssh remote instance we get this
![image](https://github.com/user-attachments/assets/d3675b0e-faa3-4e32-a441-5c3223edcec7)

Every thing looks all good until i tried finding the suid binary `flaghasher` and it shows this error:

```
-rbash: /dev/null: restricted: cannot redirect output
```

So it seems we are in a restricted shell called `rbash`

Looking it up for bypass we find that it can be easily bypassed using the `-t "bash --noprofile"` argument

Doing that works
![image](https://github.com/user-attachments/assets/113b137c-d81a-40e3-b019-fefd47ca502a)

The `flaghasher` binary is still present but just in a different directory

Executing it shows the same thing as the previous one
![image](https://github.com/user-attachments/assets/54149357-7737-4e0a-8579-778e3b861b45)

I just reused my previous solve for the path hijack and that worked
![image](https://github.com/user-attachments/assets/f44c3188-d666-4944-b780-55189521c32a)


#### Echo Valley

![image](https://github.com/user-attachments/assets/a057fab9-577b-44c9-b12d-c1301b1e98c5)

We're given the source code and binary
![image](https://github.com/user-attachments/assets/a6abba6b-e630-460d-ae09-131d7e6ca7bc)

Here's the main function

![image](https://github.com/user-attachments/assets/2773847f-40d2-4cc1-9283-97a6970b52f8)

It just calls the `echo_valley` function which does this
![image](https://github.com/user-attachments/assets/fc5ddfde-c2fd-45d0-8464-1e39dc3dc152)

This simply just keeps receiving our input and printing it out back until we give it `exit` before it returns back to `main`

There's also a win function
![image](https://github.com/user-attachments/assets/eebf1af5-11d1-47fd-9beb-5a931409db54)

So our goal is simply to somehow call that function

The bug is an obvious format string bug

Looking at the protection on the binary we get this
![image](https://github.com/user-attachments/assets/d017f981-a632-418c-97d8-44298df577ea)

We see that all protections are enabled

The first thing we would need are memory leaks

I leaked `pie` and `stack`

The reason i leaked a stack address is because i'll be overwriting the saved rip of the `echo_valley` function to the `print_flag` function

Setting a breakpoint at `echo_valley+218` here's what is on the stack
![image](https://github.com/user-attachments/assets/d4c9689d-d612-4ceb-a155-bd2e4b22d314)

At offset `20 & 21` holds some stack and pie address
![image](https://github.com/user-attachments/assets/c70ddec1-820d-49f0-8616-05d3a4e4d9d7)

And that's what i leaked
![image](https://github.com/user-attachments/assets/08df8a37-9647-469f-b23c-ee009fcd025f)

To calculate the saved rip address i set a breakpoint at `echo_valley+249` then inputted `exit`
![image](https://github.com/user-attachments/assets/6ae5f81c-ad30-4fea-b6d8-5c7a5786466a)

Now we look at the stack frame
![image](https://github.com/user-attachments/assets/fa6bbcbd-625f-4f59-9dd0-1d06db6b7b3d)

Now we just subtract our leaked stack address with that of the saved rip
![image](https://github.com/user-attachments/assets/7e9b2ccd-e878-4de6-9ed9-352c301cb220)

It's just `8` 

With this we will leverage the format string bug by gaining arb write and our goal is to overwrite the saved rip to the win function

Here's my [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2025/Binary%20Exploitation/Echo%20Valley/solve.py)
![image](https://github.com/user-attachments/assets/27ad8f4c-04e1-4255-8192-cc852510fd2d)

Running it works
![image](https://github.com/user-attachments/assets/4f1a75a1-f2f4-44d2-9e1c-6feffd75b1a5)

#### Handoff

![image](https://github.com/user-attachments/assets/7796db3b-e89d-476e-aced-0845e4a3cdba)

We are given the source code and binary

First we'll take a look at the protections on the binary
![image](https://github.com/user-attachments/assets/8026ae9f-3e4e-41a5-be8b-1133bb9cc907)

The binary literally has no protection enabled, okay looks good!

Running it shows this
![image](https://github.com/user-attachments/assets/5356c86f-dcaa-46f9-a95a-bfabd56a26d9)

It has just two main options we can choose from

Since we have the source code let's take a look at it
![image](https://github.com/user-attachments/assets/61c1c648-145a-4914-81ea-c07e6cd16364)

First we have a struct called `entry_t` that manages the `name` and `message` of the recipient

```c
typedef struct entry {
	char name[8];
	char msg[64];
} entry_t;
```

I'll look through just the important details

If we decide to add a new recipient it will read into `entries[total_entries].name` 32 bytes of data 

If we decide to send a message it will receive the index of the the entries we want to store the message and read 64 bytes of data into the `msg` field of the `entry_t` struct

And finally when we choose exit it will ask for our feedback where it reads in up to 32 bytes of data to the feedback array, null terminates at index 7 and returns

Okay cool so now what's the vulnerability?

Well there are some bugs here such as:
- Buffer overflow in feedback
- Out of bound write in add message

There's also an overflow in add recipient but i wouldn't consider it that much of a risk because even though it overwrites the `msg` field when we attempt to add a message it will replace what we overwrote with our new message

The out of bound read occurs in the add message function since it doesn't check if `index` is less than `0`
![image](https://github.com/user-attachments/assets/a17552ea-8b27-4432-a6ec-3130d146bce0)

But this isn't so much useful because there's nothing really important before the entries as you can see from the stack view 
![image](https://github.com/user-attachments/assets/28dbab7c-0c43-41be-bc58-1d46fc45a07a)

Now the main bug which we'll exploiting is the overflow in feedback

We see it's defined as a char array of 8 bytes but we're reading in 32 bytes of data to the array

At first it might look like an easy win here? but if you take a look at the stack view you'll see this
![image](https://github.com/user-attachments/assets/80634c26-14bd-4176-9ef9-a5014ece7338)

```
-000000000000000C     char feedback[8];
-0000000000000004     _DWORD total_entries;
+0000000000000000     _QWORD __saved_registers;
+0000000000000008     _UNKNOWN *__return_address;
```

The offset from the feedback array to the return address is:
- 8 + 4 + 8 = 20

This means the first 20 bytes will first fill up the `feedback` array, the `total_entries` and then the `saved rbp` 

That effectively leaves us with roughly 8 bytes for rip control

What???

How do we pwn this with just 8 bytes of rip control

Things began getting tough at this point

I neglected the fact that `NX` was disabled at first and that means the stack is `rwx` 

During the time spent on trying to solve this challenge (about 5 hours or so) i attempted:
- stack pivot to the global offset table which got me a libc leak but i couldn't pop shell because i had just 8 bytes rip control and one gadget didn't work :(

Then i decided to take a look at the rop gadgets again and got this
![image](https://github.com/user-attachments/assets/a180524f-ced5-41ed-8a7b-dc25cfd3543b)
![image](https://github.com/user-attachments/assets/944bc477-e529-4a03-a35f-6be47735060d)

The one of interest is the `jmp rax`

Taking a look at the registers when it's about to return shows this (set bp at vuln+485)
![image](https://github.com/user-attachments/assets/11885c5e-88e0-4fd5-a4cb-daf6455aa1ac)

We see that `rax` is a controllable buffer and that represents our `feedback` array!

This means we can place shellcode as the feedback then set rip to the `jmp rax` gadget effectively giving us shellcode execution

Phew! But now we know that, how can we spawn a shell?

Remember that the entries are actually stored on the stack! This means we can make `rsp` point to `entries[0]` which would hold our shellcode!

I calculated the offset between the current stack with where `entries[0]` is stored to be `0x2e4`

So with a `sub rsp` instruction + a `jmp rsp` instruction i pivoted the stack to our execve shellcode and got code execution!

Here's my [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2025/Binary%20Exploitation/Handoff/solve.py)
![image](https://github.com/user-attachments/assets/0e89c56c-63d7-484b-bf3d-6a871888a942)

Running it works
![image](https://github.com/user-attachments/assets/a3d1ad1b-ccac-44a9-b42e-dcba95c0862e)


### Reverse Engineering

I'm yet to write about this but i solved all challenges in this category, I'm a bit tired but all my solves are [here](https://github.com/h4ckyou/h4ckyou.github.io/tree/main/posts/ctf/picoctf/scripts/2025/Reverse%20Engineering)

The Binary Instrumentation 1 & 2 isn't there because it's windows rev which i solved by debugging on my windows host

- Binary Instrumentation 1:
  
But the idea behind the challenge 1 is that it will resolve some winapi functions and then executes a region of memory which holds some shellcode that later calls a function that is meant to print the flag

The issue is that it's going to take a lot of time since it uses a sleep variant to make the program pause execution

Rather than patching the function call i just scrolled down a bit and saw the base64 encoded flag which is supposed to be printed to stdout after the sleep is done so i just decoded and i got the flag

- Binary Instrumentation 2:
  
This one really took me quite a lot of time (3 hours) the reason is i'm not so much familiar with windows reversing 

So i really spent lot of time in the debugger

But the challenge itself basically also resolves some api and then executes some shellcode 

The issue with this one is when it tries to perform some winapi call it fails for some reason :( 

But before it exists i created a dump of the new memory region it creates 

And decompiling it i got the flag, but you can as well just scroll down in the memory dump and you'll see a suspicious base64 looking string

- Perplexed
  
The other challenge which gave me issue was perplexed though to reverse it wasn't so difficult but for some reason i wasn't getting the last bytes to be printable

It really frustrated me and i ended up brute forcing using gdb scripting

This is my rant here:
![image](https://github.com/user-attachments/assets/f127f782-73fd-4ce3-b797-3f79b72b6c9a)
![image](https://github.com/user-attachments/assets/01bb0a1f-1e32-4b3a-b6f4-0caebffbfd72)

And finally
![image](https://github.com/user-attachments/assets/585d4793-57b2-49c5-a01b-59e9a7cb6640)

GG to my teammates!





