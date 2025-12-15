# Import the Node class, the inorder traversal function, 
# and the tree creation function from the local file
from BinaryTree import Node, inorder, create_example_tree

def invert_tree(root: Node) -> Node:
    """
    Recursively inverts a binary tree by swapping the left and right children
    of every node.
    """
    # Base Case: If the current node is None, return it
    if root is None:
        return None

    # Recursive Step:
    # 1. Recursively invert the left and right subtrees
    left = invert_tree(root.left)
    right = invert_tree(root.right)

    # 2. Swap the left and right pointers of the current node
    root.left = right
    root.right = left

    # 3. Return the current node (which is now the root of the inverted subtree)
    return root
# 

# --- Execution ---

# 1. Create the initial tree
original_root = create_example_tree()

print("--- Initial Tree (Inorder Traversal) ---")
# Expected output: 4 2 5 1 3
inorder(original_root)
print("\n")


# 2. Invert the tree
inverted_root = invert_tree(original_root)


print("--- Inverted Tree (Inorder Traversal) ---")
# Expected output: 3 1 5 2 4
# The new structure is: 1(3, 2(5, 4))
inorder(inverted_root)
print("\n")

print("Inversion complete.")
