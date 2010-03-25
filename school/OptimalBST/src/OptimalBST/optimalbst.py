#-*-encoding:utf-8-*-
class MyOptimalBST:
    def __init__(self, p): # q):
        self.p = p
        #self.q = q
        self.psum = {}
        self.c = {}
        self.n = len(p)

        self.fill_psum()
        self.fill_diagonal()
        
    def fill_psum(self):
        for i in xrange(self.n): # Row
            rowsum = 0
            for j in xrange(i, self.n): # column
                rowsum += self.p[j]
                self.psum[(i, j)] = rowsum
                #print rowsum,
            #print

    def fill_diagonal(self):
        for i in xrange(self.n):
            self.c[(i,i)] = self.p[i]
            

    def displayAsMatrix(self, dictionary):
        for row in xrange(self.n):
            for col in xrange(self.n):
                value = dictionary.get((row,col))
                if value:
                    print "%4s\t" % value,
                else:
                    print "%4s\t" % "",
            print
                
                    
    def calculate_costs(self):
        min_cost = float("inf")

        for s in xrange(self.n-1, -1, -1):
            for t in xrange(s+1, self.n):
                for k in xrange(s+1, t):
                    current_cost = self.c[s,k-1] + self.c[k+1,t] + self.psum[s,t]
                    self.c[s,t] = current_cost
                    print self.displayAsMatrix(self.c)
                    print "c[%d,%d] = c[%d, %d] + c[%d, %d] + psum[%d,%d] = %f + %f + %f = %f" % (s,t, s,k-1,k+1,t,s,t, self.c[s,k-1], self.c[k+1,t],self.psum[s,t], current_cost)
                    if current_cost < min_cost:
                        min_cost = current_cost
                


class OptimalBST:
    
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n
        self.e = {}
        self.root = {}
        self.w = {}
        self.Leftson = Leftson = {}
        self.Rightson = Rightson = {}
        self.c = c = {}
        self.r = r = {}
        self.w = w = {}

        for i in xrange(0,n):
            w[i,i] = q[i]
            c[i,i] = 0
            r[i,i] = 0
        for length in xrange(1, n):
            for i in xrange(0, n-length):
                j = i+length
                w[i,j] = w[i,j-1] + p[j] + q[j]
                if length == 1:
                    m = j
                else:
                    minimum = float("inf")
                    for k in xrange(r[i,j-1], r[i+1,j]+1):
                        value = c[i,k-1] + c[k,j]
                        if value < minimum:
                            minimum = value
                            kvalue = k
                    m = kvalue

                c[i,j] = w[i,j] + c[i,m-1] + c[m,j]
                r[i,j] = m
                Leftson[r[i,j]] = r[i,m-1]
                Rightson[r[i,j]] = r[m,j]

"""
    # Pseudocode in http://www.ics.uci.edu/~dan/class/165/notes/OptBST.html
    for i := 0 to n do
       wi,i := qi
       ci,i := 0
       ri,i := 0
    for length := 1 to n do
       for i := 0 to n-length do
          j := i + length
          wi,j := wi,j-1 + pj + qj
          if length=1 then
             m := j
          else
             m := value of k (with ri,j-1 ≤ k ≤ ri+1,j) which minimizes (ci,k-1+ck,j)

          ci,j := wi,j + ci,m-1 + cm,j
          ri,j := m
          Leftson(ri,j) := ri,m-1
          Rightson(ri,j) := rm,j



        # ALGORITHMS BOOK IMPLEMENTATION
        e = self.e
        w = self.w
        root = self.root
        
        for i in range(1, self.n + 1):
            e[i, i-1] = q[i-1]
            w[i, i-1] = q[i-1]
        for l in range(1, n+1):
            for i in range(1, n-l+2):
                j = i + l - 1
                e[i,j] = float("inf")
                print i,j
                w[i,j] = w[i, j-1] + p[j] + q[j]
                for r in range(i, j+1):
                    t = e[i, r-1] + e[r+1, j] + w[i,j]
                    if t < e[i,j]:
                        e[i,j] = t
                        root[i,j] = r"""


if __name__ == "__main__":
    obst = MyOptimalBST([0.25, 0.25, 0.25, 0.25])#, [0.25, 0.25, 0.25, 0.25], 4)
    #obst.fill_psum()
    #print obst.psum
    #obst.displayAsMatrix(obst.psum)
    #obst.displayAsMatrix(obst.c)
    obst.calculate_costs()
