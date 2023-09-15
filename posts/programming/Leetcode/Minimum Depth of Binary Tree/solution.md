<h3> Minimum Depth of Binary Tree </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a5102e9-5123-4421-b14b-81638cbc7314)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bef6813c-b592-49c8-94d0-f13f341fa107)

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

```
Note: A leaf is a node with no children.
```

So let's take a sample binary tree to work on
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d219a417-8d99-4f4a-98bd-7f037533e844)

First we can maybe say let's take the approach we used for solving the [maximum depth](https://h4ckyou.github.io/posts/programming/Leetcode/Maximum%20Depth%20of%20Binary%20Tree/solve.html) which is depth- first search?

Let's get the traverse of the left subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1c77af27-2dcb-49dd-a269-f985eb08c5b6)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4e968688-9f93-4e8e-b004-d6d378e28265)

Now the traverse of the right subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ba0139d0-bd35-47e0-abf6-b8d51e77bc0c)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7dd8ccac-0b20-408f-9d93-66da906c5c02)

The minimum value would be our return value?
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1808af97-9134-4321-801f-cfdac9ea5b37)

We can also confirm that's the right value by getting the minimum between the left and right subtree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92147202-3a90-4594-92f1-a7e95c878613)

From the image above we can see the left subtree has just two nodes while the right has three nodes so the minimum between this two subtress is basically 2 

That would work (the script proposed) but not in the case for all binary trees

Let's say for example this binary tree
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ce5dc5b8-fd33-4007-bdeb-ef146b6645a8)

We can see that it only has right subtree and we can tell the minimum value is 4 because no comparison against the left subtree

Can you see why the script won't work?

Well there's no comparison to check if the `node.left == None` or `node.right == None` 

So we need to handle a case where there's no left subtree or right subtree

With that said here's my solve script is in the link below

Solve Script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Minimum%20Depth%20of%20Binary%20Tree/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e0b6339c-19f6-472f-85d8-85b31c1446e5)


#### Leetcode Submission Script

```python
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        if root.left is None:
            return 1 + self.minDepth(root.right)
        
        if root.right is None:
            return 1 + self.minDepth(root.left)
        
        left_dept = self.minDepth(root.left)
        right_dept = self.minDepth(root.right)

        return 1 + min(left_dept, right_dept)
```
