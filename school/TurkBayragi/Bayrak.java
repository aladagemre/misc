/**
 *
 * @author emre
 */
import java.awt.*;
import java.awt.geom.*;

public class Bayrak extends ApplicationFrame {

    private double G=600.0;
    
    @Override
    public void paint(Graphics g) {
        drawBackground(g);
        drawBigCircle(g);
        drawSmallCircle(g);
        drawStar(g);
    }
    public void drawBackground(Graphics g){
        Graphics2D g2 = (Graphics2D)g;
        Rectangle2D br = new Rectangle2D.Double(0.0, 0.0, 1.5*G, G);
        g2.setPaint(color);
        g2.fill(br);
    }
    
    
    public static Ellipse2D.Double getCircle(double x, double y, double r){
        return new Ellipse2D.Double(x-r, y-r, r*2, r*2);
    }

    public void drawBigCircle(Graphics g){
	Graphics2D g2 = (Graphics2D)g;
	Ellipse2D bigCircle = getCircle(G/2, G/2, G/4);
	
	g2.setPaint(Color.white);
	g2.fill(bigCircle);
    }

    public void drawSmallCircle(Graphics g){
	Graphics2D g2 = (Graphics2D)g;
	Ellipse2D bigCircle = getCircle(0.5625*G, G/2, G/5);
	g2.setPaint(color);
	g2.fill(bigCircle);
    }

    public void drawStar(Graphics g){

	double r = G/8;

	double xBase = (0.35 + 1/3.0)*G;
	double yBase = 3*G/8;

	double xPoints[] = { 0, 1.80901*r, 0.691*r, 0.691*r, 1.80901*r, 0};
	double yPoints[] = { r, 0.4123*r, 1.951*r, 0.049*r, 1.5877*r, r };

	Graphics2D g2 = ( Graphics2D ) g;
	g2.setPaint(Color.white);

	GeneralPath star = new GeneralPath();
	star.moveTo( xBase + xPoints[ 0 ], yBase + yPoints[ 0 ] );

	for ( int k = 1; k < xPoints.length; k++ )
	    star.lineTo( xBase + xPoints[ k ], yBase + yPoints[ k ] );

	star.closePath();
	g2.fill(star);
	
  }
}
