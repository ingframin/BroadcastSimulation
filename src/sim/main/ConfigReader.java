package sim.main;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import sim.engine.WiFiState;

import java.util.ArrayList;

final class ConfigReader{

    private ConfigReader(){

    }
    
    public static ArrayList<WiFiState> readConfigFile(String filename){
        ArrayList<WiFiState> res = new ArrayList<>();
        try{
            File file = new File(filename);
            Scanner s = new Scanner(file);
            
            while(s.hasNextLine()){
                String tmp = s.nextLine();
                String [] split = tmp.split(";");
                res.add(new WiFiState(split[0].charAt(0),
                    Double.valueOf(split[1]),
                    Double.valueOf(split[2]),
                    Double.valueOf(split[3])));
            }


        }
        catch(Exception e){
            e.printStackTrace();
        }
        
        return res;


    }

}