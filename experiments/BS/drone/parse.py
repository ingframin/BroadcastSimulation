from timestamp import *
import re
MSG = re.compile(r'D[0-9]+-.*')

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

    f = open('drone-1.txt')
    raw= f.readlines()
    f.close()
    nm = 0
    for l in raw:
        if 'D1' in l:
            nm+=1

    print(nm)
    

"""  data= read_data('drone-1.txt')
print(data)
sent = []
received = []
for d in data:
    try:
        if 'sent' in d['data']:
            sent.append(d)
        if 'D1' in d['data']:
            received.append(d)
    except:
        print(d)
print(len(sent))
print(len(received))
print(len(received)/((data[-1]['T'] - data[0]['T']).toSeconds()))

    
"""