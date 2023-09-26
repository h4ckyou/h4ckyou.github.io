<h3> Cyberlympics CTF </h3>

![img](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7191729-17fe-43bc-a337-c2bae7e1d203)

Hi! In this writeup I'll give the solution to all the binary exploitation challenges. Maybe if I have time and I'm online I'll try put the other challenge I solved

Have fun reading!

#### Flag Bank [1st Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0ddec6ed-e66a-4b66-b174-fdda9f272906)

I first connected to the remote instance but at the moment it is down 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f472d72-1882-4c6e-8e9e-f46e0809e158)

So let's work with the binary
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4adbfa4d-6719-48b5-82d4-00144e161e70)

Seems we can purchase the flag is our amount is `$20000` but currently our amount is `$10000`

We can also purchase a test flag which worth `$3000` 

Let us do that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3bca721-73cf-43c0-8136-54bf1df88d57)

Ok it works but now what's our current account balance
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/197a5e77-0aac-4fb6-86cf-8152666211f9)

Nice it deducted `$3000` from our balance which is expected

At this point we can try purchase a negative value of flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92122ba9-02e6-4d8c-bc73-33e60a4791f9)

Ok that seems to work now we can try to buy the real flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/70594095-dabd-4319-b0c2-9b400106b298)

We get content of flag not found why?

If you run ltrace you will see it trys to open up the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e8179d4-568e-4025-b585-f01d665a240e)

So we can create a fake flag file and run the program again
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/573e14d9-1030-45f0-befb-5d42cba1af18)

That works!

If you want to know why that works you can decompile the binary in ghidra and view the functions used by the program

I won't go through the whole source but I'll show you where the vuln lies
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c1d330bd-91c8-40fd-969d-c453de867d37)

We can see that it will subtract the multiplication of the `number of flag to be bought` and `the fake flag price` with `our current balance`

Since it doesn't check if the number of flag to be bought is negative therefore the whole arithmetic will be changed to:

```python
currentBalance = currentBalance + nFlag * fakeFlagPrice
```

With that our balance would be increased therefore bypassing this check making us get the real flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c4bb65d2-9fa0-4d3c-8968-523d2b0dbab0)


#### Simple
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b78c54bf-21aa-431a-a65b-5cfcd7e25e91)

During the ctf I didn't manage to solve this for some silly reason anyways this is an upsolve.

After downloading the binary I checked the file type and protections enabled on the binary
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3b5df128-f533-4ddb-8167-987a556e2f2a)

We are working with a x64 binary which is dynamically linked and not stripped.

The only protection not enabled is Stack Canary.

Opening the binary in ghidra for decompilation shows this available functions

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd43f249-f5e0-4fd0-b0cf-2be44e0165ef)

Let us view the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6d421ddc-91d1-4bf9-8faf-31cc6cbec838)

```c
undefined8 main(void)

{
  code *shellcode;
  
  setup();
  shellcode = (code *)mmap((void *)0x0,0x1000,7,0x22,-1,0);
  printf("%s","Easy! Fire it up: ");
  fgets((char *)shellcode,23,stdin);
  (*shellcode)();
  return 0;
}
```

It first calls the `setup` function which does some buffering and nothing much
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/baf40646-aa2c-4547-907f-9091115369fc)

But the main function is pretty small and nothing much going on

Here's what it does:
- It creates a new mapping in the virtual address space of the calling process using `mmap`
- Then it receives 23 bytes of input and cast it as shellcode

Basically all this binary does is to receive our input then run it as shellcode

But the catch here is that it has to be a 23 bytes shellcode

Well we could just google `x64 23 bytes shellcode` doing that would lead [here](https://www.exploit-db.com/exploits/46907)

If we try that it won't work
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/807f429e-dc49-43f7-b060-df8c59e95dd4)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/80e19f97-a355-48b0-a3e4-f307ce11c9fd)

The shellcode looks good but the thing is here:

```
push 59
pop rax
```

That part can be optimized using this assembly instruction

```
mov al, 59
```

Basically instead of push `59` to the stack and putting it in the rax register we can just directly put it in the lower byte register of the rax register

Also this shellcode is basically called `execve` which requires three arguments `/bin/bash, 0, 0`

Modifying the shellcode to that worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/229acedd-72c9-4bc7-9dd6-285ad20727b6)

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/cyberlympics22/prequal/simple/solve.py)


#### O Wise Traveler [1st Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6848ea7-1862-4fdd-a517-de1267ead6f6)

After downloading the binary I checked the file type and the protection enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dad54b98-fde1-47b2-a6dc-eb4c7883e043)

We can see that this is a x64 binary which is dynamically linked and not stripepd

The only protection enabled on the binary is NX (No-Execute) and PIE (Position Independent Executable)

So basically when NX is enabled this means that the stack is not executeable meaning we won't be able to execute shellcode that's placed on the stack

While when PIE is enabled that means when ever we run the binary it will get loaded into random addresses

So on each execution the binary memory address would change

