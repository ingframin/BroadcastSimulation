from math import e, factorial,log, gamma, sqrt
from matplotlib import pyplot as pt

Ps = {}

for i in range(1,20):
    Ps[i] = []
    for k in range(25):
        v = e**(k*log(i)-i-log(gamma((k+1))))
        Ps[i].append(v)
    


for i in range(1,20):
    pt.plot(range(25),Ps[i])

pt.axis([0,25,0,1.0])
pt.xticks(range(25), [str(int(n)) for n in range(25)])
pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
pt.ylabel(r'P(k-messages-received)')
pt.grid(True)

pt.show()