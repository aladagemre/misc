from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
from os.path import exists
from time import time

def render_image(node_list, edge_list):
        # Generate the graph
        from pygraphviz import AGraph
        G=AGraph(strict=False,directed=True)    # Create a graph
        for node in node_list:
            G.add_node(node)
        for edge in edge_list:
            G.add_edge(edge[0], edge[1])
        G.layout('dot')                         # Set hierarchical layout

        filename = str(time())
        postfix = 0
        while exists(filename+str(postfix)+".png"):
            postfix+=1
        filename += str(postfix) + ".png"
        G.draw(filename)                        # Save the image.

        with open(filename, "rb") as handle:
         return xmlrpclib.Binary(handle.read())

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(render_image, "render_image")
server.serve_forever()
