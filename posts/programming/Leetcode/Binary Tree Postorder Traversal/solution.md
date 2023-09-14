<h3> Binary Tree Postorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7581c295-421e-4f29-add1-3948997cff1e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/672a35ec-2862-4178-90d8-7e533fe69f28)






Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Binary%20Tree%20Postorder%20Traversal/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f30415dc-bc94-4085-a008-67ccec5d8021)


#### Leetcode Submission Script

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        
        return (Solution.postorderTraversal(self, root.left) + Solution.postorderTraversal(self, root.right) + [root.val])
```
