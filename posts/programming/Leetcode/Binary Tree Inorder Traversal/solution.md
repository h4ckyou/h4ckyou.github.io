<h3> Binary Tree Inorder Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6efa44dd-4e85-4c8a-a914-c537f5ce77a2)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6d31e7a-29f8-4bca-b79e-58b66dc501b5)

We are going to be given a binary tree and our goal is to return the inorder traversal of its nodes' values

First let's know what `Traversing` means:

Traversing refers to the process of visiting each node of a tree exactly once. Visiting a node generally refers to adding the node's key to a list.

There are various ways to traverse a binary tree and return the list of visited keys

In this case I'll deal with the `Inorder Traversal` method:

- Traverse the left subtree recursively inorder
- Traverse the current node
- Traverse the right subtree recursively inorder

That does not sound too good so let's take a sample

Consider this `binary tree` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/840f2369-e11a-4fb1-8af9-93b55189566c)

The key node is `3` which has two children `2 and 4` and the left and right nodes has other children

Let's take an example on what Inorder Traversal means:

First we'll start from the left node `2` of the key `3` and visit the left subtree first
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6d5ca74c-4848-4877-b47a-d651d2364220)

Now we check if the left node has another left key value, in this case it does i.e the node `2` has another left node `1`

We check again but in this case the node `1` does not have another node connected to it so we add that to our list and move to the current node `2` then check if it has any right subtree in this case it doesn't

Now we move up the from the current node to the key node
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa07c62e-1bdc-4502-b07e-4eba7408b90e)

At this point the value's we've covered are `[1, 2, 3]`

Now since our current node is `3` we'll move to the right node of the key node

We will then see that the right node has a left key value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6246b820-9428-4ce8-abab-4c78d6de77f3)

The key value `6` does not hold any other nodes so we'll add that to our list then move on to the current node `4`, the current node value will be added to the list also 

Since we are the current node we then check the right subtree which in this case is the remaining node which is `5`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58718ed4-c3a5-40dd-8333-81dea0c08db9)

At this point we've traversed the whole tree and the return value would be:

```
value = [1, 2, 3, 4, 6, 5]
```

Now to implement this is python we can create a class object that would be used to implement a binary tree i.e

```python
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
```

The remaining portion which is to implement the Inorder Traversal is going to be a recursive call to it's inorder function returning `(inorder(node.left) + [node.key] + inorder(node.right))`

```
Note: Generally Binary Tree or Binary Search Tree deals with lots of Recursion and Classes as it's trivial
```

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Binary%20Tree%20Inorder%20Traversal/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b640348-b755-48b2-ab36-a7cdf530f0c0)

#### Leetcode Submission Solution

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        
        return (Solution.inorderTraversal(self, root.left) + [root.val] + Solution.inorderTraversal(self, root.right))
```
