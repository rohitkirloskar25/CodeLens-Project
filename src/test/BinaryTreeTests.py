import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTreeTest(unittest.TestCase):

    def test_node_creation(self):
        node = Node(10)
        self.assertEqual(node.data, 10)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_tree_structure(self):
        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)

        self.assertEqual(root.data, 1)
        self.assertEqual(root.left.data, 2)
        self.assertEqual(root.right.data, 3)
        self.assertEqual(root.left.left.data, 4)
        self.assertEqual(root.left.right.data, 5)

if __name__ == '__main__':
    unittest.main()
