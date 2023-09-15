<h3> Remove Duplicates from Sorted Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6f8ff25-ec4d-43f8-9329-846c3b812800)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c59a2949-a1dc-44be-aed3-6412da155d39)

I was writing the solution to this but my firefox crashed and I didn't save the commit yet
![lol](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/59be55f9-fbb5-4e87-ae3d-d5438bef73b7)

To rewrite that is stressfull so I'll just drop the solve script

But basically this involves Removing Duplicate from a Sorted Array using In-Place Algorithm

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Remove%20Duplicates%20from%20Sorted%20Array/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f56cc9ee-41fb-4ae0-9f76-b21cf5cfc9bf)


#### Leetcode Submission Script

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        replace = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i-1]:
                nums[replace] = nums[i]
                replace +=1 
        
        return replace
```
