#-*-encoding:utf-8-*-
# AHMET EMRE ALADAG © 2010
# Implementation of Optimal BST in CLSR Algorithms Book with Python.

irange = lambda x,y,z=1: xrange(x,y+1,z)

class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        
    def __repr__(self):
        return "k%s" % self.key # < %s, %s >" % (self.key, self.left, self.right)

class DummyNode:
    def __init__(self, key):
        self.key = key
    def __repr__(self):
        return "d%s" % self.key
    
class OptimalBST:
    """<Cormen Leiserson Rivest Stein> Algorithms book Optimal BST implementation"""
    def __init__(self, p, q, n):
        """
        p is the list of probabilities for each real key to be searched.
        q is the list of probabilities for key intervals that do not exist in the tree.
        n is the number of keys.
        """
        # Parameters to attributes
        self.n  = n
        self.p = p
        self.q = q

        # Storage
        self.root = {}      # root[i,j] will hold the optimal root for the range (i,j).
        self.e = {}         # e[i,j] will hold the expected search cost of subtree in range (i,j)
        self.w = {}         # w[i,j] = P+Q sums in range (i,j)

        p.insert(0, 0)      # We will use index 1 as starting point for list p.

        # OPERATIONS
        self.find_optimal()
        self.construct_tree()
        
    def find_optimal(self):
        """Finds the Optimal BST by minimizing the expected search cost.
        Uses dynamic programming."""
        # Shortcuts
        root = self.root
        e = self.e
        w = self.w        
        
        for i in irange(1, n + 1):
            e[i, i-1] = q[i-1]
            w[i, i-1] = q[i-1]
        for l in irange(1, n):
            for i in irange(1, n - l + 1):
                j = i + l - 1
                e[i,j] = float("inf")
                w[i,j] = w[i, j-1] + p[j] + q[j]

                for r in irange(i, j):
                    t = e[i, r-1] + e[r+1, j] + w[i,j]
                    if t < e[i,j]:
                        e[i,j] = t
                        root[i,j] = r

        self.construct_tree()

    def get_root(self, start, end):
        """Returns the optimal root calculated for the range (start,end)."""
        return self.root[start, end]
    
    def construct_subtree(self, start, end):
        """Constructs a subtree for the range (start,end) and returns
        the root of this subtree."""

        if end < start:
            # If boundaries pass each other, means no more search.
            return None
        
        root_index = self.get_root(start, end)  # Get the optimal root key.
        node = Node(root_index)                 # Create the root node.

        # Assign left and right node by constructing 2 more subtrees.
        node.left = self.construct_subtree(start, root_index - 1)
        node.right = self.construct_subtree(root_index + 1, end)

        # If no child exists, put a dummy node there.
        if node.left == None:
            node.left = DummyNode(root_index-1)
        if node.right == None:
            node.right = DummyNode(root_index)

        #print "%s - < %s , %s >" % (node, node.left, node.right)

        # Return the root of this subtree.
        return node

    def construct_tree(self):
        """Constructs the Optimal BST. Starts with the rood node (which is recursive)."""
        self.root_node = self.construct_subtree(1, self.n)
        
        
if __name__ == "__main__":
    tree = OptimalBST(p=[0.15,0.10,0.05,0.10,0.20], q=[0.05,0.10,0.05,0.05,0.05,0.10], n=5)