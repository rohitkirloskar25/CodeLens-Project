import unittest
from BinaryTree import Node, inorder, create_example_tree
from invert_binary_tree import invert_tree

class TestInvertBinaryTree(unittest.TestCase):

    def test_empty_tree(self):
        root = None
        inverted_root = invert_tree(root)
        self.assertIsNone(inverted_root)

    def test_single_node_tree(self):
        root = Node(1)
        inverted_root = invert_tree(root)
        self.assertEqual(inverted_root.val, 1)
        self.assertIsNone(inverted_root.left)
        self.assertIsNone(inverted_root.right)

    def test_example_tree(self):
        root = create_example_tree()
        inverted_root = invert_tree(root)

        self.assertEqual(inverted_root.val, 1)
        self.assertEqual(inverted_root.left.val, 3)
        self.assertEqual(inverted_root.right.val, 2)
        self.assertEqual(inverted_root.right.left.val, 5)
        self.assertEqual(inverted_root.right.right.val, 4)

    def test_already_inverted_tree(self):
        root = Node(1, Node(3), Node(2, Node(5), Node(4)))
        inverted_root = invert_tree(root)

        self.assertEqual(inverted_root.val, 1)
        self.assertEqual(inverted_root.left.val, 2)
        self.assertEqual(inverted_root.right.val, 3)
        self.assertEqual(inverted_root.left.left.val, 4)
        self.assertEqual(inverted_root.left.right.val, 5)

    def test_complete_binary_tree(self):
        root = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)))
        inverted_root = invert_tree(root)

        self.assertEqual(inverted_root.val, 1)
        self.assertEqual(inverted_root.left.val, 3)
        self.assertEqual(inverted_root.right.val, 2)
        self.assertEqual(inverted_root.left.left.val, 7)
        self.assertEqual(inverted_root.left.right.val, 6)
        self.assertEqual(inverted_root.right.left.val, 5)
        self.assertEqual(inverted_root.right.right.val, 4)

if __name__ == '__main__':
    unittest.main()
