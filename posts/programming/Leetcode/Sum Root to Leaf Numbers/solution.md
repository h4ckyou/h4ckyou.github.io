<h3> Sum Root to Leaf Numbers </h3>

You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

    For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.

Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

A leaf node is a node with no children.

Let's take an example

Consider this binary tree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8adaa0fe-c216-4d3b-9b6f-4522cd2056df)

So our goal is to get the sum of all the root-->leaf nodes

A leaf is a node that doesn't have children

From the binary tree the leaf there are `5, 1 and 0`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92e59866-4996-4113-875e-818e78d8ab8a)

Now the aim is that we need to find the value from the root node to the leaf and get their sum

The path from the root node to the leaf would be considered as an integer

Let's look at what that means
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9715e9da-e452-43b2-9171-844600540821)

We can see from the above image that the node `0` is connected to the root node and since that appears to be a leaf the path would be:

```
4->0 = 40
```

That's what we are to find

Then let's look at the left subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6be42993-7e4c-4f3b-8d85-12263134d228)

At this point the whole `root-to-leaf` path are 

```
4->9->5 = 495
4->9->1 = 491
```

Then we take the sum of all `root-to-leaf` path:

```
sum = 495 + 491 + 40
sum = 1026
```

To solve this I used Depth-First Search algorithm 

Here's what my script does:

- The `root2leaf` method correctly initializes an empty list result to store the root-to-leaf paths and an empty list current_path to keep track of the current path as we traverse the tree.
- Inside the root2leaf method, we call a helper function `explore` that performs a depth-first traversal of the tree, keeping track of the current path and adding it to the result when a leaf node is reached.
- The `explore` function appends the current node's key to the path, checks if it's a leaf node, explores the left and right subtrees, and backtracks by removing the current node from the path when necessary.
- I convert the whole sublist in the result array to a single integer and return the sum of it.

Here's my solve script: [link]()
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/76670101-1f14-4042-8b15-9460b137f11a)

It's really optimized xD

#### Leetcode Submission Script

```python
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def explore(node, current_path, result):
            if node is None:
                return
            
            current_path.append(node.val)

            if node.left is None and node.right is None:
                result.append(list(current_path))
            
            explore(node.left, current_path, result)
            explore(node.right, current_path, result)
            
            current_path.pop()

        result = []
        current_path = []
        explore(root, current_path, result)
        r = [int("".join(map(str, sublist))) for sublist in result]

        return sum(r)
```

