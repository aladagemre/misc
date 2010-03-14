package gameoflife;

/**
 *
 * @author emre
 */
public class Cell {
    
    private boolean live;
    private boolean sKill=false;
    private boolean sResurrect=false;

    public Cell(){
        live = true;
    }

    public Cell(boolean alive){
        live = alive;
    }

    /**
     * @return if alive.
     */
    public boolean isLive() {
        return live;
    }

    /**
     * Tells if the cell is dead.
     * @return if dead
     */
    public boolean isDead() {
        return !live;
    }

    /**
     * Sets the cell dead
     */
    public void kill(){
        live = false;
    }

    /**
     * Schedules a kill operation for the cell.
     */
    public void scheduleKill(){
        sKill = true;
        sResurrect = false;
    }

    /**
     * Sets the cell alive.
     */
    public void resurrect(){
        live = true;
    }

    /**
     * Schedules a resurrection operation for the cell.
     */
    public void scheduleResurrect(){
        sResurrect = true;
        sKill = false;
    }

    public void toggle(){
        if (isLive()){
            kill();
        }
        else {
            resurrect();
        }
    }

    /**
     * Performs scheduled operation: kill or resurrect.
     */
    public void performOperation(){
        if (sKill)
            kill();
        else if(sResurrect)
            resurrect();
    }

    @Override
    public String toString(){
        return isLive() ? "1":"0";
    }
}
