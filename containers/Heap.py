'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an
*explicit* vector implementation,
so the code in the book is likely to be less helpful than the code
for the other data structures.
The book's implementation is the traditional implementation
because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more
practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        if xs:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be
        used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have
        a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        if node is None:
            return True
        if node.left is None and node.right is None:
            return True
        elif not node.right and node.left:
            return node.value <= node.left.value
        elif node.value <= node.left.value and node.value <= node.right.value:
            return Heap._is_heap_satisfied(node.right) and Heap._is_heap_satisfied(node.left)
        else:
            return False

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation of the total number of nodes
            1. You will have to explicitly store the size of your heap in a variable (rather than compute it) to maintain the O(log n) runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap-using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert functions.
        '''
        if self.root:
            len_nodes = self.__len__()
            path = "{0:b}".format(len_nodes + 1)[1:]
            self.root = Heap.__insert(self.root, value, path)
        else:
            self.root = Node(value)

    @staticmethod
    def __insert(node, value, path):
        if path[0] == '0':
            if not node.left:
                node.left = Node(value)
            else:
                node.left = Heap.__insert(node.left, value, path[1:])
        if path[0] == '1':
            if not node.right:
                node.right = Node(value)
            else:
                node.right = Heap.__insert(node.right, value, path[1:])

        if path[0] == '0':
            if node.left.value < node.value:
                temp = node.value
                node.value = node.left.value
                node.left.value = temp
        if path[0] == '1':
            if node.right.value < node.value:
                temp = node.value
                node.value = node.right.value
                node.right.value = temp
        return node

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for i in xs:
            self.insert(i)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        return self.root.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made the most sense.
        '''
        if not self.root:
            pass
        elif self.root.left is None and self.root.right is None:
            self.root = None
        else:
            len_nodes = self.__len__()
            path_to_last = "{0:b}".format(len_nodes)[1:]
            deleted_val = Heap._delete_node(self.root, path_to_last)
            if self.root:
                self.root.value = deleted_val
            if not Heap._is_heap_satisfied(self.root):
                self.root = Heap._swap_root(self.root)

    @staticmethod
    def _delete_node(node, path):
        last_val = 0
        if len(path) == 0:
            return None
        if path[0] == '0':
            if len(path) > 1:
                last_val = Heap._delete_node(node.left, path[1:])
            else:
                last_val = node.left.value
                node.left = None

        if path[0] == '1':
            if len(path) > 1:
                last_val = Heap._delete_node(node.right, path[1:])
            else:
                last_val = node.right.value
                node.right = None
        return last_val

    @staticmethod
    def _swap_root(node):
        if not node.left and not node.right:
            return node
        if node.right and (not node.left or node.left.value >= node.right.value):
            if node.value > node.right.value:
                temp = node.right.value
                right = node.value
                node.value = temp
                node.right.value = right
            node.right = Heap._swap_root(node.right)
        elif node.left and (not node.right or node.left.value <= node.right.value):
            if node.value > node.left.value:
                temp = node.left.value
                left = node.value
                node.value = temp
                node.left.value = left
            node.left = Heap._swap_root(node.left)
        else:
            pass
        return node
