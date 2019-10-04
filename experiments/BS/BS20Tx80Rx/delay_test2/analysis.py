from timestamp import *
import re
import numpy as np
from matplotlib import pyplot as plt
import scipy
import scipy.stats
import matplotlib
from threading import Thread

MSG = re.compile(r'D[0-9]+-.*\*')
SENT = re.compile(r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+')

def save(filename,data):
    with open(filename,'w') as fn:
        for d in data:
            print(d,file=fn)
            
def read_file(filename):
    with open(filename) as f:
        raw = f.readlines()
        return raw
    
def cleanup(line):
    return line.replace('(','').replace("'","").replace(')','').replace('b','').replace('\\t',',').replace('\\r\\n','').replace('"','').strip()
    
def read_data(raw):
    
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

def get_sent(lines):
    
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

def compute_ttx(raw):

    diff = []
  
    for line in raw:
        
        if 'dur' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[1].split(':')[1]
            d = float(s)
            diff.append(d)
            
    return diff

def scan_frequency(raw):
   
    scans = []
  
    for line in raw:
        if 'S' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            scans.append(ls[0])
    t0 = TimeStamp(scans[0]).toSeconds()
    t1 = TimeStamp(scans[-1]).toSeconds()
    return len(scans)/(t1-t0)
    
def analysis(res1,res2,n1,n2):
    rec = read_data(res2)
    
    tr = Thread(target=save,args=('received-%s.txt',rec))
    tr.start()
    sent = get_sent(res1)
    
    tr2 = Thread(target=save,args=('sent-%s.txt'%n1,sent))
    tr2.start()
      
    sent_set = set([s[1] for s in sent])
    rec_set = set([r[1].replace('*','') for r in rec])
    received = len(rec_set.intersection(sent_set))

    
    print('succ: ', received/len(sent))

    print('sent [msg/s]:', sent_frequency(sent))
    tr.join()
    tr2.join()

if __name__=='__main__':
    res1 = read_file('res-1.txt')
    res2 = read_file('res-2.txt')
    analysis(res1,res2,'res-1','res-2')
    analysis(res2,res1,'res2','res-1')
    diff1 = compute_ttx(res1)
    diff2 = compute_ttx(res2)
    print('scan freq(res-1): ',scan_frequency(res1))
    print('scan freq(res-2): ',scan_frequency(res2))
    print('Average Ttx (res-1): ',np.average(diff1)/1000)
    print('Average Ttx (res-2): ',np.average(diff2)/1000)
    print(np.std(diff1)/1000)
    print(np.std(diff2)/1000)
    plt.hist(diff1,histtype='step',color='red',density=True)
    plt.hist(diff2,histtype='step',color='green',density=True)
    plt.grid(True)
    plt.show()