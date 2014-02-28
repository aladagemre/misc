# encoding: utf8
"""
>>> graph.get_connections("username","likes")
{'data': []}
>>> mutual_friends = graph.get_connections("me", "mutualfriends/username")
>>> user = graph.get_object("239048238945720572")
>>> user = graph.get_object("username")
>>> friends2 = graph.get_connections("me","friends")
"""


import facebook
import networkx
import matplotlib.pyplot as plt


class Person:
    def __init__(self, d):
        x = d.get('name')
        if isinstance(x, str):
            self.name = unicode(x.decode("latin5").encode("utf-8"))
        elif isinstance(x, unicode):
            self.name = x
        self.id = d.get('id')

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.__unicode__()

    def __lt__(self, other):
        return self.name.__lt__(other.name)

def get_graph(token):
    graph = facebook.GraphAPI(token)
    return graph
    
def my_friends(graph):
    myfrs = graph.get_connections("me", "friends")['data']
    return [Person(person) for person in myfrs]

def my_network(graph, my_name):
    for friend in my_friends(graph):
        print (friend.name, type(friend.name))
        G.add_edge(my_name, friend.name)

        mutual_friends = graph.get_connections("me", "mutualfriends/%s" % friend.id)['data']
        mutual_objects = [Person(person) for person in mutual_friends]
        print(len(mutual_objects))

        for obj in mutual_objects:
            G.add_edge(my_name, obj.name)
            G.add_edge(friend.name, obj.name)


def draw():
    # draw graph
    pos1 = networkx.spring_layout(G)
    networkx.draw_networkx(G, pos1)
    # show graph
    plt.show()
    if not os.path.exists("output"):
        os.mkdir("output")
    plt.savefig('output/my_friendship.png')
    networkx.write_graphml(G, "output/my_graph.graphml")

if __name__ == "__main__":
    name = raw_input("Enter your name as node label:")
    token = raw_input("Enter FB access token:")
    fbgraph = get_graph(token)
    G = networkx.Graph()
    my_network(fbgraph, name)
    draw()

#print(my_friends())
