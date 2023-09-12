<h3> Majority Element </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9036ec1c-9d08-45a0-9f16-3b46d76ae99d)

Here's my thought process:

```
1. We are given an array `nums` of size `n` and our goal is to return the majority element in the array
2. Majority element is defined as that element which appears more than `n/2` times
3. So lets say I have an array of size 10 the majority element should occur more than 5 times
4. To solve this I'll make a hash table which holds all the occurrence of elements in the array, then I'll check if it meets that condition and I will be expecting it to reach because the description of the challenge says we may assume that the majority element always exists in the array
```

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Majority%20Element/solve.py)

![hashtable](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a19e51a3-e8d1-40a4-8c15-c93d9df0140b)
