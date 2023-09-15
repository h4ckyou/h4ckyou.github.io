<h3> Binary Tree Level Order Traversal </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4b6dcf60-ce50-4ad7-a276-55aa8eedb2ed)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/55bcd670-5959-4d84-b6a6-ec8a951f9bbc)

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

To solve this we can use a breadth-first search (BFS) approach to traverse the binary tree level by level

One each level of our traverse we use a queue to keep track of nodes. While the queue is not empty, we process nodes at each level and add their values to the level_values list.

After processing all nodes at the current level, we append `level_values` to the result list.

Here's more to it [link](https://www.geeksforgeeks.org/level-order-tree-traversal/?ref=lbp)

Here's the solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Binary%20Tree%20Level%20Order%20Traversal/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58cfec4e-1784-4105-81cc-d8758a09f0d1)


#### Leetcode Submission Script

```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_values = []
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                level_values.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_values)

        return result

```
