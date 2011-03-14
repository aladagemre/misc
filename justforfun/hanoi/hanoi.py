def HANOITOWERS(n, fromPeg, toPeg):
    if n==1:
        print "Move disk from peg %d to peg %d" % (fromPeg, toPeg)
        return
    unusedPeg = 6 - fromPeg - toPeg
    HANOITOWERS(n-1, fromPeg, unusedPeg)
    print "Move disk from peg %d to peg %d" % (fromPeg, toPeg)
    HANOITOWERS(n-1, unusedPeg, toPeg)
    return
 
HANOITOWERS(3, 1, 3)
