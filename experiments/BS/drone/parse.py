from timestamp import *

def read_data(filename):
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

if __name__=='__main__':
    data= read_data('drone.txt')
    sent = []
    received = []
    for d in data:
        if 'sent' in d['data']:
            sent.append(d)
        if 'D1' in d['data']:
            received.append(d)
        
    print(len(sent))
    print(len(received))
    print(len(received)/((data[-1]['T'] - data[0]['T']).toSeconds()))

        
