<h3> First Unique Character in a String </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c09fb7f5-62c6-49ff-a7e7-4f193784f4d1)

To solve this I implemented Hashtable Data Structure and here's the solve script [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/First%20Unique%20Character%20in%20a%20String/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ef931cf7-8b02-4291-a0a1-2b76e29baec0)

Another way to go about this is via Queue Data Structure

And here's the implementation

```python
from collections import Counter, deque

def firstUniqChar(s):
    c = Counter(s)
    q = deque()
    r = 0

    for char in s:
        q.append(char)
        if c[q[0]] > 1:
            while q and c[q[0]] > 1:
                q.popleft()
                r += 1
        else:
            return r
        
    return -1

s = "loveleetcode"
r = firstUniqChar(s)
print(r)
```
