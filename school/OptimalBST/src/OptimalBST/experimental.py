class MyOptimalBST:
    def __init__(self, p): # q):
        self.p = p
        #self.q = q
        self.psum = {}
        self.c = {}
        self.n = len(p)

        self.fill_psum()
        self.fill_diagonal()
        self.calculate_costs()

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

        print "n=", self.n
        for s in xrange(self.n-1, -1, -1):
            print "s=",s
            for t in xrange(s+1, self.n):
                print "t=",t
                for k in xrange(s+1, t+1):
                    print "k=",k
                    print "s=%d, t=%d, k=%d" % (s,t,k)
                    #print "c[%d,%d] = c[%d, %d] + c[%d, %d] + psum[%d,%d] = " % (s,t, s,k-1,k+1,t,s,t)
                    if k+1 > t:
                        current_cost = self.psum[s,t] # NOT SURE!
                    else:
                        current_cost = self.c[s,k-1] + self.c[k+1,t] + self.psum[s,t]
                    self.c[s,t] = current_cost
                    #print "c[%d,%d] = c[%d, %d] + c[%d, %d] + psum[%d,%d] = %f + %f + %f = %f" % (s,t, s,k-1,k+1,t,s,t, self.c[s,k-1], self.c[k+1,t],self.psum[s,t], current_cost)
                    #print self.displayAsMatrix(self.c)
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


"""

class OptimalCLSR:
    def sort_custom_keys(self):
        """Sorts custom keys and their probabilities accordingly.
        This method is useless."""
        # If no custom keys provided, exit.
        if not self.custom_keys:
            return
        # If custom keys are sorted, exit.
        if sorted(self.custom_keys) == self.custom_keys:
            return

        temp_dict = {}
        for (index, ck) in enumerate(self.custom_keys):
            temp_dict[ck] = self.p[index], self.q[index]

        for (index, value) in enumerate(sorted(temp_dict.keys())):
            self.custom_keys[index] = temp_dict[value]
            self.p[index+1] = value[0]
            self.q[index] = value[1] # q has 1 more element. Can't handle it.