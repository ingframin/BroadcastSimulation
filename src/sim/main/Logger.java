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
    public void log(char txt){
        logContent.add(String.valueOf(txt));
    }

    public void log(Object o){
        logContent.add(String.valueOf(o));
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
    public void dump(String separator){
        try(FileWriter fw = new FileWriter(path,true)){
            fw.append(separator);
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