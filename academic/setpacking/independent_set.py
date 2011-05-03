import os,random

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
			print "Adding %s %s" % (edge[0], edge[1])
		G.layout('circo')                         # Set hierarchical layout
		#print G.string()
		G.draw(filename)                        # Save the image.
		os.system("gwenview %s&" % filename)

class Chandra:
	def __init__(self, g):
		self.g = g # independent set graph
		
	def start_greedy(self):
		nodes = self.g.nodes[:]
		print nodes
		I = sorted(nodes, reverse=True)
		I_ = set()
		while I:
			heaviest = I.pop(0) # get the heaviest one.
			print "Picked up heaviest:", heaviest
			I_.add(heaviest)
			for neighbor in heaviest.connections:
				if neighbor in I:
					print "Removing", neighbor
					I.remove(neighbor)
			#print "Remaining:"
			#for node in I:
				#print node
		print I_
		new_graph = SetGraph()
		new_graph.generate(list(I_))
		new_graph.render_image("output2.png")
		

def generate_graph():
	import itertools
	nodes = []
	for combination in itertools.combinations('abcde', r=2):
		#weight = sum( [ord(l) for l in combination] ) / 495.0
		weight = random.random()
		n = Node(combination, weight )		
		nodes.append(n)
		

	g = SetGraph()
	g.generate(nodes)
	g.render_image("output.png")
	
	
	chandra = Chandra(g)
	chandra.start_greedy()
	
if __name__ == "__main__":
	generate_graph()
