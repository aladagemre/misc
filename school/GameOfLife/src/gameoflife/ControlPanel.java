package gameoflife;

import java.awt.Button;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSpinner;
import javax.swing.SpinnerModel;
import javax.swing.event.ChangeListener;

/**
 *
 * @author emre
 */
public class ControlPanel extends JPanel {

    public Button nextButton;
    public JSpinner numIteration;

    public ControlPanel(String title) {
        //super(new GridLayout(2, 1));
        super();
        setBackground(Color.lightGray);
        setBorder(BorderFactory.createTitledBorder("Number of Iterations"));
        setPreferredSize(new Dimension(150,200));

        numIteration = new JSpinner();
        numIteration.setPreferredSize(new Dimension(50,30));
        numIteration.setValue(1);
        add(numIteration);
        nextButton = new Button("Iterate");
        add(nextButton);

    }
}
