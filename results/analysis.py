from math import e, factorial,log, gamma, sqrt, floor
from matplotlib import pyplot as pt
f1 = open("r0-d0-result.txt")
raw1 = f1.read()
f1.close()

f2 = open("r0-d1-result.txt")
raw2 = f2.read()
f2.close()

good = 0
b1 = []
Es = 0
En = 0
i = 0
Ttx = 15
Trx = 300
while i < len(raw1) - Ttx :
    if raw1[i] == 'B':
        b1.append(i)
    elif raw1[i] == 'S':
        Es += 1
    elif raw1[i] == 'N':
        En += 1
    i+=1

Pb = len(b1)/len(raw1)
print("P(S) = %.6f"%(Es/len(raw1)))
print("P(N) = %.6f"%(En/len(raw1)))
print("P(B) = %.6f"%(len(b1)/len(raw1)))

l1 = 1000*len(b1) / (Ttx*len(raw1))
#l1 = len(b1) / (len(raw1))

t = Trx/1000
rt = l1*t

print("r(B) = %.6f"%(l1))
print("rt = %.6f"%(l1*t))


def count_BS(V1,V2):
    Cb = {}
    evt = 0
    for i in range(len(V2)):
        if V2[i] != 'S':
            continue
        else:
            
            if V2[i-1] != 'S' or evt == 0:
                Cb[i] = 0
            evt += 1
            if evt == Trx:
                evt = 0
    for k in Cb:
        try:
            for i in range(k,Trx+k):
                if V1[i] == 'B':
                    Cb[k] += 1
            Cb[k] = floor(Cb[k]/Ttx)
        except:
            break
    
    return Cb


Cb1 = count_BS(raw2,raw1) 

hist1 = [0 for x in range(20)]




for k in Cb1:
    if int(Cb1[k]) < 20:
        hist1[int(Cb1[k])] += 1
for i in range(len(hist1)):
    hist1[i] /= len(Cb1)
print(len(Cb1))
print(hist1)

l = sum(hist1)/len(hist1)

P1 = []
P2 = []
ex = []
#exp = []
for k in range(20):
    #v1 = e**(k*log(max(hist1))-max(hist1)-log(gamma((k+1))))
    v1 = e**(k*log(rt)-rt-log(gamma((k+1))))
    
    exd = hist1[0]*(1-hist1[0])**(k)
    #exp.append(hist1[0] * e**(-hist1[0]*k)) 
    P1.append(v1)
    ex.append(exd)
    
print("k=0 %.6f"%(1-e**(-rt)))
print(sum(hist1[1:]))
rmsp = 0
for p,h in zip(P1,hist1):
    rmsp += (p-h)**2

rmsp = sqrt(rmsp/len(P1))
print("RMSE Poisson= %.6f"%rmsp) 

rmse = 0
for p,h in zip(ex,hist1):
    rmse += (p-h)**2

rmse = sqrt(rmse/len(P1))
print("RMSE Geometric= %.6f"%rmse) 

# pt.plot(range(20),hist1,'r',label='Simulation')
pt.plot(range(20),P1,label='Poisson')
pt.plot(range(20),ex,label='Geometric')
pt.bar(range(20),hist1)
#pt.plot(range(20),exp, label='Exponential')
pt.legend()
pt.axis([0,20,0,0.5])
pt.xticks(range(20), [str(int(n)) for n in range(20)])
pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
pt.ylabel(r'P(k-messages-received)')
pt.grid(True)

pt.show()