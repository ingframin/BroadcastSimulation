package sim.utils;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Logger {
    String path;
    ArrayList<char[]> logContent;

    public Logger(String path) {
        this.path = path;
        logContent = new ArrayList<>();

    }

    public Logger(String path, int size) {
        this.path = path;
        logContent = new ArrayList<>(size);

    }

    public void log(String txt) {
        logContent.add(txt.toCharArray());
    }

    public void log(char txt) {
        logContent.add(new char[] { txt });
    }

    public void log(char[] txt) {
        logContent.add(txt);
    }

    public void log(Object o) {
        logContent.add(String.valueOf(o).toCharArray());
    }

    public void dump(boolean append) {
        try (FileWriter fw = new FileWriter(path, append)) {
            BufferedWriter bf = new BufferedWriter(fw);
            for (var s : logContent) {

                bf.write(s);
            }
            logContent.clear();
            bf.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {
            System.out.println("Log " + path + "succesfully written");
        }
    }

    public void dump(String separator) {
        try (FileWriter fw = new FileWriter(path, true)) {
            BufferedWriter bf = new BufferedWriter(fw);
            bf.write(separator);
            for (var s : logContent) {

                bf.write(s);
            }
            logContent.clear();
            bf.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {

            System.out.println("Log " + path + "succesfully written");
        }
    }

    public void compactDump() {
        StringBuffer buffer = new StringBuffer();
        for (var s : logContent) {
            if (s[0] == 'N') {
                buffer.append("N,");
            } else if (s[0] == 'S') {
                buffer.append("S,");
            } else {
                int pos = 0;
                for (int i = 0; i < s.length; i++) {
                    if (s[i] == 'B') {
                        pos = i;
                        break;
                    }
                }
                buffer.append(pos);
                buffer.append("B,");

            }
        }
        try (FileWriter fw = new FileWriter(path, false)) {
            BufferedWriter bf = new BufferedWriter(fw);
            bf.write(buffer.toString());
            logContent.clear();
            bf.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        } finally {
            System.out.println("Log " + path + "succesfully written");
        }
    }

}