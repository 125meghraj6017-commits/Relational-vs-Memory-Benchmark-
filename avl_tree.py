from data_generator  import generate_data

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    # Get height of a node
    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    # Get balance factor
    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotation
    def right_rotate(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        y.height = 1 + max(
            self.get_height(y.left),
            self.get_height(y.right)
        )

        x.height = 1 + max(
            self.get_height(x.left),
            self.get_height(x.right)
        )

        return x

    # Left rotation
    def left_rotate(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        x.height = 1 + max(
            self.get_height(x.left),
            self.get_height(x.right)
        )

        y.height = 1 + max(
            self.get_height(y.left),
            self.get_height(y.right)
        )

        return y

    # Insert a key
    def insert(self, node, key):

        # Normal BST insertion
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)

        elif key > node.key:
            node.right = self.insert(node.right, key)

        else:
            # Ignore duplicate values
            return node

        # Update height
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )

        # Calculate balance
        balance = self.get_balance(node)

        # Left Left case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Search for a key
    def search(self, node, key):

        if node is None:
            return False

        if key == node.key:
            return True

        if key < node.key:
            return self.search(node.left, key)

        return self.search(node.right, key)


if __name__ == "__main__":

    tree = AVLTree()

    # Generate test data
    data = generate_data(1000)

    # Insert generated data into AVL Tree
    for value in data:
        tree.root = tree.insert(tree.root, value)

    print("AVL Tree Module")
    print("----------------")
    print("Records inserted:", len(data))

    # Test search
    search_key = data[0]

    print("Search key:", search_key)
    print("Search result:", tree.search(tree.root, search_key))

    print("AVL Tree working successfully.")