import unittest
from BinaryTree import Node, inorder, create_example_tree
from InvertBinaryTree import invert_tree

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

        expected_inorder = [3, 1, 5, 2, 4]
        actual_inorder = []

        def inorder_traversal(node):
            if node:
                inorder_traversal(node.left)
                actual_inorder.append(node.val)
                inorder_traversal(node.right)

        inorder_traversal(inverted_root)
        self.assertEqual(actual_inorder, expected_inorder)

    def test_complete_binary_tree(self):
        root = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)))
        inverted_root = invert_tree(root)

        expected_inorder = [7, 3, 6, 1, 5, 2, 4]
        actual_inorder = []

        def inorder_traversal(node):
            if node:
                inorder_traversal(node.left)
                actual_inorder.append(node.val)
                inorder_traversal(node.right)

        inorder_traversal(inverted_root)
        self.assertEqual(actual_inorder, expected_inorder)

if __name__ == '__main__':
    unittest.main()
