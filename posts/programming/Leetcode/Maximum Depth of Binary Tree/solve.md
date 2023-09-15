<h3> Maximum Depth of Binary Tree </h3> 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c524bedd-fc53-42e5-90cc-cf7b6bf04516)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df15a679-9d2b-4561-88da-1bc331d78d2d)

We will be given a binary tree and we're to return the maximum depth

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Let's take an example on what that means:

First for each subtree in the tree it corresponds to a level
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b23d03d1-a69f-4255-9622-07e9439b2e92)

That last level is known as the maximum depth of a binary tree

Now how do we calculate that?

Well if we know the level on the left subtree and the level on the right subtree we can calculate the maximum value of it

Because there might be case where the level of the left subtree might be lower than the right subtree and vice versa

The level of the subtree is also the length of number of elements there

Let's take this sample with `ipython`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dfc5747f-b801-44c2-be08-510435411f0f)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0a7d4c7-f949-42a7-9cb7-645677924f0c)

You can see that when I traverse the left subtree the length of the result is equivalent to it's level
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/195fbbb3-0d47-49fc-9b1b-db173d9a5acd)

I can also do that for the right subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ec72db7f-fa4e-4ab7-a932-a97da4883293)

Now the maximum depth would then be the maximum value between the length returned after traversing the left subarray and the length returned after traversing the right subarray

With recursion we can easily achieve this and what we'll check will be `max(node.left, node.right) + 1`

I'm checking the maximum value from traversing the left and array subtree then the result I'll increment it by 1

That's because when I do that it would actually start from the node of the parent tree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a9536431-a33b-4dcb-a60d-c271612bbb16)

With that said my solve script is in the link below 

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
