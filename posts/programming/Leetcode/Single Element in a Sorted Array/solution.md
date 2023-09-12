<h3> Single Element in a Sorted Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3102f722-59e9-4b13-b6f5-36de965430e5)

# Intuition

Looking at the problem we can tell we'll be given an array `nums` and we're too basically find that element in the array which only appears once

A good way to start is to try solve this using a brute force approach as it helps to confirm if there's a solution to this problem

And basically my brute force approach would use Linear Search which basically does this:
- Iterate through the array and if `array[i] != array[i-1]` and `array[i] != array[i+1]` that means the non duplicate value is `array[i]`
- There are cases we should check like if `len(array) == 1` then we return `array[0]` because there's only one element in the array

Here's the implementation:

```python
def singleNonDuplicate(array):

    if len(array) == 1:
        return array[0]

    for i in range(1, len(array)-1):
        if array[i] != array[i-1] and array[i] != array[i+1]:
            return array[i]


nums = [1,1,2,3,3,4,4,8,8]
r = singleNonDuplicate(nums)

print(r)
```

That works but the problem with it is the complexity:

```
Time Complexity: O(N)
Space Complexity: O(1)
```

So now we can optimize the program

The way I'll do it is using Binary Search

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Single%20Element%20in%20a%20Sorted%20Array/solve.py)

It works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f9b573f8-235d-457c-8e9a-83e6244d4d2b)
