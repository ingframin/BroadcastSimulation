from timestamp import *
from geodesy import *

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
        
        strdata = ''.join(ls[4:-1])

        tsr = ls[-1].split()
        
        ts_rasp = TimeStamp(stamp = tsr[1])
        
        drone_data.append({'abs T':ts,'lon':lon,'lat':lat,'alt':alt,'data':strdata,'rasp T':ts_rasp})
    return drone_data

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

if __name__=='__main__':
    

    data= read_tower_data('tower.txt')
    sent = []
    received = []
    bdurs = []
    for d in data:
        try:
            if 'sent' in d['data']:
                sent.append(d)
            if 'D1' in d['data']:
                received.append(d)
            if 'b-dur' in d['data']:
                ds = d['data'].split(':')
                bdurs.append(int(ds[1][0:-5]))
                
        except:
            print(d)
            input()
        
    drone_data = read_drone_data('drone.txt')
    
    rvp = rssi_vs_position(drone_data)
    rvd = rssi_vs_distance(rvp)
    
    
    
    with open('rssi_vs_dist.txt','w') as f:
        for rd in rvd:
            print(f'{rd[0]};{rd[1]}',file = f)
        
        
    
