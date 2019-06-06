package sim.main;
import sim.engine.*;
import sim.gui.*;
import javax.swing.SwingUtilities;
import static sim.main.ConfigReader.*;

public class BroadcastSimulator{
	private BroadcastSimulator(){}

	public static Node[] generateNodes(int Nd, int Ts,int Tn, int Tb,double[] vs,double[] vn, double[] vb){
		
		Node[] nodes = new Node[Nd];
		for(int i=0;i<Nd;i++){
			var n = new Node(Ts,Tn,Tb,vs,vn,vb);
			nodes[i] = n;
		}
		return nodes;

	}

	public static void run(String runID, Node[] nodes){
		for(int i=0;i<nodes.length;i++){
			var n = nodes[i];
			var l = new Logger("./results/r"+runID+"-d"+i+"-result.txt");
			for(int k=0;k <15_000_000;k++){
				n.run();
				l.log(n.getCurrentState());
			}
			l.dump(false);
			
		}		
	}

	
	
  public static void main(String[] args){

	int n_nodes = 4;
			
	for(int i=1;i<10;i++){
		var res = readConfigFile("config"+String.valueOf(i)+".txt");
		var config = res.get(0);
		var nodes = generateNodes(n_nodes, config.Trx, config.Tn, config.Ttx, config.Vs,config.Vn,config.Vb);
		run(String.valueOf(i),nodes);
	}

	}
	
}