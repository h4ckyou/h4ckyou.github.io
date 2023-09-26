<h3> Cyberlympics CTF </h3>

![img](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7191729-17fe-43bc-a337-c2bae7e1d203)

Hi! In this writeup I'll give the solution to all the binary exploitation challenges. Maybe if I have time and I'm online I'll try put the other challenge I solved

Have fun reading!

#### Flag Bank (1st Blood 🥇)
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

Here's my solve [script]()
