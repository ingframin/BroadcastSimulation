package sim.gui;

import javax.swing.JLabel;
import javax.swing.JFrame;
import javax.swing.JTextField;
import java.awt.BorderLayout;
import java.awt.Dimension;
import javax.swing.JPanel;

public class MainWindow extends JFrame{

    private static final long serialVersionUID = 1L;
    JTextField numNodesField;

    public MainWindow(){
        setTitle("Drone SSID broadcast simulator");
        setSize(new Dimension(800,600));
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        initUI();
        setVisible(true);
        pack();
    }

    private void initUI(){
        JLabel nNodes = new JLabel("#Nodes");
        numNodesField = new JTextField(8);

        add(nNodes,BorderLayout.WEST); 
        add(numNodesField,BorderLayout.WEST);
        


    }

}