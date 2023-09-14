<h3> Binary Tree Postorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7581c295-421e-4f29-add1-3948997cff1e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/672a35ec-2862-4178-90d8-7e533fe69f28)

We are going to be given a binary tree and our goal is to return the postorder traversal of its node's values

I already solved the other ways of traversing binary trees [one](https://h4ckyou.github.io/posts/programming/Leetcode/Binary%20Tree%20Inorder%20Traversal/solution.html
) and [two](https://h4ckyou.github.io/posts/programming/Leetcode/Binary%20Tree%20Preorder%20Traversal/solution.html) 

So for this method the rule is:
- Traverse the left subtree recurisvely postorder
- Traverse the right subtree recurisvely postorder
- Traverse the current node

Let's take this binary tree as an example:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed274586-8dac-4a55-8bab-0de6260b9776)

The parent node which I'll refer as the key is `3` and it has two children nodes connected to it `2` and `4`

For us to Traverse using Postorder method I'll do this

First I'll traverse the left subtree


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
