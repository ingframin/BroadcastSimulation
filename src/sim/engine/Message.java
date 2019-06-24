package sim.engine;

public class Message{
    public final long ID;
    public final String data;
    
    private static long counter = 0;

    public Message(String d){
        ID = counter;
        counter++;
        data = d;

    }

    public boolean equals(Object o){
        if(o instanceof Message){
            var m = (Message) o;
            if(m.ID == ID && m.data.equals(data)){
                return true;
            }
        }
        return false;
    }

    public String toString(){

        return ID+"\t"+data+"\n";

    }

    public int compareTo(Object o){
        if(o instanceof Message){
            var m = (Message) o;
            if(m.ID < ID){
                return -1;
            }
            if(m.ID > ID){
                return 1;
            }
        }
        return 0;
    }

    public static void resetCounter(){
        counter = 0;
    }
}