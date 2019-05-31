package sim.main;
import sim.engine.*;
import java.util.ArrayList;

public class WiFiSSID{

	public static Node[] generateNodes(int Nd, int Ts,int Tn, int Tb,double[] vs,double[] vn, double[] vb){
		
		Node[] nodes = new Node[Nd];
		for(int i=0;i<Nd;i++){
			var n = new Node(Ts,Tn,Tb);
			n.setScanTransitions(vs[0], vs[1], vs[2]);
			n.setNetworkTransitions(vn[0], vn[1], vn[2]);
			n.setBroadcastTransitions(vb[0], vb[1], vb[2]);
			nodes[i] = n;
		}
		return nodes;

	}
	public static Node[] generateNodes(int Nd, int Ts,int Tn, int Tb,WiFiState s,WiFiState n, WiFiState b){
		
		Node[] nodes = new Node[Nd];
		for(int i=0;i<Nd;i++){
			var nd = new Node(Ts,Tn,Tb);
			nd.setScanTransitions(s.getPs(), s.getPn(), s.getPb());
			nd.setNetworkTransitions(n.getPs(), n.getPn(), n.getPb());
			nd.setBroadcastTransitions(b.getPs(),b.getPn(),b.getPb());
			nodes[i] = nd;
		}
		return nodes;

	}
  public static void main(String[] args){
	ArrayList<WiFiState> res = ConfigReader.readConfigFile("config1.txt");
	for(var r:res){
		System.out.println(r);
	}
	int n_nodes = 20;
	var nodes = generateNodes(n_nodes, 120, 30, 100, res.get(0),res.get(1),res.get(2));		
		for(int i=0;i<n_nodes;i++){
			var n = nodes[i];
			var l = new Logger("./results/d"+i+"-result.txt");
			for(int k=0;k <10_000_000;k++){
				n.run();
				l.log(n.getCurrentState().toString());
			}
			l.dump(false);
			
		}		

	}
	
}