package sim.main;
import sim.engine.*;


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
  public static void main(String[] args){
		int n_nodes = 20;
		var nodes = generateNodes(n_nodes, 120, 30, 100, new double[]{0.45,0.1,0.45}, new double[]{0.45,0.1,0.45}, new double[]{0.45,0.1,0.45});

		
			
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