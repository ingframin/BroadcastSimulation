from timestamp import *
import re
import numpy as np
from matplotlib import pyplot as plt
import scipy
import scipy.stats
import matplotlib


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

def sent_frequency(sent):
    t0 = TimeStamp(sent[0][0]).toSeconds()
    t1 = TimeStamp(sent[-1][0]).toSeconds()
    return len(sent)/(t1-t0)

def compute_ttx(filename):
    with open(filename) as rf:
        raw = rf.readlines()
        diff = []
        t0 = None
        t1 = None
        
        for line in raw:
            clean = cleanup(line)
            ls = clean.split(',')
            if '>' in ls[1]:
                t0= TimeStamp(ls[0])
            if 'B' in ls[1]:
                t1 = TimeStamp(ls[0])
            if t0 is not None and t1 is not None:
                d = t1.toSeconds() - t0.toSeconds()
                if d > 0.1:
                    print(d)
                    print(line)
                diff.append(d)
                t1 = None
                t0 = None
        return diff
            
def analysis(res1,res2):
    rec = read_data(res2)
    with open('received-%s.txt'%res2,'w') as rf:
        for r in rec:
            print(r,file=rf)
            
    sent = get_sent(res1)
    with open('sent-%s.txt'%res1,'w') as sf:
        for s in sent:
            print(s,file=sf)
    
    received = 0
    rec_set = set([r[1] for r in rec])
    for r in rec_set:
        
        if r in sent:
            received+=1
    
    print('succ: ', len(rec)/len(sent))

    print('sent [msg/s]:', sent_frequency(sent))


if __name__=='__main__':

    analysis('res-1.txt','res-2.txt')
    analysis('res-2.txt','res-1.txt')
    diff1 = compute_ttx('res-1.txt')
    diff2 = compute_ttx('res-2.txt')
    print('Average Ttx (res-1): ',sum(diff1)/len(diff1))
    print('Average Ttx (res-2): ',sum(diff2)/len(diff2))
    print(np.std(diff1))
    print(np.std(diff2))
    plt.hist(diff1)
    plt.show()
