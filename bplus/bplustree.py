from __future__ import annotations
from math import ceil, floor


class Node:
    uid_counter = 0
    """
    Base node object.

    Attributes:
        order (int): The maximum number of keys each node can hold. (aka branching factor)
    """

    def __init__(self, order):
        self.order = order
        self.parent: Node = None
        self.keys = []
        self.values = []

        #  This is for Debugging purposes only!
        Node.uid_counter += 1
        self.uid = self.uid_counter

    def split(self) -> Node:  # Split a full Node to two new ones.
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order // 2)

        left.parent = right.parent = self

        left.keys = self.keys[:mid]
        left.values = self.values[:mid+1]

        right.keys = self.keys[mid+1:]
        right.values = self.values[mid+1:]

        self.values = [left, right]  # Setup the pointers to child nodes.

        # Hold the first element from the right subtree.
        self.keys = [self.keys[mid]]

        # Setup correct parent for each child node.
        for child in left.values:
            if isinstance(child, Node):
                child.parent = left

        for child in right.values:
            if isinstance(child, Node):
                child.parent = right

        return self  # Return the 'top node'

    def get_size(self) -> int:
        return len(self.keys)

    def is_empty(self) -> bool:
        return len(self.keys) == 0

    def is_full(self) -> bool:
        return len(self.keys) == self.order - 1

    # Used to check on keys, not data!
    def is_nearly_underflowed(self) -> bool:
        return len(self.keys) <= floor(self.order / 2)

    def is_underflowed(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2) - 1

    def is_root(self) -> bool:
        return self.parent is None


class LeafNode(Node):

    def __init__(self, order):
        super().__init__(order)

        self.prev_leaf: LeafNode = None
        self.next_leaf: LeafNode = None

    def add(self, key, value):  # TODO: Implement improved version
        if not self.keys:  # Insert key if it doesn't exist
            self.keys.append(key)
            self.values.append([value])
            return

        # Otherwise, search key and append value.
        for i, item in enumerate(self.keys):
            if key == item:  # Key found => Append Value
                # Remember, this is a list of data. Not nodes!
                self.values[i].append(value)
                # self.keys = self.keys[:i] + [key] + self.keys[i:]
                # self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            if key < item:  # Key not found && key < item => Add key before item.
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # Key not found here. Append it after.
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self) -> Node:  # Split a full leaf node. (Different method used than before!)
        top = Node(self.order)
        right = LeafNode(self.order)
        mid = int(self.order // 2)

        self.parent = right.parent = top

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        right.prev_leaf = self
        right.next_leaf = self.next_leaf

        top.keys = [right.keys[0]]
        top.values = [self, right]  # Setup the pointers to child nodes.

        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        self.next_leaf = right  # Setup pointer to next leaf

        return top  # Return the 'top node'


class BPlusTree(object):
    def __init__(self, order=5):
        # First node must be leaf (to store data).
        self.root: Node = LeafNode(order)
        self.order: int = order

    @staticmethod
    def _find(node: Node, key, basic=True):
        print('find from keys:', node.keys)
        for i, item in enumerate(node.keys):
            if key == item:
                if basic:
                    return node.values[i], i
                else:
                    return node.values[i+1], i + 1
            if key <= item:

                return node.values[i], i
            elif i + 1 == len(node.keys):
                # return right-most node/pointer.
                return node.values[i + 1], i + 1

    @staticmethod
    def _merge_up(parent: Node, child: Node, index):
        parent.values.pop(index)
        pivot = child.keys[0]

        print('pivot value: ', pivot)
        print('child left value: ', child.values[0].values)
        for c in child.values:
            if isinstance(c, Node):
                c.parent = parent

        for i, item in enumerate(parent.keys):
            # if pivot <= item:
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + \
                    child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value=None):
        node = self.root

        # While we are in internal nodes... search for leafs.
        while not isinstance(node, LeafNode):
            node, index = self._find(node, key)

        # Node is now guaranteed a LeafNode!
        node.add(key, value)

        while len(node.keys) == node.order:  # 1 over full
            print(node.keys)
            if not node.is_root():
                parent = node.parent
                print("parent keys", parent.keys)
                node = node.split()  # Split & Set node as the 'top' node.
                print("parent right value", parent.values[1].values)
                jnk, index = self._find(parent, node.keys[0], False)
                print("jnk: ", jnk.values)
                print('index: ', index)
                self._merge_up(parent, node, index)
                print("parent keys", parent.keys)
                node = parent
            else:
                node = node.split()  # Split & Set node as the 'top' node.
                # Re-assign (first split must change the root!)
                self.root = node

    def retrieve(self, key):
        node = self.root

        while not isinstance(node, LeafNode):
            node, index = self._find(node, key)

        for i, item in enumerate(node.keys):
            if key == item:
                return node.values[i]

        return None

    def show_bfs(self):
        if self.root.is_empty():
            print('The B+ Tree is empty!')
            return
        queue = [self.root, 0]  # Node, Height... Scrappy but it works

        while len(queue) > 0:
            node = queue.pop(0)
            height = queue.pop(0)

            if not isinstance(node, LeafNode):
                queue += self.intersperse(node.values, height+1)
            print(height, '|'.join(map(str, node.keys)), '\t', node.uid,
                  '\t parent -> ', node.parent.uid if node.parent else None)

    def get_leftmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[0]

        return node

    def get_rightmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[-1]

    def show_all_data(self):
        node = self.get_leftmost_leaf()
        if not node:
            return None

        while node:
            for node_data in node.values:
                print('[{}]'.format(', '.join(map(str, node_data))), end=' -> ')

            node = node.next_leaf
        print('Last node')

    def show_all_data_reverse(self):
        node = self.get_rightmost_leaf()
        if not node:
            return None

        while node:
            for node_data in reversed(node.values):
                print('[{}]'.format(', '.join(map(str, node_data))), end=' <- ')

            node = node.prev_leaf
        print()

    @staticmethod
    def intersperse(lst, item):
        result = [item] * (len(lst) * 2)
        result[0::2] = lst
        return result


if __name__ == '__main__':
    print('Initializing B+ tree...')
    bplustree = BPlusTree(order=5)

    bplustree.insert(13)
    bplustree.insert(0)
    bplustree.insert(7)
    bplustree.insert(8)
    bplustree.insert(5)
    bplustree.insert(6)
    bplustree.insert(4)
    bplustree.insert(1)
    bplustree.insert(2)
    bplustree.insert(3)
    bplustree.insert(9)
    bplustree.insert(2)
    bplustree.insert(10)
    bplustree.insert(11)
    bplustree.insert(12)
    bplustree.insert(17)
    bplustree.insert(14)
    bplustree.insert(15)
    bplustree.insert(16)

    bplustree.show_bfs()
    bplustree.show_all_data()
