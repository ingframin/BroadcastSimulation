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
                                
            #try:
            ls = clean.split(',')
            ts = TimeStamp(ls[0])
            ssid_str = ssid[0][1:18]
            #rssi = int(ls[2][5:])
            rec.append((ts,ssid_str))
           # except:
            #    print(clean)
                
                
    return rec

def get_sent(lines):
    
    sent = []
    for line in lines:
        if 'B-' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[2].replace('*','').replace('sent:','').strip()
            sent.append((ls[0],s))
    return sent
def get_net(lines):
    
    net = []
    for line in lines:
        if 'N-' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            #s = ls[2].replace('*','').replace('sent:','').strip()
            net.append(ls)
    return net

def sent_frequency(sent):
    t0 = TimeStamp(sent[0][0]).toSeconds()
    t1 = TimeStamp(sent[-1][0]).toSeconds()
    return len(sent)/(t1-t0)

def net_frequency(net):
    t0 = TimeStamp(net[0][0]).toSeconds()
    t1 = TimeStamp(net[-1][0]).toSeconds()
    return len(net)/(t1-t0)

def compute_ttx(raw):

    diff = []
  
    for line in raw:
        
        if 'B-dur' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[1].split(':')[1]
            t = s.split(';')
            d = float(t[0])
            diff.append(d)
            
    return diff

def compute_trx(raw):

    diff = []
  
    for line in raw:
        
        if 'S-dur' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[1].split(':')[1]
            t = s.split(';')
            d = float(t[0])
            diff.append(d)
            
    return diff

def compute_tn(raw):

    diff = []
  
    for line in raw:
        
        if 'N-dur' in line:
            clean = cleanup(line)
            ls = clean.split(',')
            s = ls[1].split(':')[1]
            t = s.split(';')
            d = float(t[0])
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
    net = get_net(res1)
    print(len(sent))
    tr2 = Thread(target=save,args=('sent-%s.txt'%n1,sent))
    tr2.start()
      
    sent_set = set([s[1] for s in sent])
    rec_set = set([r[1].replace('*','') for r in rec])
    received = len(rec_set.intersection(sent_set))
    t0 = rec[0][0].toSeconds()
    t1 = rec[-1][0].toSeconds()
    
    print('Reception rate: ',len(rec)/(t1-t0))
    
    print('Success: %.6f%%'%(100*len(rec)/len(sent)))

    print('Transmission rate [msg/s]:', sent_frequency(sent))
    print('Networking rate [packet/s]:',net_frequency(net))
            
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
    return hist, 100*len(rec)/len(sent)

def duty_cycle(res,dtx,drx,dn):
    B = 0
    S = 0
    N = 0
    for line in res:
        if 'B' in line:
            B+=1
        if 'S' in line:
            S+=1
        if 'N' in line:
            N+=1
            
    Btime = B*np.average(dtx)/1000
    Stime = S*np.average(drx)/1000
    Ntime = N*np.average(dn)/1000
    print('B(%): ',100*Btime/(Btime+Stime+Ntime))
    print('S(%): ',100*Stime/(Btime+Stime+Ntime))
    print('N(%): ',100*Ntime/(Btime+Stime+Ntime))
    
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
    diff_n = []
    for i in range(n):
        diff_tx.append(compute_ttx(res[i]))
        diff_rx.append(compute_trx(res[i]))
        diff_n.append(compute_tn(res[i]))
        print('scan freq(res-%d): '%i,scan_frequency(res[i]))
        
       
        print('Average Ttx (res-%i): '%i,np.average(diff_tx[i])/1000)
        print('Average Trx (res-%i): '%i,np.average(diff_rx[i])/1000)
        print('Average Tn (res-%i): '%i,np.average(diff_n[i])/1000)
        duty_cycle(res[i],diff_tx[i],diff_rx[i],diff_n[i])
        
        print('----------------------------------------')
    
    #plt.rcParams["figure.figsize"] = (20,10)
    
##    for h in h_xy:
##        plt.hist(h,density=True,histtype='step',align='left',rwidth=0.8)
    xy = plt.hist(h_xy[0],bins=18,density=True,histtype='step',align='left',rwidth=0.8)
    xy2 = plt.hist(h_xy[1],bins=15,density=True,histtype='step',align='left',rwidth=0.8)
    plt.close()
    plt.plot(xy[0],'-Dr',markersize=20)
    plt.plot(xy2[0],'-Dg',markersize=20)
    #plt.axis([0,11,0,0.25])
    plt.xlabel('Throughput [msg/s]',fontsize=20)
    plt.ylabel('PDF',fontsize=20)
    plt.xticks(range(19),fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.savefig('rx_dist.pdf',dpi=300,bbox_inches='tight')
    plt.show()

##    #for dtx in diff_tx:
##    plt.hist(diff_tx[0],bins=32,histtype='bar',density=True)
##    plt.axis([24000,40000,0,6e-4])
##    plt.yticks(ticks=[x*1e-4 for x in range(0,7)],labels=["%dE-4"%x for x in range(0,7)],fontsize=20)
##    plt.xticks(range(24000,40000,1000),labels=[x/10.0 for x in range(240,400,10)],fontsize=20)
##    plt.xlabel('$T_{Tx}$ duration[ms]',fontsize=20)
##    plt.ylabel('PDF',fontsize=20)
##    plt.grid(True)
##    plt.savefig('dist_Tx.pdf',dpi=300,bbox_inches='tight')
##    plt.show()
##
##    
##    for drx in diff_rx:
##        plt.hist(drx,bins=100,histtype='step',density=True)
##    
##    plt.grid(True)
##    plt.show()
