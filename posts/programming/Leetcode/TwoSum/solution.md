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

Submitting it finally worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ec2a0c85-9f9f-4574-8493-c81f5d45bede)

But looking at the Runtime and Memory it used we can see that this isn't a good approach

So I decided to try a better way of solving this

I tried to implement using Binary Search

And here's the explanation

Consider this array and target value:

```
nums = [9,3,1,4,5,2,8,6,10,7]
target = 6
```

For we to work with Binary Search the array needs to be sorted

So I'll sort it out, get the left & right value and take the sum of the value in the left sorted array with the right last value

```
>>> nums = [9,3,1,4,5,2,8,6,10,7]
>>> target = 6
>>> 
>>> array = sorted(nums)
>>> left = 0
>>> right = len(array) - 1
>>> sum = array[left] + array[right]
>>> sum
11
>>>
```

We can see that the sum is greater than the target value, so we'll move the search space to the left by 1

```
>>> right -= 1
>>> sum = array[left] + array[right]
>>> 
>>> sum
10
>>>
```

The sum is greater than the target so I'll move the search space to the left by 1

```
>>> right -= 1
>>> sum = array[left] + array[right]
>>> 
>>> sum
9
>>>
```

Basically we'll keep on going till we get this

```
>>> right -= 1
>>> sum = array[left] + array[right]
>>> 
>>> sum
6
>>>
```

At this point the sum is equal to the target value

Now we'll get the value of `array[left] & array[right]`

```
>>> array[left]
1
>>> array[right]
5
>>>
```

Because the array has been sorted we'll need to get it's corresponding index from the original array

We can just use python `index()` function to do this

```
>>> nums.index(1)
2
>>> nums.index(5)
4
>>>
```

Cool the index is `[2, 4]` and that will be our answer

To confirm we can sum the values of `nums[2]` and `nums[4]` and we know it will return `6` becasue it's value is `2 & 4`

```
>>> nums[2] + nums[4]
6
>>>
```

That's the solution!

So I wrote a script to implement this

```python
def twoSum(nums, target):
    array = sorted(nums)
    left, right = 0, len(array) - 1
    result = []

    while left <= right:
        sum = array[left] + array[right]

        if sum == target:
            result.append(nums.index(array[left]))
            result.append(nums.index(array[right]))
            return result

        elif sum > target:
            right -= 1
        
        else:
            left += 1

    return None
            
nums = [9,3,1,4,5,2,8,6,10,7]
target = 6

result = twoSum(nums, target)
print(result)
```

It works but then I saw an issue

If I run it against this test case it doesn't return the right value

```
Input: nums = [3,3], target = 6
Output: [0,1]
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/26e71023-7f7a-4559-adad-08fb05ed30d4)

I spent some time trying to fix that but failed 😢

So after looking through the Editorial I saw they used a more faster algorithm `Two-pass Hash Table`

Algorithm: 

A simple implementation uses two iterations. In the first iteration, we add each element's value as a key and its index as a value to the hash table. Then, in the second iteration, we check if each element's complement `target - nums[i]` exists in the hash table. If it does exist, we return current element's index and its complement's index. Beware that the complement must not be `nums[i]` itself!

Let me explain it:

Consider this array of numbers:

```
nums = [9,3,1,4,5,2,8,6,10,7]
target = 11
```

First we'll iterate through the values in the nums array taking it's complement and keeping the progress in a dictionary defined as this: `{integer: index}`

```
11 - 9 = 2
```

Our hash table dictionary will be this:

```
{9: 0}
```

We go over the second index

```
11 - 3 = 8
```

Hash table dictionary

```
{3: 1}
```

During this iteration we'll check if the current complement is in the hash table dictionary 

```python3
if complement in hashtable:
```

If that returns True that means we've found a number that meets the condition required for this task

And we'll return the index of the position of the current complement with the iterate

```
[hashtable[complement], i]
```

With that said I made a script to do that

```python
def twoSum(nums, target):
    hashtable = {}

    for i, j in enumerate(nums):
        complement = target - j

        if complement in hashtable:
            return [hashtable[complement], i]

        hashtable[j] = i

    return None

nums = [2,7,11,15]
target = 17

result = twoSum(nums, target)
print(result)
```

Submitting it we can see it works pretty good
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b4b0136e-0b16-44a7-8b23-1539b3369d2c)

In terms of speed it was way faster but in memory it is consumes some amount of memory and that's because each iterate is stored in the dictionary

That's all!
