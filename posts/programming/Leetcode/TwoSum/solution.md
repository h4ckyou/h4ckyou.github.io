<h3> Two Sum</h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c0750f84-c00f-4377-a161-013a5df972fe)

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

#### Solution

The task is that:

We'll be given an array of numbers and a target value

We are asked to return the index of two numbers from the array whose sum is the target value

```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

At first my thought was that this can be easily solved if the array length is small

Since it would be a brute force sort of solve

And what that will basically do is this!

Consider this array:

```
nums = [2,7,11,15]
target = 9
```

In two loops I'll compare the sum of each values of the array with the target value:

```
nums[i] + num[j] == target True | False
```

That would be in a loop of range `array.length()`

But you can tell that if the length is large then that increases the time complexity since it will perform multiple loops 

Here's a sample script to solve this:

```python
def brute(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    
    return None


nums = [2,7,11,15]
target = 9

result = brute(nums, target)
print(result)
```

Running that works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15c5cf95-eca2-4820-b21c-865e0b739211)

We can submit that on the platform too

But I noticed this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/88420a78-0787-4e64-84e9-e86e29b43d19)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f72772d1-ce58-4152-b65d-b9ba5ef6bb2d)

Well looking at that we can see it failed and that's True because I forgot the condition:

```
You may assume that each input would have exactly one solution, and you may not use the same element twice.
```

We can't use the same element twice

To solve that part I just add a check in my script to not use the same element and that can be done by starting the second nested loop from `i+1`

Here's it

```python
def brute(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
        
    return None


nums = [3,2,4]
target = 6

result = brute(nums, target)
print(result)
```


