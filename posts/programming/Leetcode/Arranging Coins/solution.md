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

4 coins      2 coins      incomplete .....................
```

We can also draw the block form of it 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e5e32ab-922e-4478-809b-9fa14639f7db)

So basically we can form 2 coin staircase out of 5

That will sound confusing but here's what I mean:

```
1 == 4 coins
2 == 2 coins
3 == incomplete
```

So let's say we're counting from 0 and our current coin is 5

That means when we reach `i` the coin will reduce by `coin-i`

We reach 2 the coin will reduce by 2 i.e `current_coin - count`

We reach 3 the coin will reduce by 2 but now the problem is there's one left i.e `current_coin - count ==  2 - 3`

That makes it incomplete

And the task here is saying we should find the number of rows of `n` which means that we should find how many rows can `n` make  to form a staircase excluding the incomplete coin

That might not also sound too good I'm sorry for that I don't know how to visualize it for you :(

But this is what I discovered:

We can determine when the value has become imcomplete when the next counter is greater than the previous coin value

Let us take our case sample as example

```
counter = 0
coins = 5

1 --> 2 --> 3
4 --> 2 --> ?
```

We can see that if the next counter value which in this case is `3` is greater than the previous coin value which is `2` therefore the next coin value will be incomplete

To confirm that I tried it over various test cases and it returned True 

So now we just need to find a way to get the rows and that part is pretty easy if you figure it out

Here's what I did:
- Initialize an array to hold the current coin value
- In a for loop iterate through the range(1, coins)
  - On each iterate append the difference of the last value of the array with the iterate value
- To check is we have meet the incomplete coin case I'll check if `i+1` is greater than `array[-1]`, if it is then I'll break out of the loop
- The return value should exclude the initial coin value at the 0th index since it isn't needed, therefore the return value would be `array[1::]`

That's basically what my script does:

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Arranging%20Coins/solve.py)

```python
def arrangeCoins(coins):
    rows = [coins]

    if coins == 1:
        return 1

    for i in range(1, coins):
        rows.append(rows[-1] - i)
        
        if i+1 > rows[-1]:
            break
    
    return len(rows[1::])


n = 10
r = arrangeCoins(n)

print(r)
```

After running it I saw that the efficiency isn't that good so on looking at other solution I found this:

##### Approach

Suppose we have the input value n = 8.

    Initialize num as 8 and count as 0.
    Start the outer loop with i = 1:
        On the first iteration:
            Start the inner loop with j = 0.
                Since j is less than i and num (8) is greater than 0, enter the loop.
                Decrement num by 1. Now num = 7.
                Increment j to 1.
            Continue the inner loop:
                Since j is less than i and num (7) is greater than 0, enter the loop.
                Decrement num by 1. Now num = 6.
                Increment j to 2.
            Continue the inner loop:
                Since j is equal to i (2) and num (6) is greater than 0, increment count by 1. Now count = 1.
        On the second iteration:
            Start the inner loop with j = 0.
                Since j is less than i and num (6) is greater than 0, enter the loop.
                Decrement num by 1. Now num = 5.
                Increment j to 1.
            Continue the inner loop:
                Since j is equal to i (1) and num (5) is greater than 0, increment count by 1. Now count = 2.
        On the third iteration:
            Start the inner loop with j = 0.
                Since j is less than i and num (5) is greater than 0, enter the loop.
                Decrement num by 1. Now num = 4.
                Increment j to 1.
            Continue the inner loop:
                Since j is less than i (2) and num (4) is greater than 0, enter the loop.
                Decrement num by 1. Now num = 3.
                Increment j to 2.
            Continue the inner loop:
                Since j is equal to i (2) and num (3) is greater than 0, increment count by 1. Now count = 3.
        The outer loop continues until num is no longer greater than 0.
    Exit the outer loop.
    The function returns count, which is 3.

In this example, the function arrangeCoins determines the number of complete rows of coins that can be arranged based on the input value n = 8. The result is 3, indicating that 3 complete rows of coins can be arranged.
Complexity

    Time complexity:O(n2)O(n^2)O(n2)

    Space complexity:O(1)O(1)O(1)


Code Implementation:

```python
class Solution:
    def arrangeCoins(self, n: int) -> int:
        if n == 1:
            return 1
        
        for i in range(1, n + 1):
            n -= i
            if (n < 0):
                return i - 1
```

It's pretty neat compared to mine which takes more time and space than this code snippet does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3a7798ca-a408-4f58-9330-2b65be00035f)




