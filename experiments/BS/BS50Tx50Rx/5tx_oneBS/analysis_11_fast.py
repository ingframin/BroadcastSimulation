from timestamp import *
import re
import numpy as np
from matplotlib import pyplot as plt
import scipy
import scipy.stats
import matplotlib
from threading import Thread
from datetime import datetime
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
        
        if 'dur' in line and 's-' not in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[1].split(':')[1]
            d = float(s)
            diff.append(d)
            
    return diff

def compute_trx(raw):

    diff = []
  
    for line in raw:
        
        if 's-dur' in line:
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


def analysis(res1,res2,n1,n2,f=None):
    rec = read_data(res2)
    
    tr = Thread(target=save,args=('received-%s.txt'%n2,rec))
    tr.start()
    sent = get_sent(res1)
    
    tr2 = Thread(target=save,args=('sent-%s.txt'%n1,sent))
    tr2.start()
      
    sent_set = set([s[1] for s in sent])
    rec_set = set([r[1].replace('*','') for r in rec])
    received = len(rec_set.intersection(sent_set))
    t0 = rec[0][0].toSeconds()
    t1 = rec[-1][0].toSeconds()
    
    print('Reception rate: ',len(rec)/(t1-t0))
    
    print('Success: %.6f%%'%(100*received/len(sent)))

    print('Transmission rate [msg/s]:', sent_frequency(sent))
    if f is not None:
        print('----------------------------------------',file=f)
        print('Results for: %s,%s'%(n1,n2),file=f)
        print('Reception rate: ',len(rec)/(t1-t0),file=f)
    
        print('Success: %.6f%%'%(100*received/len(sent)),file=f)

        print('Transmission rate [msg/s]:', sent_frequency(sent),file=f)
            
    wnd = {}
    wnd[0] = []
    tref = rec[0][0].toSeconds()
    i = 0
    for r in rec:
        if r[0].toSeconds() - tref < 1:
            wnd[i].append(r)
        else:
            tref = r[0].toSeconds()
            i += 1
            wnd[i] = []
    hist = []
    for w in wnd:
        hist.append(len(wnd[w]))
    tr.join()
    tr2.join()
    return hist, 100*received/len(sent)

def duty_cycle(res,dtx,drx,f=None):
    B = 0
    S = 0
    for line in res:
        if '>' in line:
            B+=1
        if 'S' in line:
            S+=1
    Btime = B*np.average(dtx)/1000
    Stime = S*np.average(drx)/1000
    print('B(%): ',100*Btime/(Btime+Stime))
    print('S(%): ',100*Stime/(Btime+Stime))
    if f is not None:
        print('B(%): ',100*Btime/(Btime+Stime),file=f)
        print('S(%): ',100*Stime/(Btime+Stime),file=f)
    
if __name__=='__main__':

    res = read_file('res-20Mps.txt')

    
    trx = compute_trx(res)
    plt.hist(trx,bins=100,histtype='step',density=True)
    plt.show()
    rec = [cleanup(l) for l in res if 'rssi' in l]
    r0 = []
    print(sum(trx)/(1000*len(trx)),'ms')
    for r in rec:
        if 'D1' in r:
            r0.append(r)
    dts = []
    for i in range(1,len(r0)):
        ts0 = r0[i-1].split(',')[0]
        t0 = datetime.strptime(ts0,"%H:%M:%S.%f")
        ts1 = r0[i].split(',')[0]
        t1 = datetime.strptime(ts1,"%H:%M:%S.%f")
        dt = (t1-t0).total_seconds()
        if dt > 10:
            continue
        dts.append(dt)
        
    print(len(r0)/sum(dts),'msg/s')

    counters = []
    
    for line in res:
        
        if "S" in line:
            counters.append(0)
            
        elif 's-dur' not in line:
            counters[-1] += 1

    cnt = list(filter(lambda x: x>0,counters))
    
    print(sum(cnt)/len(cnt),'msg/scan')
            
        
