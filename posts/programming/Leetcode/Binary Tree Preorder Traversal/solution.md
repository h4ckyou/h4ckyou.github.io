<h3> Binary Tree Preorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a3404fd4-58d7-459a-a816-ec9767545ded)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5c9266aa-a5bd-4c5a-9d29-0e524bb38529)

We are going to be given a binary tree and our goal is to return the preorder traversal of its node's values

I covered the first method of Traversing Binary Tree in this [writeup](https://h4ckyou.github.io/posts/programming/Leetcode/Binary%20Tree%20Inorder%20Traversal/solution.html) you can check it out!

The rule of Preorder Traversal is this:
- Traverse the current node
- Traverse the left subtree recursively preorder
- Traverse the right subtree recursively preorder

Let's take an example! Consider this Binary Tree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/85d70b76-8218-426d-8705-81adfd0533e5)

What we can see is that the parent node which I'll call the key is `3` and it has two children `2 and 4` 

In order to traverse using the preorder method I'll start from the current node which is `3`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/752c31ba-a383-40cc-8ad7-9a5fe2b6f0b9)

Now we move to the left tree and deal with the left subtree

In this case the left node connected to the key node is `2` and it has just one node which is the left node `1` so the list will then be `[3, 2, 1]`

Since we're done with the left tree of this node we'll move back to the key node
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cd7a5ea1-1525-4b4e-a01d-368f0e4c97f2)

Now we check for the right tree and the right node connected to the key node is `4` which also is the `current node`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dcee8fdd-c47f-48fa-9bc7-d588136ff50b)

The current node has two children which are the left and right children 

From the rule of preorder traversal after traversing the current node we should traverse the left subtree 

Since the current node has just one left node that means we've finished traversing the left subtree then we move to the right subtree which is the right node 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ff60b07c-6ac6-457a-a943-bc7f20185542)

So the final return value would be `[3, 2, 1, 4, 6, 5]`

In order to implement this using python I'll use the generic `TreeNode` Class then recursively call the `preorder` function which would return `([node.key] + preorder(node.left) + preorder(node.right)`

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Binary%20Tree%20Preorder%20Traversal/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e673a86-c8f6-490b-8776-15340241fcb9)

### Leetcode Submission Script

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        
        return ([root.val] + Solution.preorderTraversal(self, root.left) + Solution.preorderTraversal(self, root.right))
```
