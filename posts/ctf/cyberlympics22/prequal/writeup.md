<h3> Cyberlympics 2023 Prequalification </h3>

![img](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7191729-17fe-43bc-a337-c2bae7e1d203)

Hi! In this writeup I'll give the solution to all the binary exploitation challenges. Maybe if I have time and I'm online I'll try put the other challenge I solved

Have fun reading!

### Binary Exploitation

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

And that happens because the binary uses `printf` to print out our input without using a format specifier

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


#### Robin [1st Blood 🩸]
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/74a8f810-b90c-4016-9e50-09d9bff3e746)

Doing the usual gives this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6076c36a-6fdb-42e9-b611-7b01551577ee)

Note that I already patched the binary with the remote libc file

So we're working with a x64 binary which is dynamically linked and not stripped

The protection not enabled is PIE

Using ghidra I decompiled the binary here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1ed944ba-4252-454e-9f27-f2aa2af25444)

```c
undefined8 main(void)

{
  undefined8 buffer;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  code *idk;
  undefined8 *mmap_;
  
  setup();
  mmap_ = (undefined8 *)mmap((void *)0x999999000,0x20,3,0x21,-1,0);
  idk = notcalled;
  fwrite("Tell me, what\'s your strategy here: ",1,0x24,stdout);
  read(0,&buffer,0x20);
  printf("Riiiiight, %s",&buffer);
  *mmap_ = buffer;
  mmap_[1] = local_30;
  mmap_[2] = local_28;
  mmap_[3] = local_20;
  fwrite("This might actually come to fruition. Try fire it up: ",1,0x36,stdout);
  fgets((char *)&buffer,0x100,stdin);
  return 0;
}
```

The binary is fairly simple and here's what it does:
-  It creates a new mapping in the virtual address space of the calling process using `mmap`
-  Sets a global variable called `notcalled` and what it does is just a `ret` call
-  Receives `0x20` bytes of our input and stores in the `buffer` variable
-  Prints out our buffer
-  Receives `0x100` bytes of our input and stores in the `buffer` variable
-  Then returns

So the buffer overflow is pretty obvious right? but the issue is because PIE is enabled this is going to look kinda hard

But there's another issue with this binary

And it's here:

```c
printf("Riiiiight, %s",&buffer);
```

It uses `printf` to print our input and this time it uses a format specifier `%s` but the issue is this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92e5f2a3-d41e-460b-8139-85b6d86404bd)

So when `printf` is used it would print our input till it meets a null byte this means that if we give it a specific amount of bytes let's say we full the buffer with characters it would leak values
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c09963b3-bbca-4029-b9b4-bd72602a7b45)

In this case our buffer can hold up to `32` bytes of data so I did some trial and error and got the best leak to be at `31` bytes

With that said the leak turned out to be a binary section address and I just calculated the offset to the elf base address 

From here since the second `fgets` gives us a buffer overflow we can calculate the offset to overwrite the instruction pointer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9327b9b8-c1ee-43fe-b44d-3039b11cb4c3)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ea0bfcda-8752-4869-a344-8e2a8f605928)

It is `56`.

With this we can just perform a ROP technique called Ret2Libc

But initially I was trying to call `execve()` since it had some available gadgets but it didn't work cause we need `/bin/bash` to be placed somewhere in the binary but that I couldn't do 

So I just went with `Ret2Libc`

Basically what that would do is this:
- Leak the address of `printf@got` using `printf@plt`
- Jump back to the `main address + 0x1231` to avoid stack allignment
- At this point we have the libc base address then we can either jump to a `one_gadget` or do `system(/bin/sh)`

Here's my solve [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/cyberlympics22/prequal/Robin/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96af0a3c-dab2-4bf7-8ead-54c74c812c4d)

### Reverse Engineering

#### 34sy-r3v
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b5ce6ea-5369-4e1b-a00a-25b70aff3cf5)

First I ran the binary to know what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c0e9f6cf-c6e6-46bb-9c04-830e057a16dd)

It asks for a pin

I used `ltrace` which is a library trace to know what's happening 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/805451fc-3192-46b6-be6c-21fe07c9bb6d)

It uses `strcmp` of our input with the flag

So I just ran the `strings` command and grep for the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/628abe2a-851c-45cd-85ad-f778e1a36309)

```
Flag: acdfCTF{5tr1ngs_b1n4ry_t0_g3t_fl4g}
```

#### CodeX 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/551a7607-f318-413a-8c22-88c20bd0536f)

First thing I did was to run it to know what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b5085ce0-1ee7-4595-b63c-0b8a72f426a8)

We can use `ltrace` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b76673b1-9ddd-479a-bc6c-822320c4e78e)

Ok it uses `strcmp` but this time around we can't use `strings` command cause it's likely not hardcoded in the binary
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e1fdfd3b-230e-436f-bb45-9993dace4aa8)

I opened it in gdb got the list of function available
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8f846451-4dbc-4819-8b74-585b46e44c5a)

Since it uses `strcmp` therefore our input would be in the `rdi` register while the expected value would be in the `rsi` register

So I set a breakpoint before the `strcmp` call
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/356e8d63-1a73-4aab-9f6c-dcf5473dd9db)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4b0c3779-f402-4f99-9e44-af7a848e5e82)

Now when we run it we would get the flag in the `rsi` register
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0f53bdc1-a30b-40e2-83bd-226524c84251)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2e739593-b5c3-4e7b-8f77-f5eda01d6303)

```
Flag: acdfCTF{Th3_p3rf3ct_r3c1p3_for_3t3rn1ty_l1f3}
```

And that's all :P

I played with team `sudoers` and we got `3rd`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f4727fc1-1d37-4b5d-a357-624ead8cf1a4)



