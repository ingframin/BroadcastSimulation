package sim.engine;
import java.util.Arrays;
import java.util.Random;

public abstract class State{
    public static final char states[] = {'S','B','N','I'};
    double[] transitions;
    char name;
    boolean idle;
    private Random r;
    
    public State(char name, double[] transitions){
        this.name = name;
        this.transitions = transitions.clone();
        idle = false;
        r = new Random();
    }

    public abstract char getCurrent();

    public char transition(){
        double rnd = r.nextDouble();
        int j = 0;
        for(int i=0;i<transitions.length;i++){
            double t = Arrays.stream(Arrays.copyOf(transitions, i+1)).sum();
            if(rnd < t){
                break;
            }
        }    
        return states[j];
    }
}