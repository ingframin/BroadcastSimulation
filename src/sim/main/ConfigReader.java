package sim.main;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;

public final class ConfigReader{

    private ConfigReader(){

    }

    public static ArrayList<Double> readConfigFile(String filename){
        ArrayList<Double> res = new ArrayList<>();
        try{
            File file = new File(filename);
            Scanner s = new Scanner(file);
            
            while(s.hasNextLine()){
                String tmp = s.nextLine();
                String [] split = tmp.split(";");
                for(var n:split){
                    res.add(Double.parseDouble(n));
                }
            }


        }
        catch(Exception e){
            e.printStackTrace();
        }
        
        return res;


    }

}