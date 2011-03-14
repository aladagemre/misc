#include <stdio.h>
//#include <stdlib.h>

int HANOITOWERS(int n, int fromPeg, int toPeg);

int main()
{
    printf("Hello world!\n");


    HANOITOWERS(3, 1, 3);

    return 0;
}

int HANOITOWERS(int n, int fromPeg, int toPeg){

    int unusedPeg;

    if (n == 1){
        printf("Move disk from peg %d to peg %d\n", fromPeg, toPeg);
        return 0;
    }
    unusedPeg = 6 - fromPeg - toPeg;
    HANOITOWERS(n-1, fromPeg, unusedPeg);
    printf("Move disk from peg %d to peg %d\n", fromPeg, toPeg);
    HANOITOWERS(n-1, unusedPeg, toPeg);
    return 0;

}
