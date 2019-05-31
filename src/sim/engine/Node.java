package sim.engine;

import java.util.Random;

public class Node {
	WiFiState current;
	Random r;
	static long id_counter = 0;
	long ID;
	int timer;
	int Trx,Ttx,Tn;
	double[] Vs;
	double[] Vb;
	double[] Vn;

	public Node(int Trx, int Tn, int Ttx){
		current = new WiFiState();
		r = new Random();
		ID = id_counter;
		id_counter++;
		timer = 0;
		this.Trx = Trx;
		this.Ttx = Ttx;
		this.Tn = Tn;
		Vs = new double[]{0.3,0.4,0.3};
		Vn = new double[]{0.3,0.4,0.3};
		Vb = new double[]{0.3,0.4,0.3};
	}

	public void run(){
		switch(current.name){
			case 'S':
				if(timer < Trx){
					timer++;
					return;
				}
				break;
			case 'B':
				if(timer < Ttx){
					timer++;
					return;
				}
				break;
			case 'N':
				if(timer < Tn){
					timer++;
					return;
				}
				break;
		}
		timer = 0;
		double thr1 = current.Ps;
		double thr2 = current.Pb+thr1;
		double v = r.nextDouble();
		
		if(v < thr1){
			current.name = 'S';
			current.Ps = Vs[0];
			current.Pn = Vs[1];
			current.Pb = Vs[2];
		}
		else if(v < thr2){
			current.name = 'B';
			current.Ps = Vb[0];
			current.Pn = Vb[1];
			current.Pb = Vb[2];
		}
		else{
			current.name = 'N';
			current.Ps = Vn[0];
			current.Pn = Vn[1];
			current.Pb = Vn[2];
		}
		
	}

	public WiFiState getCurrentState(){
		return new WiFiState(current);
	}

	public long getID(){
		return ID;
	}

	public void setScanTransitions(double Pss, double Psn, double Psb){
		Vs[0] = Pss;
		Vs[1] = Psn;
		Vs[2] = Psb;
	}
	public void setBroadcastTransitions(double Pbs, double Pbn, double Pbb){
		Vb[0] = Pbs;
		Vb[1] = Pbn;
		Vb[2] = Pbb;
	}
	public void setNetworkTransitions(double Pns, double Pnn, double Pnb){
		Vn[0] = Pns;
		Vn[1] = Pnn;
		Vn[2] = Pnb;
	}
	
}

