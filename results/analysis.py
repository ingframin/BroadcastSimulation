from math import e, factorial,log, gamma
from matplotlib import pyplot as pt
f1 = open("d0-result.txt")
raw1 = f1.read()
f1.close()

f2 = open("d1-result.txt")
raw2 = f2.read()
f2.close()

f3 = open("d2-result.txt")
raw3 = f3.read()
f3.close()

good = 0
b1 = []
b2 = []
b3 = []
s1 = []
for i in range(len(raw1)):
    if raw1[i] == 'B':
        b1.append(i)
    if raw2[i] == 'B':
        b2.append('B')
    if raw3[i] == 'B':
        b3.append('B')
    if raw1[i] == 'S':
        s1.append(i)

    
print(len(b1)/len(raw1))
print(len(b2)/len(raw1))
print(len(b3)/len(raw1))
l1 = len(b1)/len(raw1)
l2 = len(b2)/len(raw1)
l3 = len(b3)/len(raw1)
ls = len(s1)*120/len(raw1)
pv1 = []
pv2 = []
pv3 = []
ps = []
for k in range(300):
    P1 = e**(k*log(l1*30)-l1*30-log(gamma(k+1)))
    P2 = e**(k*log(l2*30)-l2*30-log(gamma(k+1)))
    P3 = e**(k*log(l3*30)-l3*30-log(gamma(k+1)))
    Ps = e**(k*log(ls*120)-ls*120-log(gamma(k+1)))
    #print(gamma(k+1))
    #input()
    pv1.append(P1)
    pv2.append(P2)
    pv3.append(P3)
    ps.append(Ps)


pt.plot(range(300),pv1,'r',range(300),pv2,'b',range(300),pv3,'g',range(300),ps,'y')
pt.show()
