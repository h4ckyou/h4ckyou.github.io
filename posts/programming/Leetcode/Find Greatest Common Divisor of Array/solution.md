<h3> Find Greatest Common Divisor of Array </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/da035b31-e0e2-458c-be39-0231396991c4)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9dab1b94-9b90-486e-948e-0e75544f679a)

Given an integer array `nums`, return the greatest common divisor of the smallest number and largest number in nums.

The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.

To read more on `gcd` check out [here](https://byjus.com/maths/greatest-common-divisor/)

The way I'll solve it is using recursion

Here's my solve script

```python
class Solution:
    def findGCD(self, nums: List[int]) -> int:
        def gcd(a, b):
            if b == 0:
                return a
            else:
                return gcd(b, a % b)
        
        nums.sort()
        a,b = nums[0], nums[len(nums)-1]
        r = gcd(a, b)

        return r
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/96c5a675-02e6-488e-95b3-f78204074a8c)
