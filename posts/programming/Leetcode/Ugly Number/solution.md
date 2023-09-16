<h3> Ugly Number </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f1fe1f9c-8b91-4bda-8dd7-a6efbd9e3342)

An ugly number is a positive integer whose prime factors]( are limited to `2, 3, and 5`.

Given an integer `n`, return true if `n` is an ugly number.

So basically what this task is asking us to do is to find the prime factors of a given number and check if it's factor are within the positive integer

Let's say I have a number `6`, the prime factors of `6` are `2 and 3` 

Since the prime factors are within the constraint factors then we return True

Let's take another number `14` , the prime factors are `2 and 7`

Since it isn't within the constaint factors i.e 7 isn't within the constraint factor then we return False

So my approach to solve this is to get the prime factors of a given integer `n` and check if it meets the constaint

To get the prime factors (Prime Factorization) we can follow this [process](https://www.mathsisfun.com/prime-factorization.html):
- While `n` is divisible by `2`, append `2` to my factor list then divide `n` by `2`.
- After that, `n` must be an `odd` number. Now start a loop from `i = 3` to the square root of `n` and incrementing by `2`.
- While `i` divides `n`, I'll append `i` to my factors list and divide `n` by `i`.
- If `n` is greater than `1` I'll append it to my factors list and return the list

With that we would have the prime factors of the integer

The time complexity of this process is dependent of the size of the integer

I would have used [Fermat's Factoring Method](https://www.youtube.com/watch?v=tKTNVmnW_4w&list=PLBlnK6fEyqRgJU3EsOYDTW7m6SUmW6kII&index=52) but the issue it's designed to find two factors of a composite integer.

If the composite integer has more than two prime factors, we may need to apply the method multiple times to find pairs of factors iteratively until you have factored the number completely.

That process itself is dependent of the size of the integer so I'm going with the normal process

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Ugly%20Number/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7db98592-49d4-40ce-8782-ef4768c67883)

