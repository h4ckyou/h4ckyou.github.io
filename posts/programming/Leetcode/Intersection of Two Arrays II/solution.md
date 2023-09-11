<h3> Intersection of Two Arrays II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2c91159c-660b-4a1d-a6f9-2d13797da8f8)

This is part two of the `Intersection of Two Arrays`

The difference here is that each element in the result must appear as many times as it shows in both arrays

So let us consider this two arrays:

```
num1 = [1, 3, 5 3]
num2 = [3, 3]
```

The result we should be expecting is `[3, 3]` and why?

Well I solved mine based on how many times can each element in `num2` appear in `num1`

It can be vice versa but more ideal to use the array of lower size

I saw that my previous `Overkill` script takes too much in terms of speed

So I decided to optimize using Hash table

The idea is this:
- Create a hashtable to hold up the count of occurrence of each element in array 1
- Iterate through the second array and check if the element is in the count:
  - If it is, I'll decrement the count in the hash table and add it to the result array
 

With that this program is way more optimized than before :P
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fe27ce47-64e1-40b0-9580-e448eb1eadb9)

But in terms of Space Complexity the Big O is `O(min(N, M)), where N is the length of nums1 and M is the length of nums2.`

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Intersection%20of%20Two%20Arrays%20II/solve.py)
