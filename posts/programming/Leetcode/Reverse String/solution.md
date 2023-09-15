<h3> Reverse String </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee965db6-5277-40fd-915c-e5f8fb54d2b5)

We are to reverse a string without using memory this method is called `in-place` algorithm

Basically the idea to solve this is:
- When we split the string in half we can reverse them using this `s[i], s[n-i-1] = s[n-i-1], s[i]`

There are other ways to reverse a string but this method changes the value in memory and does not require much memory usage

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Reverse%20String/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c572542-653c-41bf-879d-81b3e0c98cf3)

#### Leetcode Submission Script

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        n = len(s)
        for i in range(n//2):
            s[i], s[n-i-1] = s[n-i-1], s[i]
        

```
