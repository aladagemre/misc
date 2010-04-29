from math import sqrt

class Data:
    def __init__(self, value):
        self.value = value
    
    def __sub__(self, other):
        if isinstance(other, Cluster):
            return other - self
        elif isinstance(other, Data):
            # Make sure they are the same type.
            assert type(self.value) == type(other.value)
            if isinstance(self.value, list) or isinstance(self.value, tuple):
                # make sure that dimensions are the same
                length1 = len(self.value)
                assert  length1 == len(other.value)
                
                sum = 0
                for i in range(length1):
                    sum += (self.value[i] - other.value[i])**2
                
                result = sqrt(sum)
            else:
                # single value
                result = self.value - other.value
                if result < 0:
                    result *= -1
            
            return result
            
        else:
            print "Unexpected subtraction."
        
class Cluster:
    __slots__ = ['elements', 'linkage_type']
    def __init__(self, linkage_type):
        self.linkage_type = linkage_type
        self.elements = []
    
    def __distance_single(self, other):
        min_distance = float("inf")
        
        if isinstance(other, Cluster):
            # Subtract Cluster - Cluster for Single Linkage
            for element in self.elements:
                for other_element in other.elements:
                    value = element - other_element
                    if value < min_distance: min_distance = value
            return min_distance
        
        elif isinstance(other, Data):
            # Subtract Cluster - Data
            for element in self.elements:
                value = element - other
                if value < min_distance: min_distance = value
            return min_distance
        else:
            # Unknown?
            print "Unexpected subtraction."
    def __distance_complete(self, other):
        max_distance = float("-inf")
        if isinstance(other, Cluster):
            # Subtract Cluster - Cluster for Complete Linkage
            for element in self.elements:
                for other_element in other.elements:
                    value = element - other_element
                    if value > max_distance: max_distance = value
            return max_distance
                    
        elif isinstance(other, Data):
            # Subtract Cluster - Data
            for element in self.elements:
                value = element - other
                if value > max_distance: max_distance = value
            return max_distance
        else:
            # Unknown?
            print "Unexpected subtraction."
        
    def __sub__(self, other):
        """Calculates distance between two clusters."""
        method_dict = {'single' : self.__distance_single,
                       'complete': self.__distance_complete, }
        
        return method_dict[self.linkage_type](other)
    
    def __add__(self, other):
        """Merges two Clusters on the first operand."""
        self.elements.extend(other.elements)
        c_new = Cluster(self.linkage_type)
        c_new.elements = self.elements + other.elements
        return c_new
    
    def __repr__(self):
        if hasattr(self, 'id'):
            return "C%d" % self.id
        else:
            return self
        
class HierarchicalClustering:
    def __init__(self, linkage_type="single", filename="soru1.m"):
        self.linkage_type = linkage_type
        self.clusters = []
        self.last_cluster_id = 1
        # initialize
        self.node_dict = {}
        self.clusters = []
        self.filename = filename
        self.output = open(self.filename, "w")
        
    def load_data(self, data):
        for item in data:
            c = Cluster(self.linkage_type)
            c.id = self.last_cluster_id
            self.last_cluster_id += 1
            c.elements.append(Data(item))
            self.clusters.append(c)

    def load_distance_matrix(self, matrix):
        self.matrix = matrix
        for i in range(len(self.matrix)):
            c = Cluster(self.linkage_type)
            c.id = self.last_cluster_id
            c.elements.append(i+1)
            self.clusters.append(c)
            self.node_dict[c.id] = c
            self.last_cluster_id += 1
    def run(self):
        not_finished = True
        self.output.write("dendmatrix = [" )
        step_num = 1
        while not_finished:
            step_num+=1
            if hasattr(self, 'matrix'):
                not_finished = self.step_matrix()
            else:
                not_finished = self.step()
            
        self.output.write("]\n")
        self.output.write("dendrogram(dendmatrix);")
        self.output.close()
        print "Wrote to the file %s" % self.filename
    
    def step_matrix(self):

        # Find what to merge
        
        c1=0
        c2=0
        while c1==c2:
            min_val = float("inf")
            for i in range(1, len(self.matrix)):
                for j in range(i):
                    if self.matrix[i][j] < min_val:
                        min_val = self.matrix[i][j]
                        x, y = i, j
                        
            # Merge
            self.matrix[x][y] = float("inf")
            c1 = self.node_dict[x+1]
            c2 = self.node_dict[y+1]
        
        self.output.write( "%0.4f %0.4f %0.4f;" % (c1.id, c2.id, min_val) )
        
        #print "merging %s and %s at distance %s" % (c1,c2, min_val)
        
        c_new = c1 + c2
        c_new.id = self.last_cluster_id
        self.last_cluster_id += 1
        for element in c_new.elements:
            self.node_dict[element] = c_new
        
        # Delete old ones
        self.clusters.remove(c1)
        self.clusters.remove(c2)
        self.clusters.append(c_new)
        self.node_dict[x+1] = c_new
        self.node_dict[y+1] = c_new
        
        return len(self.clusters) != 1
            
        
    def step(self):
        """Performs the one step of the algoritm"""
        distance_list = []
        min_distance = float("inf")
        
        length = len(self.clusters)
        for i, element in enumerate(self.clusters):
            for otherelement in self.clusters[i+1:]:
                #print "%s - %s = %s" % (element.elements[0].value, otherelement.elements[0].value, element - otherelement)
                if element is not otherelement:
                    distance = element - otherelement
                    if distance < min_distance:
                        # a new minimum record
                        distance_list = [ (element, otherelement, distance) ]
                        min_distance = distance
                    elif distance == min_distance:
                        # Same value, this will be merged too.
                        distance_list.append( (element, otherelement, distance) )
                
        if distance_list:
            element = distance_list.pop(0)            
            c1 = element[0]
            c2 = element[1]
            distance = element[2]
            
            self.output.write("%0.4f %0.4f %0.4f;" % (c1.id, c2.id, distance))
            
            c_new = c1 + c2
            c_new.id = self.last_cluster_id
            self.last_cluster_id += 1
            self.clusters.append(c_new)
            
            self.clusters.remove(c1) # remove cluster as it is merged. Following steps wont see it.
            self.clusters.remove(c2)
                    
            return True
        else:
            return False
    
