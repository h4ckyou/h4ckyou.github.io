<h3> Reverse String II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/270f463e-a4cf-4873-a80d-38517e3478cc)

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Reverse%20String%20II/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1fc49cd9-33ba-42df-9beb-2f880bdf8834)


#### Leetcode Submission Script

```python
class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        result = []
        reverse = True 

        for i in range(0, len(s), k):
            chunk = s[i:i + k]
            if reverse:
                result.append(chunk[::-1])
            else:
                result.append(chunk)
            reverse = not reverse

        return "".join(result)
```
