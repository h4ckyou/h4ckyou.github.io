<h3> Contains Duplicate </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d8f214d6-f28e-42fd-b950-753a7ea14c50)

Here is my thought process:

```
1. We are given an integer array and we're to return "true" if any of the number in the array appears at least twice and "false" if the numbers in the array are distinct
2. First I will create a hash table containing each elements in the array and it's corresponding occurrence, then I'll iterate through the hash table values and see if any is greater than 2 or not
If it is then I'll return "true" else "false"
```

And my solve script:

```python
def containsDuplicate(nums):
    array = nums
    counter = {}

    for i in array:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    
    for i in range(len(counter)):
        if list(counter.values())[i] >= 2:
            return True

    return False
    
nums = [2,14,18,22,22]
r = containsDuplicate(nums)

print(r)
```

Running it works but when I did it on the challenge platform I got a `Time Limit Exceeded`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/abe438f6-e616-4e5c-b57b-d9d076fa3f9c)

So I need to optimize the program to use less time

The reason why I'm getting Time Limit Exceeded is because I tend to loop over each element in the array to get it's corresonding occurrence

Then I'm looping over the hash table values to find any value that's greater than or equal to two

In a case where that element occurs first then I'll program runs quickly but in some case the value might be as the last value in the hash table or array

And the maximum length that can be our input is `100,000` while the element in the array maxiumum value can be `1,000,000,000`

We should always consider the worst case scenerio as it helps us optimize our code

After few minutes of thinking I figured I could optimize the second loop using Binary Search

Since I will sort the `counter.values()` values therefore any number that's greater than or equal to our target value which is `2` then the function should return `True` as we are not exactly looking for number `2` but we are looking for any number which is at least `2`

Here's my final script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Contains%20Duplicate/solve.py)

It's not too good in terms of speed and memory but it does the job
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e96b452-1af0-421d-a831-474e7e912176)

After looking at other people approach I saw that my script efficiency was too low as there are way more easier ways of solving this :D

I don't know why I over think things :P

Anyways the idea behind this one I found interesting is this:

Approach solving using sorting:

```
The sorting approach sorts the array in ascending order and then checks for adjacent elements that are the same. If any duplicates are found, it returns true. Sorting helps in bringing duplicates together, simplifying the check. However, sorting has a time complexity of O(n log n).
```

Here's the code snippet

```python
    def containsDuplicate(nums):
        nums.sort()
        n = len(nums)
        for i in range(1, n):
            if nums[i] == nums[i - 1]:
                return True
        return False
```

And here's a more efficent one:

```python
def containsNearbyDuplicate(nums):
    hashtable = {}

    for num in nums:
        if num in hashtable:
            return True
        hashtable[num] = num

    return False

nums = [1,2,3,1]
result = containsNearbyDuplicate(nums)
print(result) 
```

The idea is to create a hash table which stores each element of the array and then if it appears again then there's a duplicate and it returns True else if there's no occurrence of two elements in the hash table we return False
![wow](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d772ec51-f83d-4818-a38f-9348282b3df3)


