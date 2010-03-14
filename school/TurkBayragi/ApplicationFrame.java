/**
 *
 * @author emre
 */
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class ApplicationFrame
    extends Frame {
    public Color color = Color.red;
  public ApplicationFrame() { this("Turkish Flag v0.1"); }


  private class MouseHandler implements MouseListener {

        public void mouseClicked(MouseEvent e) {
            System.out.println("Clicked on the flag");
            // To change the color of the flag:
            /*if (color == Color.red)
                color = Color.green;
            else
                color = Color.red;

            Random rand = new Random();
            
            color = new Color(rand.nextInt(256),
                         rand.nextInt(256),
                         rand.nextInt(256));

            e.getComponent().repaint();*/
        }

        public void mousePressed(MouseEvent e) {

        }

        public void mouseReleased(MouseEvent e) {

        }

        public void mouseEntered(MouseEvent e) {

        }

        public void mouseExited(MouseEvent e) {

        }
      
  }
  public ApplicationFrame(String title) {
    super(title);
    createUI();
    this.addMouseListener(new MouseHandler());
  }

  protected void createUI() {
    setSize(900, 600);
    center();

    addWindowListener(new WindowAdapter() {
            @Override
      public void windowClosing(WindowEvent e) {
        dispose();
        System.exit(0);
      }
    });
  }

  public void center() {
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    Dimension frameSize = getSize();
    int x = (screenSize.width - frameSize.width) / 2;
    int y = (screenSize.height - frameSize.height) / 2;
    setLocation(x, y);
  }
}
