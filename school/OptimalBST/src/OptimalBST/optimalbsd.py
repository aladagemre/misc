# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="emre"
__date__ ="$Mar 10, 2010 9:19:18 PM$"

class OptimalBST:
    
    def __init__(self, p, q, n):
        self.p = p
        self.q = q
        self.n = n
        self.e = {}
        self.root = {}
        self.w = {}

        e = self.e
        w = self.w
        root = self.root
        
        for i in range(0, self.n + 1):
            e[i, i-1] = q[i-1]
            w[i, i-1] = q[i-1]
        for l in range(0, n):
            for i in range(0, n-l+1):
                j = i + l - 1
                e[i,j] = float("inf")
                w[i,j] = w[i, j-1] + p[j] + q[j]
                for r in range(i, j+1):
                    t = e[i, r-1] + e[r+1, j] + w[i,j]
                    if t < e[i,j]:
                        e[i,j] = t
                        root[i,j] = r
                        



if __name__ == "__main__":
    obst = OptimalBST([0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], 4)
