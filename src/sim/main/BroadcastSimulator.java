package sim.main;
import sim.engine.*;
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
			var log_m = new Logger("./results/m"+runID+"-d"+i+"-result.txt");
			boolean flag = false;
			for(int k=0;k <10_000_000;k++){
				n.run();
				char s= n.getCurrentState();
				l.log(s);
				if(s != 'B'){
					flag = false;
				}
				if(s == 'B' && !flag){
					String string = new Message(String.valueOf(k)).toString();
					log_m.log(string);
					flag = true;
				}
				
			}
			Message.resetCounter();
			l.dump(false);
			log_m.dump(false);
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