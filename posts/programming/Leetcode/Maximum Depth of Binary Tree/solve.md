<h3> Maximum Depth of Binary Tree </h3> 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c524bedd-fc53-42e5-90cc-cf7b6bf04516)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df15a679-9d2b-4561-88da-1bc331d78d2d)

We will be given a binary tree and we're to return the maximum depth

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.



Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Maximum%20Depth%20of%20Binary%20Tree/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4c43388b-5b55-43f2-84bc-157530e0d3e1)


#### Leetcode Submission Script

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        return 1 + max(Solution.maxDepth(self, root.left), Solution.maxDepth(self, root.right))
```