To understand what the binary does I loaded and decompiled it in ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c8b0476-9bdb-438d-af68-a3b123034ade)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81be9daa-82db-4696-9672-7b566cfc60b5)

```c
undefined8 main(void)

{
  char local_98 [143];
  char option;
  
  setup();
  memset(local_98,0,0x82);
  fwrite(&banner,1,0xbb,stdout);
  __isoc99_scanf("%c",&option);
  if (option == '1') {
    puts("Go back to where you came!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  if (option == '2') {
    question();
    fwrite("Would you like to tell me more about pointers? (y/n): ",1,0x36,stdout);
    __isoc99_scanf("%c",&option);
    if (option == 'y') {
      question();
      fwrite("Anything else? (y/n): ",1,0x16,stdout);
      __isoc99_scanf("%c",&option);
      if (option != 'y') {
        if (option == 'n') {
          puts("Cheers mate!");
                    /* WARNING: Subroutine does not return */
          exit(0);
        }
        puts("It\'s a y/n question :)");
                    /* WARNING: Subroutine does not return */
        exit(0);
      }
      fwrite("Shoot: ",1,7,stdout);
      getchar();
      fgets(local_98,0x82,stdin);
      printf(local_98);
    }
    else {
      if (option != 'n') {
        puts("It\'s a y/n question :)");
                    /* WARNING: Subroutine does not return */
        exit(0);
      }
      getchar();
      fwrite("Hate to see you leave. Were the challenges fun? (y/n): ",1,0x37,stdout);
      __isoc99_scanf("%c",&option);
      if (option == 'y') {
        puts("Splendid!");
      }
      else if (option == 'n') {
        puts("There\'s nooo waaay!");
      }
      else {
        puts("It\'s a y/n question :)");
      }
    }
    return 0;
  }
  puts("It\'s either 1 or 2 :)");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

I'll work through each of what this binary does:

First it prints out some banner which is more of the option and receives our input option and if our option chosen is `1` it will exit 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df22daa9-6bed-4753-a713-27800036e6ad)

Option 2 tends to perform more things
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0e50e0f-a861-4b00-8521-4a54ad2aec8f)

So it will ask a question and if our answer is `y` it will call the `question` function

Here's the decompiled function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9baea990-c03d-4a03-add3-ae70d551d508)

```c
void question(void)

{
  char buffer [144];
  
  memset(buffer,0,0x82);
  fwrite("Educate me, what\'s so interesting about pointers: ",1,0x32,stdout);
  getchar();
  fgets(buffer,0x82,stdin);
  printf(buffer);
  return;
}
```

So basically what all this does is to receive our input and print it our back using `printf`

Back to the main function, we are asked the same question again if our answer is `y` it will call the `question` function again 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8c805f3e-5375-4c22-886b-68669f1fce98)

And after that it would ask `Anything else` if our answer if `n` it will exit the program

Else it receives our input and prints it out using `printf`

But if the initial question is `n` it would do this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b8689fb-d39a-456e-8d69-bf0620e89a1f)

Nothing much going on there so I won't look explain that

At this point the vulnerability is quite obvious and it's occurs here:

```c
void question(void)

{
  char buffer [144];
  
  memset(buffer,0,0x82);
  fwrite("Educate me, what\'s so interesting about pointers: ",1,0x32,stdout);
  getchar();
  fgets(buffer,0x82,stdin);
  printf(buffer);
  return;
}
```

And here:

```c
fwrite("Shoot: ",1,7,stdout);
getchar();
fgets(local_98,0x82,stdin);
printf(local_98);
```

So the vulnerability here is Format String Vuln

And that happens because the binary uses `printf` to print out our input without specifying a format specifier

With that we can leak address off the stack and also exploit the binary

Here's how my exploitation would go:
- First I need to calculate the elf base address with the libc base address and that's neccessary because PIE is enabled and we need the libc base address
- The second chain I'll overwrite the value of `printf@got` to `system` in libc so that on the third part where `printf` is called on our input it would be evaluated as `system` therefore giving us command execution

Another thing to know if where the offset of our input is on the stack

And we can easily calculate it using this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/07bf88e6-50fb-42ed-bc73-022ef1e29549)

At offset `6` is where our input is on the stack

We also need an offset where a binary address and libc address is on the stack so I made a simple fuzz script to get me that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5045a7fe-db76-42c2-9263-e248470cce83)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23edff39-c146-4a32-bb76-9db4c57682ee)

Ok but before we move forward one thing to note is that we would need the libc for solving this but since it wasn't provided I asked one of the mod if the docker instance is the same for all challenges and he said yes

So I got rce on one of the web box (Demon Slayer) then transferred the libc for it to my device and patched the binary using [pwninit](https://github.com/io12/pwninit)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1b04e3cb-aeb9-4044-bfcd-f4be80d9c3d4)

With that said the binary would be the same as the one in the remote instance

For the second chain I'll perform a Global Offset Table (GOT) overwrite of `printf@got` to `system@libc`

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/cyberlympics22/prequal/O%20Wise%20Traveler/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5652e76f-df14-4f53-9738-5014424094fd)
