<h3> Binary Tree Postorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7581c295-421e-4f29-add1-3948997cff1e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/672a35ec-2862-4178-90d8-7e533fe69f28)

We are going to be given a binary tree and our goal is to return the postorder traversal of its node's values

I already solved the other ways of traversing binary trees [one](https://h4ckyou.github.io/posts/programming/Leetcode/Binary%20Tree%20Inorder%20Traversal/solution.html
) and [two](https://h4ckyou.github.io/posts/programming/Leetcode/Binary%20Tree%20Preorder%20Traversal/solution.html) you can check it out!

So for this method the rule is:
- Traverse the left subtree recurisvely postorder
- Traverse the right subtree recurisvely postorder
- Traverse the current node

Let's take this binary tree as an example:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed274586-8dac-4a55-8bab-0de6260b9776)

The parent node which I'll refer as the key is `3` and it has two children nodes connected to it `2` and `4`

For us to Traverse using Postorder method I'll do this

First I'll traverse the left subtree so that means I'll need to visit all the left nodes from the left node connected to the key and add to my list

In this case there just two left nodes in the left subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f39ff41f-3725-4234-baee-a7807e1b3482)

So the list result would be `[1, 2]`

Now we move to the right subtree which is starting from `4`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bc7b5c18-e38a-4de4-ab44-ce4bc2954766)

The node of value `4` has two children which are `6 and 5` 

Since `6` is a left node we'll first visit it before moving to the right node that's because the rule says we should traverse the `left` before `right` then `current node`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c21d5fb3-a65d-4d7a-bcfe-dc8ad24ed4d1)

At this point we've applied the first and second rule so our list should hold `[1, 2, 6, 5]` 

To accomplish the last rule we'll visit the remaining current nodes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/44e4081b-f956-4f95-9e58-391e8c3ed6fe)

Therefore the final result will be `[1, 2, 6, 5, 4, 3]` 

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
