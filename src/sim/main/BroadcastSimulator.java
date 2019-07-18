package sim.main;

import sim.engine.*;
import static sim.utils.ConfigReader.*;
import sim.utils.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.stream.Stream;

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

	public static void run(String runID, Node[] nodes, int points){
		for(int i=0;i<nodes.length;i++){
			var n = nodes[i];
			var l = new Logger("./results/r"+runID+"-d"+i+"-result.txt");
			var log_m = new Logger("./results/m"+runID+"-d"+i+"-result.txt");
			boolean flag = false;
			for(int k=0 ; k < points ; k++){
				n.run();
				char s= n.getCurrentState();
				l.log(s);
				if(s != 'B'){
					flag = false;
				}
				/*if(s == 'B' && !flag){
					var msg = new Message(String.valueOf(k));
					log_m.log(msg);
					flag = true;
				}*/
				
			}
			Message.resetCounter();
			l.dump(false);
			log_m.dump(false);
		}		
	}

	
	
	public static void main(String[] args){
	
		int n_nodes = 20;
		final int points;
				
		if(args.length > 0){
			points = Integer.parseInt(args[0]);
		}
		else{
			points = 10_000_000;
		}
		System.out.println("Points: "+points);
		try (Stream<Path> walk = Files.walk(Paths.get("."))) {

			var result = walk.filter(Files::isRegularFile).map(x -> x.toString()).filter((fn)->fn.matches("(.*)config[0-9]+(.*)")).collect(Collectors.toList());

			result.forEach((fn)->{
				var n = fn.replaceAll("\\D+","");
				System.out.println("config"+n+".txt");
				try{
					var config = readConfigFile("config"+n+".txt");
					var nodes = generateNodes(n_nodes, config.Trx, config.Tn, config.Ttx, config.Vs,config.Vn,config.Vb);
					run(n,nodes,points);
				}
				catch(Exception e){
					System.out.println(e.getMessage());
				}
	
			});

		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
		
	}
	
}