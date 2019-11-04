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


def analysis(res1,res2,n1,n2):
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

def duty_cycle(res,dtx,drx):
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
    
if __name__=='__main__':

    res = []
    n = 2

    for i in range(1,n+1):
          
        res.append(read_file('res-%d.txt'%i))
    

    h_xy = []
    s_xy = []
    
    
    for x in range(n):
        for y in range(n):
            if x != y:
                h,s = analysis(res[x],res[y],'res-%d'%x,'res-%d'%y)
                h_xy.append(h)
                s_xy.append(s)

    print('----------------------------------------')
    print('Average success rate: ',np.average(s_xy),'%')
    print('----------------------------------------')
    
    diff_tx = []
    diff_rx = []
    for i in range(n):
        diff_tx.append(compute_ttx(res[i]))
        diff_rx.append(compute_trx(res[i]))
        print('scan freq(res-%d): '%i,scan_frequency(res[i]))
        
       
        print('Average Ttx (res-%i): '%i,np.average(diff_tx[i])/1000)
        print('Average Trx (res-%i): '%i,np.average(diff_rx[i])/1000)
        duty_cycle(res[i],diff_tx[i],diff_rx[i])
        
        print('----------------------------------------')
    
    
    
    for h in h_xy:
        plt.hist(h,bins=30,density=True,histtype='step')
    
    plt.grid(True)
    plt.show()

    for dtx in diff_tx:
        plt.hist(dtx,bins=100,histtype='step',density=True)
   
    plt.grid(True)
    plt.savefig('dist_Tx.pdf',dpi=300,)
    plt.show()

    
    for drx in diff_rx:
        plt.hist(drx,bins=100,histtype='step',density=True)
    
    plt.grid(True)
    plt.show()
