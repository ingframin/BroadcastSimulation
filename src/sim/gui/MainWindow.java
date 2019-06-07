package sim.gui;

import javax.swing.JLabel;
import javax.swing.JFrame;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JPanel;

import sim.main.BroadcastSimulator;
import static sim.main.ConfigReader.*;

public class MainWindow extends JFrame{

    private static final long serialVersionUID = 1L;
    JTextField numNodesField;
    JTextField configPathField;
    JButton runButton;

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
        var wpane = new JPanel();
        wpane.setLayout(new BoxLayout(wpane, BoxLayout.Y_AXIS));
        JLabel nNodes = new JLabel("Number of Nodes");
        numNodesField = new JTextField(8);
        numNodesField.setMaximumSize(new Dimension(120,20));
        JLabel configPathLabel = new JLabel("Configuration file path");
        configPathField = new JTextField();
        configPathField.setMaximumSize(new Dimension(120,20));
        nNodes.setAlignmentX(Component.CENTER_ALIGNMENT);
        numNodesField.setAlignmentX(Component.CENTER_ALIGNMENT);
        configPathLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        configPathField.setAlignmentX(Component.CENTER_ALIGNMENT);
        runButton = new JButton("Run");
        runButton.setAlignmentX(Component.CENTER_ALIGNMENT);
        wpane.add(nNodes);
        wpane.add(numNodesField);
        wpane.add(Box.createVerticalGlue());
        wpane.add(configPathLabel);
        wpane.add(configPathField);
        wpane.add(Box.createVerticalGlue());
        wpane.add(runButton);
        runButton.addActionListener((e)->{
            var path = configPathField.getText();
            var res = readConfigFile(path);
            var config = res.get(0);
            int n_nodes = Integer.parseInt(numNodesField.getText());
            var nodes = BroadcastSimulator.generateNodes(n_nodes, config.Trx, config.Tn, config.Ttx, config.Vs,config.Vn,config.Vb);
            BroadcastSimulator.run("0",nodes);
        });
        add(wpane,BorderLayout.CENTER);


    }
    public static void main(String[] args){
        SwingUtilities.invokeLater(()->{
            new MainWindow();
        });
    
    }

}