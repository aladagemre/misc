import os,random
import itertools

K=3

class CombinationCreator:
	def __init__(self):
		self.level1 = ["a","b"]
		self.level2 = ["x","y"]
		self.level3 = ["k","m"]
		
		self.combinations = []
		for item1 in self.level1:
			for item2 in self.level2:
				for item3 in self.level3:
					comb = Node( [item1, item2, item3], random.randint(0,100))
					self.combinations.append( comb )
		
class Node:
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
	def __init__(self, nodes = None, edges = None):
		if not nodes:
			nodes = []
		if not edges:
			edges = set()
			
		self.nodes = nodes	
		self.edges = edges
		
	def generate(self, nodes):
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
		# Generate the graph
		from pygraphviz import AGraph
		G=AGraph(directed=False)    # Create a graph
		for node in self.nodes:
			G.add_node(node)
		for edge in self.edges:
			G.add_edge(edge[0], edge[1], color='blue')
			#print "Adding %s %s" % (edge[0], edge[1])
		G.layout('circo')                         # Set hierarchical layout
		#print G.string()
		G.draw(filename)                        # Save the image.
		os.system("gwenview %s&" % filename)

class Chandra:
	def __init__(self, g):
		self.g = g # independent set graph
		
	def start_greedy(self):
		nodes = self.g.nodes[:]
		
		I = sorted(nodes, reverse=True)
		I_ = set()
		while I:
			heaviest = I.pop(0) # get the heaviest one.
			print "Picked up heaviest:", heaviest
			I_.add(heaviest)
			for neighbor in heaviest.connections:
				if neighbor in I:
					#print "Removing", neighbor
					I.remove(neighbor)
			#print "Remaining:"
			#for node in I:
				#print node
		self.I = I_
		new_graph = SetGraph()
		new_graph.generate(list(I_))
		new_graph.render_image("output2.png")

	def is_independent_set(self, perm):
		cumulative_items = set() 
		for i in range(len(perm)):
			old_length = len(cumulative_items)
			cumulative_items.update(*perm[i].items)
			if len(cumulative_items) - old_length < K:
				# repeating, we have intersection so its not independent
				#print "dependent:", perm
				return False
		else:
			print "independent:",perm
			return True
					
	def improve(self):
		I = list(self.I)
		ratios = [] 
		
		for node in I[:]:
			subsets = []
			for n in range(1, len(node.connections) + 1):
				for perm in itertools.permutations(node.connections, n):
					# for each subset element, union them one by one
					# and observe if it doesnt grow more than K.
					# if grows < K, it means one of its items was already in the union.
					# so it's not an independent set. break and move to another subset.
					
					if self.is_independent_set(perm):
						subsets.append( perm )
						
			print "Subets:"
			for subset in subsets:
				print subset
			for Q in subsets:
				"""print "Q:",
				for n in Q:
					print n,
				print"""
				w_q = 0.0
				neighbors = []
				for node in Q:
					w_q += node.weight
					neighbors.extend(node.connections) # add node's neighbors to neighbors list.
				w_n = sum ( [ node.weight for node in set(neighbors) ] )
				ratios.append(w_q/w_n)
				if w_q / w_n > 1: # if W(Q) / W(Neighbors of Q) > 1:
					# remove those adjacent to Q
					#print "Removing neighbors of %s" %,
					#for n in neighbors: print n,
					print "Adding Q:",
					for n in Q: print n,
					print
					for node in neighbors:
						if node in I:
							I.remove(node)
					# add Q
					I.extend(Q)
					I = list(set(I))
					print I
		new_graph = SetGraph()
		new_graph.generate(I)
		new_graph.render_image("output3.png")
		ratios.sort()
		print "Biggest 10:", ratios[-10:]
		self.I = set(I)

def happiness(table):
	"""
	Find the happiness of the table
	- by calculating the maximum distance between the letters
	"""
	return abs(ord(table[0]) - ord(table[-1]))
	
def generate_graph():
	"""nodes = []
	for combination in itertools.combinations('abcdefg', r=K):
		#weight = sum( [ord(l) for l in combination] ) / 495.0
		weight = random.randrange(100) #happiness(combination) # random.random()
		n = Node(combination, weight )		
		nodes.append(n)
	random.shuffle(nodes)
	nodes = nodes[:len(nodes)/2]"""
	
	tp = CombinationCreator()
	nodes = tp.combinations
	
	g = SetGraph()
	g.generate(nodes)
	g.render_image("output.png")
	
	
	chandra = Chandra(g)
	chandra.start_greedy()
	chandra.improve()
	
if __name__ == "__main__":
	
	
	import cProfile
	cProfile.run('generate_graph()')
