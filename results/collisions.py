from analysis import *
import os

files = filter(lambda name: 'r1' in name, os.listdir('.'))

transmissions = {}

for fn in files:
    f = open(fn)
    raw = f.read()
    f.close()
    dn = fn.replace('r1-','').replace('-result.txt','')
    for i in range(len(raw)):
        if raw[i] == 'B':
            try:
                transmissions[i].append((dn,i))
            except:
                transmissions[i] = [(dn,i)]

input()