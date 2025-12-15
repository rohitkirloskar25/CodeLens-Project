import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def inorder(node):
    if node:
        inorder(node.left)
        print(node.data, end=" ")
        inorder(node.right)

def create_example_tree():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)

    root.left.left = Node(4)
    root.left.right = Node(5)
    
    return root

class TestBinaryTree(unittest.TestCase):

    def test_node_creation(self):
        node = Node(10)
        self.assertEqual(node.data, 10)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_create_example_tree(self):
        root = create_example_tree()
        self.assertEqual(root.data, 1)
        self.assertEqual(root.left.data, 2)
        self.assertEqual(root.right.data, 3)
        self.assertEqual(root.left.left.data, 4)
        self.assertEqual(root.left.right.data, 5)
        self.assertIsNone(root.right.left)
        self.assertIsNone(root.right.right)

if __name__ == '__main__':
    unittest.main()
