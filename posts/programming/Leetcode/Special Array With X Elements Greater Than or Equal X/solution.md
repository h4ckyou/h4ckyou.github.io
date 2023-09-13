<h3> Special Array With X Elements Greater Than or Equal X </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f700a22-c323-4f60-9f4f-c3826de48c1e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5a198f0d-f207-404c-a667-d792892df750)

We are given an array `nums` of non negative integers. We can say `nums` is special if there exists a number `x` such that there are exactly `x` numbers in `nums` that are greater than or equal to `x`

The idea is simple we just need to find a number `x` such that there are exactly `x` numbers in the array `nums` that are greater than or equal to `x`

Let's take a example:

```
nums = [3, 5]
```

I'll take `x` as 1:

```
If x == 1 --> is there any single number in the nums array that is greater than or equal to one?
```

In this case it returns True because there are two various numbers that meets the condition

Let's take `x` as 2:

```
If x == 2 --> are there any two numbers in the nums array that are greater than or equal to two?
```

Looking at the condition we can tell that there are two numbers in the array that meet the condition

So the answer we would return is `2` and not `1` because it kinda takes the highest value 

From this first case I was able to conclude that the value of `x` doesn't essentially need to be in the array but it must be less than or equal to the length of the array i.e `x <= len(nums)`

Let us take another example:

```
nums = [0, 4, 3, 0, 4]
```

I'll take `x` as 1:

```
If x == 1 -->
```

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Special%20Array%20With%20X%20Elements%20Greater%20Than%20or%20Equal%20X/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64142ec0-6126-4241-8a17-5113a491aa29)
