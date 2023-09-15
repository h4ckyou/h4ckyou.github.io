from collections import deque

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def parseTuple(data):
        if isinstance(data, tuple) and len(data) == 3:
            node = TreeNode(data[1])
            node.left = TreeNode.parseTuple(data[0])
            node.right = TreeNode.parseTuple(data[2])

        elif data is None:
            node = None

        else:
            node = TreeNode(data)

        return node

def levelOrder(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_values = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            level_values.append(node.key)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level_values)

    return result

data = (None, 2, (None, 3, (None, 4, (None, 5, 6))))

root = TreeNode.parseTuple(data)
print(levelOrder(root))
