<h3> Two Sum II - Input Array Is Sorted </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7431e8ae-0331-4603-b8f1-d78f405ae19a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/207c7bcf-1cc2-477d-b929-c5233e3c540d)

### Approach

We are given an array starting from index `0` which is already sorted in a non-decreasing order.

Our goal is to find two numbers such that they add up to the `target` value and return the indices of the two values of the array

#### Constraints:

```
- 2 <= numbers.length <= 3 * 104
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order.
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution.
```

Since the array is already sorted I can actually implement Binary Search to solve it

But I took another approach which makes use of a hash table

The idea is that I'll have a hashtable which would hold each element and it's index and during the iteration I'll check if the `complement` resides in the hashtable

I defined the `complement` as the difference between the `target` value and `array[i]`

If we happen to get a complement which resides in the hashtable we'll then return `[hastable[complement]+1, i+1]`

I'm incrementing by `1` because in my program I made use of `enumerate()` making it start from index `0` instead of `1`

P.S I would have been giving screenshots of the drawing but the issue is I use Linux so I don't have any tool where I can freely draw stuffs so therefore, my drawings and thought process are like on my book :P

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Two%20Sum%20II/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/31eba667-ef32-4c64-956f-999bc0455c63)
