from pygml.pygml import Graph, Node

class Dijkstra:
    def __init__(self, G, s):
        self.g = G
        self.s = s
        self.H = self.g.nodes[:]
        self.set_initial_values()
        self.find_shortest_path()
        
    def set_initial_values(self):
        for u in self.g.nodes:
            u.sp = float("inf")
        self.s.sp = 0
        self.s.prev = None
        self.sort()
        
    def sort(self):
        self.H.sort(key=lambda x:x.sp)
    
    def find_shortest_path(self):
        while self.H:
            v = self.H.pop(0)
            print "Popped",v.id
            for edge in v.outgoing_edges:
                w = edge.v # target
                if w not in self.H: continue
                if v.sp + edge.weight < w.sp:
                    print w.id,".sp was",w.sp
                    w.sp = v.sp + edge.weight
                    w.prev = v
                    print w.id,".sp is",w.sp
                    
            self.sort()

    def get_path(self, target):
        print "From %d on the way to %d" % (self.s.id+1, target.id+1)
        current = target
        while hasattr(current, 'prev'):
            print "Hopping: ", current.id+1
            current = current.prev
            
                    

if __name__ == "__main__":
    G = Graph()
    
    n1 = Node()
    n2 = Node()
    n3 = Node()
    n4 = Node()
    n5 = Node()

    map(G.add_node, (n1,n2,n3,n4,n5))
    n1.add_link_to(n2).weight = 2
    n1.add_link_to(n3).weight = 7
    n1.add_link_to(n4).weight = 1
    
    n2.add_link_to(n3).weight = 4
    n2.add_link_to(n4).weight = 5
    
    n4.add_link_to(n5).weight = 2
    n5.add_link_to(n3).weight = 3
    
    G.render_image("output.png")
    
    d = Dijkstra(G, n1)
    print G.nodes
    for node in G.nodes:
        print node.id+1, node.sp
    
    d.get_path(n3)