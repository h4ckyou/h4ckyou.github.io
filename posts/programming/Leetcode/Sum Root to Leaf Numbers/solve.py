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

    def root2leaf(self):
        def explore(node, current_path, result):
            if node is None:
                return

            current_path.append(node.key)

            if node.left is None and node.right is None:
                result.append(list(current_path))

            explore(node.left, current_path, result)
            explore(node.right, current_path, result)

            current_path.pop()

        result = []
        current_path = []
        explore(self, current_path, result)
        r = [int("".join(map(str, sublist))) for sublist in result]
        
        return sum(r)

data = ((5, 9, 1), 4, (None, 0, None))

node = TreeNode.parseTuple(data)

print(node.root2leaf())
