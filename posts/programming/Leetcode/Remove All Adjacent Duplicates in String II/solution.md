<h3> Remove All Adjacent Duplicates in String II </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e932d79e-cb6d-4401-b7cb-a70efd9ccd9e)

My first approach to solve this works but the issue was the order of the return value wasn't the same in the original string which made it fail
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/992e0b3b-4f39-40fc-b58d-da25cc4a43d7)

But here's the solve script:

```python
def removeDuplicates(s, k):
    ht = {}
    r = []

    for i in s:
        if i in ht:
            ht[i] += 1
        else:
            ht[i] = 1
        
    for key, value in ht.items():
        check  = value % k
        if check < k:
            r.append(key * check)

    return "".join(r)

s = "yfttttfbbbbnnnnffbgffffgbbbbgssssgthyyyy" 
k = 4
r = removeDuplicates(s, k)

print(r)
```

So I implemented another appraoch which made us of Stack Data Structure

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Remove%20All%20Adjacent%20Duplicates%20in%20String%20II/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00574063-bbde-451a-bc61-455298f2e425)
