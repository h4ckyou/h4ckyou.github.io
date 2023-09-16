<h3> Happy Number </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/94419191-a3f5-4f9a-b9fa-d742304e6040)

Write an algorithm to determine if a number `n` is happy.

A happy number is a number defined by the following process:
- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if `n` is a happy number, and false if not.

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Happy%20Number/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/72865484-fde4-4e53-99ba-a71f1ceac00c)


#### Leetcode Submission Script

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        n=str(n)
        ch=False
        if n=='1':
            ch=True
        else:
            while n not in ('2', '3', '4', '5', '6', '8','9'):
                print(n,1)
                s=0
                for i in n:
                    s+=int(i)**2
                if s==1:
                    ch=True
                    break
                else:
                    n=str(s)
        return ch
```
