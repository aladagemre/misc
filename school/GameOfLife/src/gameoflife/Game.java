/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package gameoflife;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 *
 * @author emre
 */
public class Game extends JFrame {

    private Grid grid;    
    private ControlPanel controlArea;
    private DrawingPanel drawingArea;
    private int size = 100;
    
    public static void main(String[] args) {
        new Game();
    }

    public Game() {
        super("The Game of Life");
        setupGui();
        setEvents();
        createGrid();
        updateDrawing();

    }

    private void createGrid(){
        grid = new Grid(size);
    }

    private void updateDrawing(){
        drawingArea.updateGrid(grid);
    }
    private void setupGui(){
        //setPreferredSize(new Dimension(850, 768));
        setExtendedState(getExtendedState()|JFrame.MAXIMIZED_BOTH);
        WindowUtilities.setNativeLookAndFeel();
        addWindowListener(new ExitListener());
        Container content = getContentPane();
        content.setBackground(Color.lightGray);

        controlArea = new ControlPanel("Operations");

        content.add(controlArea, BorderLayout.EAST);
        drawingArea = new DrawingPanel();
        drawingArea.setPreferredSize(new Dimension(700,700));
        // Preferred height is irrelevant, since using WEST region
        drawingArea.setBorder(BorderFactory.createLineBorder(Color.blue, 2));
        drawingArea.setBackground(Color.white);

        content.add(drawingArea, BorderLayout.WEST);
        pack();
        setVisible(true);
    }

    private void setEvents(){

        // NEXT BUTTON
        controlArea.nextButton.addMouseListener(new MouseListener() {

            public void mouseClicked(MouseEvent e) {
                
                int numIteration =(Integer) controlArea.numIteration.getValue();
                grid = drawingArea.getGrid();
                for (int i=0; i < numIteration; i++)
                    grid.iterate();
                updateDrawing();
            }

            public void mousePressed(MouseEvent e) {}
            public void mouseReleased(MouseEvent e) {}
            public void mouseEntered(MouseEvent e) {}
            public void mouseExited(MouseEvent e) {}
        });

        // OTHERS
    }

}
