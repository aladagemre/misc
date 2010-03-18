package fractalgeometry;

public class Fractal {

    private int SIZE;
    private Complex c;
    private int[][] matrix;

    public Fractal(){
        this(500, new Complex(0.4, 0.6));        
    }
    
    public Fractal(int SIZE, Complex c){
        this.c = c;
        this.SIZE = SIZE;
        matrix = new int[SIZE][SIZE];
        calculateImage();
    }
    
    private Complex f1(Complex z){
        return z.times(z).plus(c);
    }

    private void calculateImage(){
        int i;
        for (int x=0; x<SIZE; x++){
            for (int y=0; y<SIZE; y++){
                double re = (x * 2.0 / SIZE) - 1.0;
                double im = (y * 2.0 / SIZE) - 1.0;

                Complex z = new Complex(re, im);

                for (i=0; i<256; i++){
                    if (z.norm() > 2.0)
                        break;
                    z = f1(z);
                }

                matrix[x][y] = i*5;                
            }
        }
        
    }

    public void printMatrix(){
        for (int i=0; i<SIZE; i++){
            for (int j=0; j<SIZE; j++)
                System.out.printf("%3d", matrix[i][j]);
            System.out.println();
        }

    }

    public int[][] getMatrix(){
        return matrix;
    }

    public static void main(String[] args) {
        Fractal f = new Fractal();
        f.printMatrix();
        
    }

}
