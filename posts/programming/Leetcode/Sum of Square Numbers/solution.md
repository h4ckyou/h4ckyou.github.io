<h3> Sum of Square Numbers </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/850d1351-5457-490e-a7fc-eee2507f98c3)

Given a non-negative integer `c`, decide whether there're two integers `a` and `b` such that `a^2 + b^2 = c`.

First we know that we'll be given a positive integer and our goal is to determine is there are two numbers that when you take the sum of their square we get the integer as the answer

Here's my thought process:

We know that the range of both the two numbers would be less than the given integer

So with that we know that our search range will be within the integer

For the brute force we can do two nested loops to represent `a` and `b`

But that won't be well optimized as the time complexity would be `N^2`

Let's take a look at the given equation:

```
a^2 + b^2 = c
```

If we happen to get the value of `a` can we get `b` ?

Yes we can by making `b` the subject of the formular:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4ec5852a-f7fc-4ba2-9669-0de532999b81)

```
b = sqrt(c - a^2)
```

Now that we have the value of `a` and `b` during each iteration 

Solve Script: [link]()
