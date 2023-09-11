<h3>  Intersection of Two Arrays </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f31f4959-d492-4bee-aae7-7c9f471dc034)

We can easily implement python builtins function to solve this:

```python
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        num1 = set(nums1)
        num2 = set(nums2)

        intersect = num1.intersection(num2)
        return list(intersect)
```

But I will implement Binary Search to solve this

