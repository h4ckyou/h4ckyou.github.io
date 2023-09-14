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

    def remove_none(nums):
        return [x for x in nums if x is not None]

    def inorderTraverse(self):
        if self is None:
            return []

        return TreeNode.remove_none(TreeNode.inorderTraverse(self.left) + [self.key] + TreeNode.inorderTraverse(self.right))


data = ((None, None, None), 1, (3, 2, None))

node = TreeNode.parseTuple(data)
print(node.inorderTraverse())

