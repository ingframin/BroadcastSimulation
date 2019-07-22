import os
from threading import Thread

def filter_results(r):
    
    files = filter(lambda name: 'result' in name and 'r%d-'%r in name, os.listdir('.'))

    transmissions = [[] for i in range(10000000)]

    for fn in files:
        print(fn)
        f = open(fn)
        raw = f.read()
        f.close()
        dn = fn.replace('r%d-d'%r,'').replace('-result.txt','')
        for i in range(len(raw)):
            if raw[i] =='B':
                transmissions[i].append(dn)

    fclean = open("r%d-clean.txt"%r,"w")
    for i in range(len(transmissions)):
        if len(transmissions[i])==1:
            fclean.write("%d;%s\n"%(i,transmissions[i][0]))
    fclean.close()

    fres = open('r%d-collisions.txt'%r,'w')
    for t in transmissions:
        fres.write('\t'.join(transmissions[i])+'\n')
    fres.close()
    


for i in range(21):
    filter_results(i)
    


