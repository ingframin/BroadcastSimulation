package sim.main;
import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

final class ConfigReader{

    private ConfigReader(){}
    
    public static ArrayList<WiFiConfig> readConfigFile(String filename){
        //Improve parsing:
        //- Add read of multiple configurations

        ArrayList<WiFiConfig> res = new ArrayList<>();
        File file = new File(filename);
        try(Scanner s = new Scanner(file)){
            char n;
            double[] Ps = null;
            double[] Pn = null;
            double[] Pb = null;

            while(s.hasNextLine()){
                String tmp = s.nextLine();
                String [] split = tmp.split(";");
                n = split[0].charAt(0);
                switch(n){
                    case 'S':
                        Ps = new double[]{Double.valueOf(split[1]),Double.valueOf(split[2]),Double.valueOf(split[3])};
                        break;
                    case 'N':
                        Pn = new double[]{Double.valueOf(split[1]),Double.valueOf(split[2]),Double.valueOf(split[3])};
                        break;
                    case 'B':
                        Pb = new double[]{Double.valueOf(split[1]),Double.valueOf(split[2]),Double.valueOf(split[3])};
                        break;
                }
            }
            if(Ps != null && Pn != null && Pb != null){
                res.add(new WiFiConfig(Ps,Pn,Pb));
            }
            else{
                throw new Exception("Incomplete configuration file");
            }
            
        }
        catch(Exception e){
            e.printStackTrace();
        }
      
        return res;


    }

}