public class Hanoi {
    public static void main(String args[]){
        Hanoi y = new Hanoi();
        y.HANOITOWERS(3, 1, 3);
    }
 
        
    public int HANOITOWERS(int n, int fromPeg, int toPeg){
    
        int unusedPeg;
    
        if (n == 1){
            System.out.printf("Move disk from peg %d to peg %d\n", fromPeg, toPeg);
            return 0;
        }
        unusedPeg = 6 - fromPeg - toPeg;
        HANOITOWERS(n-1, fromPeg, unusedPeg);
        System.out.printf("Move disk from peg %d to peg %d\n", fromPeg, toPeg);
        HANOITOWERS(n-1, unusedPeg, toPeg);
        return 0;
    
    }


}