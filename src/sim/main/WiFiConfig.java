package sim.main;


public class WiFiConfig{

    public final double[] Vs,Vb,Vn;
        
    public WiFiConfig(WiFiConfig s){
        Vs = s.Vs.clone();
        Vn = s.Vn.clone();
        Vb = s.Vb.clone();
    }
    
    public WiFiConfig(double[] ps, double[] pn, double[] pb){
        Vs = ps.clone();
        Vn = pn.clone();
        Vb = pb.clone();
            
    }
    
}