<h3> Find the Index of the First Occurrence in a String </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/faeee16b-f7c5-4c32-aba8-d2a1220d53f5)

Solve Script:

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle in haystack:
            return haystack.index(needle)
        else:
            return -1

```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/769b99f4-6248-4502-8013-318f05c22f2d)
