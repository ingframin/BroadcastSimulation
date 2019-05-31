package sim.main;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Logger{
    String path;
    ArrayList<String> logContent;
    
    public Logger(String path){
        this.path = path;
        logContent = new ArrayList<>();

    }

    public void log(String txt){
        logContent.add(txt);
    }

    public void dump(boolean append){
        try(FileWriter fw = new FileWriter(path,append)){
            for(var s: logContent){
                fw.append(s);
            }
            logContent.clear();
        }
        catch(IOException ioe){
            ioe.printStackTrace();
        }
    }
}