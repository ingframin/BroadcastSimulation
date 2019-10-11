package sim.utils;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Logger {
    String path;
    StringBuffer logContent;

    public Logger(String path) {
        this.path = path;
        logContent = new StringBuffer();

    }

    public Logger(String path, int size) {
        this.path = path;
        logContent = new StringBuffer(size);

    }

    public void log(String txt) {
        logContent.append(txt);
    }

    public void log(char txt) {
        logContent.append(new char[] { txt });
    }

    public void log(char[] txt) {
        logContent.append(txt);
    }

    public void log(Object o) {
        logContent.append(String.valueOf(o));
    }

    public void dump(boolean append) {
        try (FileWriter fw = new FileWriter(path, append)) {
            BufferedWriter bf = new BufferedWriter(fw);
            bf.write(logContent.toString());
            bf.close();
            logContent.delete(0, logContent.length());
            logContent.setLength(0);
            System.gc();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {
            System.out.println("Log " + path + "succesfully written");

        }
    }

}