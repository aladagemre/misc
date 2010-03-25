/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package gameoflife;

import javax.swing.JApplet;

/**
 *
 * @author emre
 */
public class GameApplet extends JApplet {

    Game g;
    /**
     * Initialization method that will be called after the applet is loaded
     * into the browser.
     */
    public void init() {
        setSize(300,100);

        g = new Game();
        g.setTitle("The Game of Life by Ahmet Emre Aladağ");
        g.setVisible(true);
    }

    public void destroy(){
        g.dispose();
        g = null;
    }
    // TODO overwrite start(), stop() and destroy() methods

}
