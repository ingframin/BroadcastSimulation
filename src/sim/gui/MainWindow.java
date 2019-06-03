package sim.gui;

import javax.swing.GroupLayout;
import javax.swing.JFrame;
import java.awt.Dimension;

public class MainWindow extends JFrame{

    private static final long serialVersionUID = 1L;

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
        var pane = getContentPane();
        var gl = new GroupLayout(pane);
        pane.setLayout(gl);
        gl.setAutoCreateGaps(true);
        gl.setAutoCreateContainerGaps(true);
        


    }

}