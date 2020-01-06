from timestamp import *
from geodesy import *
from matplotlib import pyplot as pt
from math import log
import re
MSG = re.compile(r'D[0-9]+-.*')

def read_tower_data(filename):
    with open(filename) as f:
        raw = f.readlines()

        points = []

        for line in raw:
            cl = line.replace("b'",'').replace("'",'').replace('(','').replace('{','').replace(')','').replace('}','')
            ls = cl.split(',')
            p = {}
            for field in ls:
                fs = field.split(':')
                try:

                    if 'T' in fs[0]:
                        p['T'] = TimeStamp(h=int(fs[1]),m=int(fs[2]),s=float(fs[3]))
                        continue
                except:
                    print(fs)
                try:
                    p[fs[0]] = float(fs[1])
                except:
                    p['data'] = field

            points.append(p)
        
        return points


def read_drone_data(filename):
    dfile = open(filename)
    draw = dfile.readlines()
    dfile.close()
    drone_data = []
    
    for line in draw:
        
        lclean = line.replace("b'",'').replace("'",'').replace('(','').replace('{','').replace(')','').replace('}','')
        ls = lclean.split(',')
        
        if ls[0] == '0':
            continue
        
        
        time_str = ls[0].split()[1]
        ts = TimeStamp(stamp=time_str)

        lat = float(ls[1])
        lon = float(ls[2])
        alt = float(ls[3])
        if alt < 35:
            continue
        
        strdata = ''.join(ls[4:-1])

        tsr = ls[-1].split()
        
        ts_rasp = TimeStamp(stamp = tsr[1])
        
        drone_data.append({'abs T':ts,'lon':lon,'lat':lat,'alt':alt,'data':strdata,'rasp T':ts_rasp})
    return drone_data

def cluster(data,i=0):
    clusters = {}
    ind = 0
    for rd in data:
        if rd[i] < 100:
            ind = 100
        elif rd[i] >= 100 and rd[i]<200:
            ind = 200
        elif rd[i] >=200 and rd[i] <300:
            ind = 300
        elif rd[i] >= 300 and rd[i] <400:
            ind = 400
        elif rd[i]>=400 and rd[i] <500:
            ind = 500
        elif rd[i]>=500 and rd[i] <600:
            ind = 600
        elif rd[i] >=600 and rd[i] <700:
            ind = 700
        elif rd[i] >= 700 and rd[0]<800:
            ind = 800
        elif rd[i] >=800 and rd[i] < 850:
            ind = 850
        elif rd[i]>=850 and rd[i]<890:
            ind =900
        elif rd[i] >=890:
            ind = 950

        try:
            clusters[ind][0].append(rd[0])
            clusters[ind][1].append(rd[1])
        except:
            clusters[ind] = [[rd[0]],[rd[1]]]
    return clusters

def rssi_vs_position(data):
    rvp = []
    for d in data:
        if 'rssi' in d['data']:
            ds = d['data'].split('t')
            try:
                rp = (d['lat'],d['lon'],d['alt'],int(ds[1].split(':')[1][0:-4]))
                rvp.append(rp)
            except:
                pass
    return rvp


def rssi_vs_distance(rvp,ref=(50.86227366666667, 4.685484, 46.2)):
    rvd = []
    for rp in rvp:
        d = haversine(ref[0],rp[0],ref[1],rp[1])
        rvd.append((d,rp[3]))

    rvd.sort()
    return rvd

def received(data):
    rec = []
    for d in data:
        if 'D' in d['data']:
            rec.append(d)
    return rec

def msg_vs_distance(rec,ref=(50.86227366666667, 4.685484, 46.2)):
    
    mvd = []
    for r in rec:
        d = haversine(ref[0],r['lat'],ref[1],r['lon'])
        mvd.append((d,r['rasp T']))

    mvd.sort()
    return mvd
    
            
if __name__=='__main__':
    
    dd = []
    for i in range(1,13):
        dd += read_drone_data('log%d.txt'%i)
    
    rvp = rssi_vs_position(dd)
    rvd = rssi_vs_distance(rvp)

    
    clusters = cluster(rvd)
    
    res = []
    for k in clusters:
        dist = sum(clusters[k][0])/len(clusters[k][0])
        rssi = sum(clusters[k][1])/len(clusters[k][1])
        res.append((dist,rssi))
        
    #avg values
    d = [x[0] for x in res]
    r = [x[1] for x in res]

    #path loss
    pl = [19.5-3.55-10*2.118*log(x/0.0147,10) for x in d]
    

    #points
    rssi = [p[1] for p in rvd]
    dist = [p[0] for p in rvd]
    pt.rcParams['figure.figsize'] = 15, 10
    pt.grid(True)
    pt.plot(dist,rssi,'o',markersize=5,label="Measurement")
    pt.plot(d,pl,'g',linewidth=3.0,label="$P_{t}-K-10\gamma log_{10}(d/d_{0})$")
    pt.plot(d,r,'r*',markersize=16, label = "Average")
    pt.text(700,-60,"$Pt=19.5dBm$,$K=\lambda/(4\pi\d_{0})=-3.55$,\n$d_{0}=2*D/\lambda = 0.0147$,$\gamma=2.118$")
    pt.legend()
    
    pt.show()
    with open('rvd.txt','w') as f:
        for d,r in res:
            
            print(f'{d};{r}',file = f)
    
    with open('rssi_vs_dist.txt','w') as f:
        for rd in rvd:
            print(f'{rd[0]};{rd[1]}',file = f)

    rec = received(dd)
    mvd = msg_vs_distance(rec)
   
    cls = cluster(mvd)
    rate = []
    distance = []
    for k in cls:
        d = sum(clusters[k][0])/len(clusters[k][0])
        r = (clusters[k][1][-1]-clusters[k][1][0])/len(clusters[k][1])
        rate.append(r)
        distance.append(d)

    pt.plot(distance,rate)
    pt.show()
        
    
    
    
            
        
        
    
