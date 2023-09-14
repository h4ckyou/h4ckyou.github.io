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
    
    def maximumDepth(self):
        if self is None:
            return 0
        
        return 1 + max(TreeNode.maximumDepth(self.left), TreeNode.maximumDepth(self.right))


data = ((1, 2, None), 3, (6, 4, 5))

node = TreeNode.parseTuple(data)
print(node.maximumDepth())
