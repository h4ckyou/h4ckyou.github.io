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

    def minimumDepth(self):
        if self is None:
            return 0

        if self.left is None and self.right is None:
            return 1

        if self.left is None:
            return 1 + TreeNode.minimumDepth(self.right)

        if self.right is None:
            return 1 + TreeNode.minimumDepth(self.left)

        left_depth = TreeNode.minimumDepth(self.left)
        right_depth = TreeNode.minimumDepth(self.right)

        return 1 + min(left_depth, right_depth)


data = ((None, 9, None), 3, (15, 20, 7))

node = TreeNode.parseTuple(data)
print(node.minimumDepth())