soru2data = ( 
( 40.330, 40.218, 151.0, 54.4, 40.330, 9.077, 0.0, 628.0 ),
( 0.89, 40.247, 202.0, 57.9, 40.211, 5.088, 40.262, 1.555 ),
( 15.707, 40.283, 113.0, 53.0, 40.271, 9.212, 0.0, 1.058 ),
( 40.210, 40.220, 168.0, 56.0, 0.3, 6.423, 34.3, 700.0 ),
( 17.899, 40.398, 192.0, 51.2, 36.526, 3.300, 40.344, 2.044 ),
( 11.689, 40.311, 111.0, 60.0, -2.2, 11.127, 40.320, 1.241 ),
( 44.562, 40.221, 175.0, 67.6, 40.211, 7.642, 0.0, 1.652 ),
( 40.452, 40.218, 245.0, 57.0, 40.240, 13.082, 0.0, 309.0 ),
( 12.420, 13.0, 168.0, 60.4, 40.216, 8.406, 0.0, 862.0 ),
( 40.513, 40.280, 197.0, 53.0, 40.361, 6.455, 39.2, 623.0 ),
( 0.75, 40.305, 173.0, 51.5, 40.304, 17.441, 0.0, 768.0 ),
( 41.275, 40.431, 178.0, 62.0, 40.362, 6.154, 0.0, 1.897 ),
( 42.005, 40.371, 199.0, 53.7, 40.274, 7.179, 50.2, 527.0 ),
( 40.422, 36.861, 96.0, 49.8, 40.269, 9.673, 0.0, 588.0 ),
( 0.96, 40.336, 164.0, 62.2, -0.1, 6.468, 0.9, 1.400 ),
( 42.370, 40.430, 252.0, 56.0, 40.218, 15.991, 0.0, 620.0 ),
( 0.76, 40.274, 136.0, 61.9, 36.770, 5.714, 40.245, 1.920 ),
( 40.299, 40.341, 150.0, 56.7, 40.361, 10.140, 0.0, 1.108 ),
( 42.370, 40.370, 104.0, 54.0, -2.1, 13.507, 0.0, 636.0 ),
( 43.831, 40.401, 148.0, 59.9, 40.301, 7.287, 41.1, 702.0 ),
( 40.269, 40.337, 204.0, 61.0, 40.301, 6.650, 0.0, 2.116 ),
( 40.360, 40.246, 174.0, 54.3, 40.426, 10.093, 40.355, 1.306 ),
)

hc = HierarchicalClustering("complete", "/home/emre/Desktop/odev2/soru2.m")
hc.load_data(soru2data)
hc.run()


soru1distmatrix = [ 
[0, 2, 2, 7, 6, 6, 6, 6, 7, 9, 9],
[2, 0, 1, 5, 4, 6, 6, 6, 7, 8, 9],
[2, 1, 0, 6, 5, 6, 5, 5, 6, 8, 9],
[7, 5, 6, 0, 5, 9, 9, 9, 10, 8, 9],
[6, 4, 5, 5, 0, 7, 7, 7, 8, 9, 9],
[6, 6, 6, 9, 7, 0, 2, 1, 5, 10, 9],
[6, 6, 5, 9, 7, 2, 0, 1, 3, 10, 9],
[6, 6, 5, 9, 7, 1, 1, 0, 4,10, 9],
[7, 7, 6, 10, 8, 5, 3, 4, 0, 10, 9],
[9, 8, 8, 8, 9, 10, 10, 10, 10, 0, 8],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 0],
]
hc = HierarchicalClustering("single", "/home/emre/Desktop/odev2/soru1.m")
hc.load_distance_matrix(soru1distmatrix)
hc.run()