/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package gameoflife;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JPanel;

/**
 *
 * @author emre
 */
public class DrawingPanel extends JPanel {
    private Grid grid;
    private int w;

    public DrawingPanel(){
        super();
        setEvents();
        
    }
    @Override
    public void paintComponent(Graphics g){
        w = getWidth() / grid.getSIZE();
        int newSize = grid.getSIZE() * w;
        setSize(new Dimension(newSize, newSize));
        for (int row=0; row < grid.getSIZE(); row++){
            for (int col=0; col < grid.getSIZE(); col++){
                if (grid.getCellAt(row, col).isLive())
                    g.setColor(Color.white);
                else
                    g.setColor(Color.black);

                // now draw the rect
                g.fillRect(col*w, row*w, w, w);
                

            }
        }
    }

    public void updateGrid (Grid grid){
        this.grid = grid;
        repaint();
    }

    public Grid getGrid(){
        return grid;
    }    

    private void setEvents(){
        this.addMouseListener(new MouseListener() {

            public void mouseClicked(MouseEvent e) {
                int x,y,row,col;
                x = e.getX();
                y = e.getY();

                col = x / w;
                row = y / w;
                

                //System.out.println(row + "-" + col);
                grid.getCellAt(row, col).toggle();
                repaint();
                
            }

            public void mousePressed(MouseEvent e) {}
            public void mouseReleased(MouseEvent e) {}
            public void mouseEntered(MouseEvent e) {}
            public void mouseExited(MouseEvent e) {}
        });
    }

}
