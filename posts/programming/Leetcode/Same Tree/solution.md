<h3> Same Tree </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/66aa76bf-f990-4683-8a33-59cb61c145c1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2356a30d-a9cc-45e6-9df3-302833af631f)

Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are `structurally identical`, and the nodes have the `same value`.

So we'll be given two binary trees `p and q` and our goal is to check if they are the same or not

Let's consider this two binary tress `A` and `B`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ca021b51-37c2-4c2b-be98-d098fd8637d3)

From that we can see the best way to know if the nodes have the same value is by traversing and comparing it

So the next thing is how to determine if they are of the same structure

Luckily we can check for that using recursion and for every recursion we check if the nodes of `p` and `q` are None, if they are it means they have the same structure, then we can check if the node `p` happens to be None or vice versa

If that is the case then they are not of the same structure

At the point of each recursion we can check if the key value of `p` and `q` are the same

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Same%20Tree/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/49afe9f1-745d-4294-8790-0309eee24eec)


#### Leetcode Submission Script

```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:
            return True
        
        if p is None or q is None:
            return False
            
        return (p.val == q.val) and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```
