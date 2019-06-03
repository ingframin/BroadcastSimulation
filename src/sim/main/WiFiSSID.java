package sim.main;
import sim.engine.*;
import java.util.ArrayList;

public class WiFiSSID{

	public static Node[] generateNodes(int Nd, int Ts,int Tn, int Tb,double[] vs,double[] vn, double[] vb){
		
		Node[] nodes = new Node[Nd];
		for(int i=0;i<Nd;i++){
			var n = new Node(Ts,Tn,Tb,vs,vn,vb);
			nodes[i] = n;
		}
		return nodes;

	}
	
  public static void main(String[] args){
	var res = ConfigReader.readConfigFile("config1.txt");
	//Temporary code
	var config = res.get(0);
	int n_nodes = 20;
	var nodes = generateNodes(n_nodes, 120, 30, 100, config.Vs,config.Vn,config.Vb);		
		for(int i=0;i<n_nodes;i++){
			var n = nodes[i];
			var l = new Logger("./results/d"+i+"-result.txt");
			for(int k=0;k <10_000_000;k++){
				n.run();
				l.log(n.getCurrentState());
			}
			l.dump(false);
			
		}		

	}
	
}