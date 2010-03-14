/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package gameoflife;
import java.awt.*;
import java.awt.event.*;

/** A listener that you attach to the top-level Frame or JFrame of
 *  your application, so quitting the frame exits the application.
 *  1998-99 Marty Hall, http://www.apl.jhu.edu/~hall/java/
 */

public class ExitListener extends WindowAdapter {
  public void windowClosing(WindowEvent event) {
    System.exit(0);
  }
}
