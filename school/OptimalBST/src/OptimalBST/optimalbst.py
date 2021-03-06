#-*-encoding:utf-8-*-
# AHMET EMRE ALADAG © 2010
# Implementation of Optimal BST in CLSR Algorithms Book with Python.

# A shortcut for inclusive range function: [x,y]
irange = lambda x,y,z=1: xrange(x,y+1,z)

class Node:
    """Tree node class."""
    def __init__(self, key):
        self.key = key
        self.custom_key = None
        
    def __repr__(self):
        #return "k%s - %s" % (self.key, self.custom_key)
        return "%s" % self.custom_key
class DummyNode:
    """Dummy node class, used as a substitute for searched items that do not exist."""
    def __init__(self, key):
        self.key = key
    def __repr__(self):
        return "d%s" % self.key
    
class OptimalBST:
    """<Cormen Leiserson Rivest Stein> Algorithms book Optimal BST implementation"""
    def __init__(self, p=None, q=None, n=None, custom_keys=None, filename=None):
        """
        p is the list of probabilities for each real key to be searched.
        q is the list of probabilities for key intervals that do not exist in the tree.
        n is the number of keys.
        custom_keys is the list of custom key names (can be any type, like str).
        """
        # Parameters to attributes
        self.n  = n
        self.p = p
        self.q = q
        self.custom_keys = custom_keys

        if filename:
            self.read_from_file(filename)

        # Storage
        self.__root = {}      # root[i,j] will hold the optimal root for the range (i,j).
        self.__e = {}         # e[i,j] will hold the expected search cost of subtree in range (i,j)
        self.__w = {}         # w[i,j] = P+Q sums in range (i,j)

        self.p.insert(0, 0)          # We will use index 1 as starting point for list p.
        if self.custom_keys:         # If we have custom keys, start them from the index 1.
            self.custom_keys.insert(0, None)


        """# OPERATIONS
        print "Finding the optimal roots"
        self.find_optimal()     # Calculate the search cost table.
        
        print "Constructing tree"
        self.construct_tree()   # Construct the tree according to the search cost table.
        print "Finished."
        """
            


    def find_optimal(self):
        """Finds the Optimal BST by minimizing the expected search cost.
        Uses dynamic programming."""
        # Shortcuts
        root = self.__root
        e = self.__e
        w = self.__w
        n = self.n
        q = self.q
        p = self.p
        
        for i in irange(1, n + 1):
            e[i, i-1] = q[i-1]
            w[i, i-1] = q[i-1]
        for l in irange(1, n):
            for i in irange(1, n - l + 1):
                j = i + l - 1
                e[i,j] = float("infinity")          # Set to infinity for "minimum" comparisons.
                w[i,j] = w[i, j-1] + p[j] + q[j]    # Set PSum table

                for r in irange(i, j):
                    t = e[i, r-1] + e[r+1, j] + w[i,j]
                    if t < e[i,j]:
                        e[i,j] = t
                        root[i,j] = r

        self.construct_tree()

    def __get_root(self, start, end):
        """Returns the optimal root calculated for the range (start,end)."""
        return self.__root[start, end]
    
    def __construct_subtree(self, start, end):
        """Constructs a subtree for the range (start,end) and returns
        the root of this subtree."""

        if end < start:
            # If boundaries pass each other, means no more search.
            return None
        
        root_index = self.__get_root(start, end)  # Get the optimal root key.
        node = Node(root_index)                 # Create the root node.
        if self.custom_keys:
            node.custom_key = self.custom_keys[root_index]

        # Assign left and right node by constructing 2 more subtrees.
        node.left = self.__construct_subtree(start, root_index - 1)
        node.right = self.__construct_subtree(root_index + 1, end)

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
        self.root_node = self.__construct_subtree(1, self.n)

    def get_node_by_index(self, key, root=None):
        """Returns the node with the given key. If can't find, returns the dummy node."""
        if not root:
            root = self.root_node

        # If we reach a dummy node, return it. No need to search anymore.
        # This is the one of the base cases.
        if isinstance(root, DummyNode):
            return root

        # If we reach the real node we look for, return it.
        # This is the second of the base cases.
        if root.key == key:
            return root

        # If the key we look for is smaller than the current node,
        # Look for the key in the left subtree
        elif key < root.key:
            return self.get_node_by_index(key, root.left)
        # If the key is greater, look in the right subtree.
        else:
            return self.get_node_by_index(key, root.right)
    def get_node_by_custom_key(self, custom_key, root=None):
        """Returns the node with the given custom key. If can't find, returns the dummy node."""
        if not root:
            root = self.root_node

        # If we reach a dummy node, return it. No need to search anymore.
        # This is the one of the base cases.
        if isinstance(root, DummyNode):
            return root

        # If we reach the real node we look for, return it.
        # This is the second of the base cases.
        if root.custom_key == custom_key:
            return root

        # If the key we look for is smaller than the current node,
        # Look for the key in the left subtree
        elif custom_key < root.custom_key:
            return self.get_node_by_custom_key(custom_key, root.left)
        # If the key is greater, look in the right subtree.
        else:
            return self.get_node_by_custom_key(custom_key, root.right)

    def __add_subtrees(self, node_list, edge_list, root):
        """Adds the subtrees of the given root node to the graph G."""
        if isinstance(root, DummyNode):         # If dummy, do nothing.
            return
        node_list.append(root.left.__repr__())                   # Add left child
        node_list.append(root.right.__repr__())                  # Add right child

        edge_list.append( (root.__repr__(), root.left.__repr__()) )           # Add edge to left child
        edge_list.append( (root.__repr__(), root.right.__repr__()) )          # Add edge to right child

        self.__add_subtrees(node_list, edge_list, root.left)       # Add left subtree
        self.__add_subtrees(node_list, edge_list, root.right)      # Add right subtree

    def __generate_image(self):
        """Generates node and edge lists to prepare materials for graph construction."""
        root = self.root_node                   # Use root as shortcut
        node_list = [ root.__repr__() ]                    # Add the root to graph
        edge_list = [ ]
        #G.add_node(root)

        # Add the subtrees of root
        self.__add_subtrees(node_list, edge_list, root)

        return node_list, edge_list
        
    def render_local(self, filename):
        """Renders the OBST image locally using pygraphviz."""
        # Get the graph information
        node_list, edge_list = self.__generate_image()
        # Generate the graph
        from pygraphviz import AGraph
        G=AGraph(strict=True,directed=True)    # Create a graph
        for node in node_list:
            G.add_node(node)
        for edge in edge_list:
            G.add_edge(edge[0], edge[1])        
        G.layout('dot')                         # Set hierarchical layout
        G.draw(filename)                        # Save the image.

    def render_online(self, filename):
        """Renders the OBST image locally using RPC."""
        # Get the graph information
        node_list, edge_list = self.__generate_image()
        print node_list, edge_list
        # Call RPC
        import xmlrpclib
        port = 1000 - 2
        proxy = xmlrpclib.ServerProxy("http://www.remziduzagac.com:" + str(port))
        with open(filename, "wb") as handle:
            handle.write(proxy.render_image(node_list, edge_list).data)

    
    def read_from_file(self, filename):
        """Reads the probabilities and keynames from a file."""
        f = open(filename)
        self.q = []
        self.p = []
        self.custom_keys = []
        first_q = float(f.readline().strip())
        self.q.append(first_q)
        for line in f:
            q, p, ck = line.strip().split("\t")
            self.q.append(float(q))
            self.p.append(float(p))
            self.custom_keys.append(ck)
        self.n = len(self.p)
        f.close()
            
if __name__ == "__main__":
    """tree = OptimalBST(
        p=[0.15,0.10,0.05,0.10,0.20],
        q=[0.05,0.10,0.05,0.05,0.05,0.10],
        n=5,
        custom_keys=["Ahmet", "Caner", "Emre","Volkan","Zeynep"])"""

    tree = OptimalBST(None, None, None, None, filename="input.txt")
    tree.find_optimal()
    tree.construct_tree()

    for i in range(5):
        print "Looking for Key %d: %s" %( i,  tree.get_node_by_index(i) )

    for ck in ["Alen", "Ahmet", "Caner","Cemil", "Emre","Mehmet","Volkan","Zeynep", "Züleyha"]:
        print "Looking for %s: %s" %( ck,  tree.get_node_by_custom_key(ck) )

    #tree.render_online("online.png")
    tree.render_local("offline.png")