package fractalgeometry;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JFrame;

public class FractalFrame extends JFrame{

    private Fractal f;
    private int[][] matrix;
    public int SIZE=700;

    public FractalFrame(){
        super("Fractal Demo");
        f = new Fractal(SIZE, new Complex(-0.4, 0.6));
        //f = new Fractal(SIZE, new Complex(-0.835,-0.2321));
        //f = new Fractal(SIZE, new Complex(-0.8,0.156));
        //f = new Fractal(SIZE, new Complex(-0.70176,-0.3842));
        //f = new Fractal(SIZE, new Complex(0.45, 0.1428));
        //f = new Fractal(SIZE, new Complex(0.285,0.01));
        //f = new Fractal(SIZE, new Complex(0.285,0));
        //f = new Fractal(SIZE, new Complex(-0.618,0));
        //f = new Fractal(SIZE, new Complex());
        matrix = f.getMatrix();
        
    }
    @Override
    public void paint( Graphics g ) {
        for (int i=0; i < matrix.length; i++){
            for (int j=0; j< matrix.length; j++){
                g.setColor(Color.getColor("", matrix[i][j]));
                g.fillRect(i, j, 1, 1);
            }
        }
        
    }

    public static void main(String[] args) {
        FractalFrame ff = new FractalFrame();
        ff.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ff.setPreferredSize(new Dimension(ff.SIZE, ff.SIZE));
        ff.setSize(new Dimension(ff.SIZE, ff.SIZE));
        ff.setVisible(true);
        
    }


}
