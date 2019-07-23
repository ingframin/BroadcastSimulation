import os
from threading import Thread

def filter_results(r):
    
    files = filter(lambda name: 'result' in name and 'r%d-'%r in name, os.listdir('.'))

    transmissions = {}

    for fn in files:
        print(fn)
        f = open(fn)
        raw = f.read()
        f.close()
        dn = fn.replace('r%d-d'%r,'').replace('-result.txt','')
        for i in range(len(raw)):
            if raw[i] =='B':
                try:
                    transmissions[i].append(dn)
                except:
                    transmissions[i] = [dn]

    fclean = open("r%d-clean.txt"%r,"w")
    for i in transmissions:
        if len(transmissions[i])==1:
            fclean.write("%d;%s\n"%(i,transmissions[i][0]))
    fclean.close()

    fres = open('r%d-collisions.txt'%r,'w')
    for t in transmissions:
        fres.write('\t'.join(transmissions[t])+'\n')
    fres.close()
    


for i in range(21):
    filter_results(i)
    


