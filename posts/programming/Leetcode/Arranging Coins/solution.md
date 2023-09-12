<h3> Arranging Coins </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39ae173b-cc5b-423e-a71c-f25fc29bbc68)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3236ab08-c1e2-4fe8-8e40-b61ca49b0d97)

I solved this in a way that's not really optimized
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39f42264-929e-4957-a9c0-f23655152c52)

But still I'll give my thought process while solving this task

I was actually writing the drawings and my assumptions on a book since I don't have Paint Bar on Linux :D

Anyways let's get to it

<h4> Challenge </h4>

You have `n` coins and you want to build a staircase with these coins. The staircase consists of `k` rows where the `ith` row has exactly `i` coins. The last row of the staircase may be incomplete.

Given the integer `n`, return the number of complete rows of the staircase you will build.

###### Example
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/feb01a32-68d5-4aba-ba07-cffafff1cea4)

  Input: `n = 5`
  Output: `2`
  Explanation: `Because the 3rd row is incomplete, we return 2.`

So now we can say that this is the logic behind this:

```
Number of coins = 5

Counts:

1 ----------> 2 ------->---> 3 --------->-> 4 ----------> 5

4 coins      2 coinds      incomplete .....................
```

We can also draw the block form of it 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e5e32ab-922e-4478-809b-9fa14639f7db)

