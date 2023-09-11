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

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Intersection%20of%20Two%20Arrays/solve.py)

My script is quite a bit of an overkill and you can tell that the time it takes is pretty not efficient
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f8e16d0a-7196-48b5-9f19-44bb850bf48d)

Also I was doing lots of debugging hehe :P
