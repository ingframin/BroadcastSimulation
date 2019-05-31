package sim.engine;


public class WiFiState{

    double Ps,Pb,Pn;
    char name;
    static final char[] names = new char[]{'S','B','N'};

    public WiFiState(WiFiState s){
        Ps = s.Ps;
        Pb = s.Pb;
        Pn = s.Pn;
        name = s.name;
    }
    public WiFiState(){
        Ps = 0.33;
        Pn = 0.33;
        Pb = 0.33;
        int n = (int)Math.round((names.length-1) * Math.random());
        this.name=names[n];
        
    }
    public WiFiState(char name, double ps, double pn, double pb){
        Ps = Math.abs(ps);
        Pn = Math.abs(pn);
        Pb = Math.abs(pb);
        this.name=name;
        
    }
    public WiFiState(char name, double[] Tv){
        Ps = Math.abs(Tv[0]);
        Pn = Math.abs(Tv[1]);
        Pb = Math.abs(Tv[2]);
        this.name=name;
        
    }

    public void setPs(double ps){
        Ps = Math.abs(ps);
    }
    public void setPb(double pb){
        Pb = Math.abs(pb);
    }
    public void setPn(double pn){
        Ps = Math.abs(pn);
    }

    public double getPs(){
        return Ps;
    }
    public double getPn(){
        return Pn;
    }
    public double getPb(){
        return Pb;
    }

    public boolean equals(Object o){
        if(o instanceof WiFiState){
            WiFiState ws = (WiFiState)o;
            if(ws.Pb==this.Pb&&ws.Ps==this.Ps&&ws.Pn==this.Pn){
                if(ws.name == this.name){
                    return true;
                }
            }
        }
        return false;
    }

    public String toString(){
        return String.valueOf(name);
    }
}