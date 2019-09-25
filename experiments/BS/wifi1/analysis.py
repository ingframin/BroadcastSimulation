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
                sent.append(s)
        return sent
            

if __name__=='__main__':
    
    rec =read_data('res-2.txt')
    with open('received.txt','w') as rf:
        for r in rec:
            print(r,file=rf)
            
    sent = get_sent('res-2.txt')
    with open('sent.txt','w') as sf:
        for s in sent:
            print(s,file=sf)
    
    received = 0
    
    for r in rec:
        
        if r[1] in sent:
            received+=1
    print(len(sent))
    print(len(rec))
