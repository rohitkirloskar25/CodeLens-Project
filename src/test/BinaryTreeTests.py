import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTreeTraversalTest(unittest.TestCase):

    def setUp(self):
        self.root = Node(1)
        self.root.left = Node(2)
        self.root.right = Node(3)
        self.root.left.left = Node(4)
        self.root.left.right = Node(5)

    def test_inorder_traversal(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.data)
                inorder(node.right)
        inorder(self.root)
        self.assertEqual(result, [4, 2, 5, 1, 3])

    def test_empty_tree(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.data)
                inorder(node.right)
        inorder(None)
        self.assertEqual(result, [])

    def test_single_node_tree(self):
        root = Node(10)
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.data)
                inorder(node.right)
        inorder(root)
        self.assertEqual(result, [10])

if __name__ == '__main__':
    unittest.main()
