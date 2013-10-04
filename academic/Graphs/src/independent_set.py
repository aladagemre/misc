import os,random,time
import itertools
from pygraphviz import AGraph

K=3

class CombinationCreator:
	def __init__(self):
		self.level1 = ["a","b","c"]
		self.level2 = ["x","y","z"]
		self.level3 = ["k","m","n"]
		
		self.combinations = []
		for item1 in self.level1:
			for item2 in self.level2:
				for item3 in self.level3:
					comb = Node( [item1, item2, item3], random.randint(0,100))
					self.combinations.append( comb )
		
class Node:
	"""Independent Set Node contains combination of items."""
	def __init__(self, items=None, weight=None):
		if not items:
			items = []
		if not weight:
			weight = 0.0
			
		self.items = set(items)
		self.weight = weight
		
		self.connections = set()
		
	def add_connection(self, target):
		self.connections.add(target)
	
	def __str__(self):
		return "%s (%f)" % ( "".join(self.items), self.weight )
		
	def __repr__(self):
		return self.__str__()
		
	def __cmp__(self, other):
		if self.items == other.items:
			return 0
		if self.weight < other.weight:
			return -1
		else:
			return 1
			
	def __hash__(self):
		return reduce(lambda x,y : x*y, map(hash, list(self.items)) + [int(self.weight*100)])
		
class SetGraph:
	"""Independent Set Graph"""
	def __init__(self, nodes = None, edges = None):
		if not nodes:
			nodes = []
		if not edges:
			edges = set()
			
		self.nodes = nodes	
		self.edges = edges
		
	def generate(self, nodes):
		"""Generates an independent set graph from given nodes.
		Adds edges to nodes with common items inside."""
		
		# do a better matching if possible
		self.nodes = nodes
		l = len(nodes)
		for i in range(l):
			for j in range(l):
				u = nodes[i]
				v = nodes[j]
				if i!=j and u.items.intersection(v.items):
					u.add_connection( v )
					v.add_connection( u )
					edge = tuple(sorted([u,v]))
					self.edges.add(edge)
					
					
	def render_image(self, filename):
		"""Renders the graph image locally using pygraphviz."""
		
		# Create a graph
		G=AGraph(directed=False) 
		# Add nodes
		for node in self.nodes:
			G.add_node(node)
		# Add edges
		for edge in self.edges:
			G.add_edge(edge[0], edge[1], color='blue')
		# Give layout and draw.
		G.layout('circo')
		G.draw(filename) # Save the image.
		
		# Display the output image.
		os.system("gwenview %s&" % filename)

class Chandra:
	def __init__(self, g):
		self.g = g # independent set graph
		
	def start_greedy(self):
		"""Performs greedy pickups. Starts from the heaviest node,
		removes its adjacent nodes and picks up the heaviest from the 
		remaining ones."""
		nodes = self.g.nodes[:]
		
		I = sorted(nodes, reverse=True)
		I_ = set()
		while I:
			heaviest = I.pop(0) # get the heaviest one.
			print "Picked up heaviest:", heaviest
			# Add heaviest to temporary I_.
			I_.add(heaviest)
			# Remove all neighbors of this heaviest node.
			for neighbor in heaviest.connections:
				if neighbor in I:
					I.remove(neighbor)
		
		# Now replace I with I_.
		self.I = I_
		
		# Draw the resulting graph.
		new_graph = SetGraph()
		new_graph.generate(list(I_))
		new_graph.render_image("output2.png")

	def is_independent_set(self, perm):
		"""Says if given permutation is independent or not.
		For example abc and bde are dependent as they both have b.
		abc def are independent as they dont share any items.
		
		for each subset element, union them one by one
		and observe if it doesnt grow more than K.
		if grows < K, it means one of its items was already in the union.
		so it's not an independent set. 
		
		"""
		cumulative_items = set() 
		for i in range(len(perm)):
			old_length = len(cumulative_items)
			cumulative_items.update(*perm[i].items)
			if len(cumulative_items) - old_length < K:
				# repeating, we have intersection so its not independent
				#print "dependent:", perm
				return False
		else:
			#print "independent:",perm
			return True
					
	def improve(self):
		"""Tries to perform local improvement."""
		I = list(self.I) # Remaining nodes graph (independent set graph)
		ratios = []  #holds the payoff improvement ratios.
		
		for node in I[:]:
			if node not in I: continue # if we deleted this node in previous steps, skip it.
			subsets = []
			for n in range(1, K+1):
				for perm in itertools.permutations(node.connections, n):
					# for each subset of length 1...K, see if it's independent.
					if self.is_independent_set(perm):
						# if independent, add to subsets list, we'll use it.
						subsets.append( perm )
						
			print "Subets that are independent:"
			for subset in subsets:
				print subset
			for Q in subsets:
				# Try to include all these subsets into the graph I.
				# Q is one of the subsets.
				# find weight of Q.
				w_q = 0.0
				neighbors = [] # holds total weight of its neighbors that are supposed to be removed from I.
				for newnode in Q:
					w_q += newnode.weight # add node weight
					neighbors.extend(newnode.connections) # add node's neighbors to neighbors list.
				# now calculate  total weight sum of neighbors of Q
				w_n = sum ( [ neighbor.weight for neighbor in set(neighbors) ] )
				
				payoff_improvement = w_q/w_n
				# save this ratio to a list to see all of them later.
				ratios.append(payoff_improvement)
				
				# if this replacement is beneficial, add Q, and remove N(Q)
				if w_q / w_n > 1: # if W(Q) / W(Neighbors of Q) > 1:
					# remove those adjacent to Q
					
					#print "Removing neighbors of %s" %,
					#for n in neighbors: print n,
					
					# now remove neighbors of Q who are in I.
					for node in neighbors:
						if node in I:
							I.remove(node)
					
					# add Q into I.
					print "Adding Q:",
					for n in Q: print n,
					print
					
					I.extend(Q)
					I = list(set(I))

		new_graph = SetGraph()
		new_graph.generate(I)
		new_graph.render_image("output3.png")
		
		
		# Now I want to see 10 highest payoff improvement ratios I could see ever.
		ratios.sort()
		print "Highest 10:", ratios[-10:]
		
		self.I = set(I)

def happiness(table):
	"""
	Find the happiness of the table
	- by calculating the maximum distance between the letters
	"""
	return abs(ord(table[0]) - ord(table[-1]))
	
def generate_graph():
	"""Generates a random graph using some combination tricks."""
	
	"""nodes = []
	for combination in itertools.combinations('abcdef', r=K):
		# Combination of abcdef of K letters.
		weight = random.randrange(100) #happiness(combination) # random.random()
		n = Node(combination, weight )		
		nodes.append(n)"""
	
	# ======== TO FASTEN THE PROCESS =========
	#random.shuffle(nodes)
	#nodes = nodes[:len(nodes)/2]
	# ======== TO USE EXTERNAL COMBINATIONS=========
	#tp = CombinationCreator()
	#nodes = tp.combinations
	
	#=========GENERATE GRAPH USING COMBINATIONS FOUND======
	
	n1 = Node(list("abc"), 99)
	n2 = Node(list("ade"), 98)
	n3 = Node(list("bfg"), 98)
	n4 = Node(list("chi"), 98)
	nodes=[n1,n2,n3,n4]
	g = SetGraph()
	g.generate(nodes)
	g.render_image("output.png")
	
	
	chandra = Chandra(g)
	chandra.start_greedy() # do greedy picking
	chandra.improve() # improve once.
	
if __name__ == "__main__":
	
	generate_graph()
	
	#import cProfile
	#cProfile.run('generate_graph()')
