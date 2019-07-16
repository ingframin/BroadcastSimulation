import os
from threading import Thread

def filter_results(r):
    
    files = filter(lambda name: 'result' in name and 'r%d-'%r in name, os.listdir('.'))

    transmissions = [0 for i in range(10000000)]

    for fn in files:
        print(fn)
        f = open(fn)
        raw = f.read()
        f.close()
        dn = int(fn.replace('r%d-d'%r,'').replace('-result.txt',''))
        for i in range(len(raw)):
            if raw[i] =='B':
                transmissions[i] |= 2**dn

    dsn = [2**n for n in range(20)]
    fclean = open("r%d-clean.txt"%r,"w")
    for i in range(len(transmissions)):
        if transmissions[i] in dsn:
            fclean.write("%d;%d\n"%(i,transmissions[i]))
    fclean.close()

    fres = open('r%d-collisions.txt'%r,'w')
    for t in transmissions:
        fres.write(bin(t).replace('0b','-'))
    fres.close()
    


for i in range(21):
    filter_results(i)
    


