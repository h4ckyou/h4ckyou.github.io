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


