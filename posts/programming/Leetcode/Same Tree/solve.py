class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    
    def parsetuple(data):
        if isinstance(data, tuple) and len(data) == 3:
            node = TreeNode(data[1])
            node.left = TreeNode.parsetuple(data[0])
            node.right = TreeNode.parsetuple(data[2])

        elif data is None:
            node = None
        
        else:
            node = TreeNode(data)

        return node

    def isSameTree(p, q):
        if p is None and q is None:
            return True
        
        if p is None or q is None:
            return False
        
        return TreeNode.isSameTree(p.left, q.left) and TreeNode.isSameTree(p.right, q.right) and (p.key == q.key)

p = (1, 1, None)
q = (None, 1, 1)

p_node = TreeNode.parsetuple(p)
q_node = TreeNode.parsetuple(q)

r = TreeNode.isSameTree(p_node, q_node)
print(r)
