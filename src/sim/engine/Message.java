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
}