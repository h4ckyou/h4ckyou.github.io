<h3> Kth Missing Positive Number </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4dbc6d56-931c-4485-8f1e-265b6ea8af02)

We are given an array which is sorted in increasing order with an integer `k`

Our goal is to return the `Kth` positive integer that's missing from the array

#### Approach

One way we can easily solve this is:

First we can store a list of possible values within a specific range in this case I used `5001` in an array `possible[]`

Now I can iterate through each values in the `possible[i]` and see if the iterate isn't among the `array[j]`

Is that returns True I'll save those elements in another array `missing` then return the `kth` missing value which we can represent as `missing[k]`

That said it's pretty simple but the issue is what if our `kth` value is more than the value in `possible` that would return an error!

Also it's efficiency is bad
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8a75efa6-48a9-4b05-b031-326b88cb4949)

It uses much space and time because we're storing a large value in memory and iterating through a large array

So let's optmize that!

Instead of using lot of memory we can optimize that 

I'll keep the current number not in the array in a variable and keep track of when we get the `k` which would be possible if I make a variable `count` that increments on each check of `currentNumber`
