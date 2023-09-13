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
If x == 1 --> is there any single value in the nums array that is greater than or equal to one? --> True
```

When `x` is 2:

```
If x == 2 --> are there any two numbers in the nums array that are greater than or equal to two? --> True
```

When `x` is 3:

```
If x == 3 --> are there any three numbers in the num array that are greater than or equal to three --> True
```

When `x` is 4:

```
If x == 4 --> are there are four numbers in the num array that are greater than or equal to four --> False
```

This case returned False this means that the previous result is what will be returned as it returns True so the answer is `3`

After I understood that I was able to come up with an idea I can use to implement this and find the value of `x`:
- Initialize variable `x` as `1` because from the constraint, `1 <= nums.length <= 100` and I'll be using that in the future of this program
- In a while loop I'll iterate till `x` is less than or equal to the length of the array i.e `x <= len(nums)`
- I set a variable `count` as `0,` then I iterate through all the numbers in the number array on each iteration I'll check if `number >= x` which is the condition required for us to perform
- If that is True then I'll increment variable `count` by `1`
- I'll check if `count == x` and if it is, I'll return `x`
- Else I'll increment `x` by `1`
- If after the loop and no values is found I'll return `-1`

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Special%20Array%20With%20X%20Elements%20Greater%20Than%20or%20Equal%20X/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64142ec0-6126-4241-8a17-5113a491aa29)

My approach is Ok but not well optimized 

Anyways after looking at others solution I found this approach which made use of Binary Search

Here's the way it was used:
- It initialized `left`, `right` to it's corresonding value (the standard stuff xD)
- In a while loop, we calculates the mid value
- Inside the loop, we use a list comprehension and the sum function to count the number of elements in `nums` that are greater than or equal to `mid`. This count is stored in the variable count.
- We then shift the search range depending on the value of `count`

Here's the script implementation:

```python
def specialArray(nums):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        count = sum(1 for num in nums if num >= mid)

        if count == mid:
            return mid
        elif count > mid:
            left = mid + 1
        else:
            right = mid - 1

    return -1

nums = [0,4,3,0,4]
r = specialArray(nums)

print(r)
```

It works pretty well
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8145e109-87ce-4ec5-9858-87164c75ca2a)

