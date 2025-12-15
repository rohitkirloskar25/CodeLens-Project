import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class TestNode(unittest.TestCase):

    def test_node_creation(self):
        node = Node(1)
        self.assertEqual(node.data, 1)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

class TestInorderTraversal(unittest.TestCase):
    def test_inorder_traversal(self):
        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)

        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.data)
                inorder(node.right)
        inorder(root)
        self.assertEqual(result, [4, 2, 5, 1, 3])

if __name__ == '__main__':
    unittest.main()
