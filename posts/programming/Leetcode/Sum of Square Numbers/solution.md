<h3> Sum of Square Numbers </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/850d1351-5457-490e-a7fc-eee2507f98c3)

Given a non-negative integer `c`, decide whether there're two integers `a` and `b` such that `a^2 + b^2 = c`.

First we know that we'll be given a positive integer and our goal is to determine is there are two numbers that when you take the sum of their square we get the integer as the answer

Here's my thought process:

We can try approach a brute force method and we can do that using two nested loops to represent `a` and `b` and check if it meets the condition

But that won't be well optimized

So let's take a look at the given equation:

```
a^2 + b^2 = c
```

Express `a` as the subject of the formular:

```
a = sqrt(c - b^2)
```

This concludes that:

```
a <= sqrt(c)
```

Now with that we can traverse for `a` in range `sqrt(c)` and do this operation:

First we need to know the value of `b^2` let's call it `bSquare`:

```
bSquare = c - a^2
```

From here we calculate this:

```
b = int(sqrt(bSquare))
```

Then to know if the value of `a` and `b` satifies the condition `a^2 + b^2 = c` we can check if `b^2 == bSquare`

Incase you don't get what that is here's it, remember from the intial equation we have:

```
a^2 + b^2 = c
```

At this point we have the value of `a` and `b` right?

So we can basically just check if the condition holds true for `a` and `b`

But at the same time we can check the condition if the equation is changed to this

```
b^2 = c - a^2
```

So that's what I did up there

For the square root part we can binary search it or just use python math package

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Sum%20of%20Square%20Numbers/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/712b7c35-3d8e-455e-94f4-4818b01cf4f5)
