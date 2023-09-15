<h3> Remove Elements </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e9fc9c49-ea66-4eae-b521-72351345cd8e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e822dc69-9755-4204-9f19-5a8de0fe538c)

Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` [in-place](https://en.wikipedia.org/wiki/In-place_algorithm). The order of the elements may be changed. Then return the number of elements in `nums` which are not equal to `val`.

Consider the number of elements in `nums` which are not equal to `val` be `k`, to get accepted, you need to do the following things:
- Change the array `nums` such that the first `k` elements of `nums` contain the elements which are not equal to `val`. The remaining elements of `nums` are not important as well as the size of `nums`.
- Return `k`.

I just solved this using array method `pop()`

My solve script is in the below link

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Remove%20Elements/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/720d890e-558a-444c-8ef3-cdf66be2ea1a)

Another efficient way to solve this is using Two Pointer

```python
def removeElement(nums, val):
  index = 0
  
  for i in range(len(nums)):
      if nums[i] != val:
        nums[index] = nums[i]
        index += 1
  
  return index
```

#### Leetcode Submission Script

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        i = 0

        while i < len(nums):
            if nums[i] == val:
                nums.pop(i)
            else:
                i += 1
        
        return len(nums)
```

