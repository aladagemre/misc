package gameoflife;

import java.util.ArrayList;

/**
 *
 * @author emre
 */
public class Grid {

    private int SIZE = 100;
    private Cell[][] board = new Cell[getSIZE()][getSIZE()];

    public Grid(){
        initializeBoard();
    }

    public Grid(int size){
        SIZE = size;
        initializeBoard();
    }

    /**
     * Use this to get a cell at a specific position.
     * @param row The row the cell is on.
     * @param col The column the cell is on.
     * @return the requested Cell object.
     */
    public Cell getCellAt(int row, int col){
       return board[row][col];
    }

    private void initializeBoard(){
        for (int i=0; i< getSIZE(); i++){
            for (int j=0; j<getSIZE(); j++){
                board[i][j] = new Cell(false);
            }
        }

        setAliveAt(3, 3);
        setAliveAt(4, 3);
        setAliveAt(5, 3);

        setAliveAt(0, 0);
        setAliveAt(0, 1);
        setAliveAt(1, 0);
        setAliveAt(1, 1);

        setAliveAt(10, 10);
        setAliveAt(10, 11);
        setAliveAt(10, 12);
        setAliveAt(11, 10);
        setAliveAt(11, 11);
        setAliveAt(11, 12);
        setAliveAt(12, 10);
        setAliveAt(12, 11);
        setAliveAt(12, 12);

    }

    private void setAliveAt(int row, int col){
        getCellAt(row, col).resurrect();
    }

    private void setDeadAt(int row, int col){
        getCellAt(row, col).kill();
    }
    public void displayBoard(){
        System.out.print("  ");
        for (int i=0; i<getSIZE(); i++){
            // print the headers
            System.out.printf("%3d", i);
        }
        System.out.println();
        
        for (int i=0; i< getSIZE(); i++){
            System.out.print(i + "-"); // print row number
            for (int j=0; j<getSIZE(); j++){
                System.out.printf("%3s", board[i][j]);
            }
            System.out.println();
        }
    }


    public void iterate(){
       // Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
       // Any live cell with more than three live neighbours dies, as if by overcrowding.
       // Any live cell with two or three live neighbours lives on to the next generation. NO NEED TO CHECK
       // Any dead cell with exactly three live neighbours becomes a live cell.

        // Do scheduling
        for (int i=0; i < getSIZE(); i++){
            for (int j=0; j < getSIZE(); j++){
                if (board[i][j].isLive()){
                    checkDie(i,j);
                }
                else {
                    checkResurrection(i,j);
                }
            }
        }

        // Perform Scheduled Operations
        for (int i=0; i < getSIZE(); i++){
            for (int j=0; j < getSIZE(); j++){
                board[i][j].performOperation();
            }
        }
    }

    private int getAliveNeighborSum(int row, int col){
        int aliveSum = 0;
        ArrayList<Cell> neighbors = new ArrayList<Cell>();

        try { neighbors.add( board[row][col-1]);} catch (Exception e) {}
        try { neighbors.add(board[row][col+1]);} catch (Exception e) {}
        try { neighbors.add(board[row-1][col]);} catch (Exception e) {}
        try { neighbors.add(board[row+1][col]);} catch (Exception e) {}
        try { neighbors.add(board[row-1][col-1]);} catch (Exception e) {}
        try { neighbors.add(board[row+1][col+1]);} catch (Exception e) {}
        try { neighbors.add(board[row-1][col+1]);} catch (Exception e) {}
        try { neighbors.add(board[row+1][col-1]);} catch (Exception e) {}

        for (int i = 0; i< 8; i++){
            try {
                if (neighbors.get(i).isLive())
                    aliveSum++;
            }
            catch(Exception e) {
                // do nothing
            }
        }

        // Found the alive neighbors.
        return aliveSum;
    }

    private void checkDie(int i, int j){
        // Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        // Any live cell with more than three live neighbours dies, as if by overcrowding.
        int aliveNeighbors = getAliveNeighborSum(i, j);
        if (aliveNeighbors < 2 || aliveNeighbors > 3)
            board[i][j].scheduleKill();
    }

    
    private void checkResurrection(int i, int j) {
        // Any dead cell with exactly three live neighbours becomes a live cell.

        int aliveNeighbors = getAliveNeighborSum(i, j);
        if (aliveNeighbors == 3)
            board[i][j].scheduleResurrect();
    }

    /**
     * @return the SIZE
     */
    public int getSIZE() {
        return SIZE;
    }

    /**
     * @param SIZE the SIZE to set
     */
    public void setSIZE(int SIZE) {
        this.SIZE = SIZE;
    }


}
