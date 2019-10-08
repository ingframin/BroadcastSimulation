from timestamp import *
import re
MSG = re.compile(r'D[0-9]+-.*\*')
SENT = re.compile(r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+')

def cleanup(line):
    return line.replace('(','').replace("'","").replace(')','').replace('b','').replace('\\t',',').replace('\\r\\n','').replace('"','').strip()
    
def read_data(filename):
    with open(filename) as rf:
        raw = rf.readlines()
        rec = []
        
        for line in raw:
            clean = cleanup(line)
            
            ssid = MSG.findall(clean)
            
            if len(ssid) > 0:
                                    
                try:
                    ls = clean.split(',')
                    ts = TimeStamp(ls[0])
                    ssid_str = ssid[0][1:18]
                    rssi = int(ls[2][5:])
                    rec.append((ts,ssid_str,rssi))
                except:
                    print(clean)
                    
                    
        return rec

def get_sent(filename):
    with open(filename) as fs:
        lines = fs.readlines()
        sent = []
        for line in lines:
            if 'sent' in line:
                clean = cleanup(line)
                ls = clean.split(',')
                s = ls[2].replace('*','').replace('sent:','').strip()
                sent.append((ls[0],s))
        return sent
            

if __name__=='__main__':
    
    sent = get_sent('res-2.txt')
    with open('sent.txt','w') as sf:
        for s in sent:
            print(s,file=sf)
    diff = []
    for i in range(1,len(sent)):
        s1 = sent[i][0]
        s0 = sent[i-1][0]
        tns = TimeStamp(s1)-TimeStamp(s0)
        diff.append(tns.toSeconds())
    print(sum(diff)/len(diff))
