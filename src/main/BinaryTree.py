class Node:
    """Represents a node in the binary tree."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Simple traversal (inorder)
def inorder(node):
    """Performs an in-order traversal of the tree."""
    if node:
        inorder(node.left)
        print(node.data, end=" ")
        inorder(node.right)

# Function to create the example tree structure
def create_example_tree():
    """Creates the specific tree: 1(2(4,5), 3)"""
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)

    root.left.left = Node(4)
    root.left.right = Node(5)
    
    return root
