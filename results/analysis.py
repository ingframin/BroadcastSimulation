from math import e, factorial,log, gamma, sqrt, floor
from matplotlib import pyplot as pt
from numpy.random import geometric, poisson, exponential
from scipy.stats import ks_2samp

def computeEvents(V, ttx, trx, tn):
    Eb = 0
    Es = 0
    En = 0

    for c in V:
        if c == 'B':
            Eb += 1
        elif c == 'S':
            Es += 1
        else:
            En += 1
    return (Eb/ttx,Es/trx,En/tn)

def countSuccess(V1,V2,Trx,Ttx):
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
            #Cb[k] = Cb[k]/Ttx
            
        except:
            break
    
    return Cb

def buildHistogram(Cb,Trx,Ttx):
    hist = [0 for x in range(int(2*Trx/Ttx))]
    n = 1/len(Cb)
    for k in Cb:
        try:
            hist[round(Cb[k])] += n
        except:
            print(round(Cb[k]))
    return hist

def geom(p,maxK):
    return [p*(1-p)**k for k in range(0,maxK)]

def poisson_dist(lam,maxK):
    return [e**(k*log(lam)-(lam)-log(gamma((k+1)))) for k in range(0,maxK)]

def exponential_dist(lam, maxK):
    return [lam*(e**(-lam*k)) for k in range(0,maxK)]

def rmse(v1,v2):
    rmse = 0
    for x1,x2 in zip(v1,v2):
        rmse += (x1-x2)**2
    return sqrt(rmse/len(v1))

if __name__ == '__main__':

    f1 = open("r5-d0-result.txt")
    raw1 = f1.read()
    f1.close()

    f2 = open("r5-d1-result.txt")
    raw2 = f2.read()
    f2.close()

    f3 = open("r5-d2-result.txt")
    raw3 = f3.read()
    f3.close()

    Eb = 0
    Es = 0
    En = 0

    Ttx = 15
    Trx = 160
    Tn = 1

    Eb,Es,En = computeEvents(raw1,Ttx,Trx,Tn)

    print("P(S) = %.6f"%(Es/len(raw1)))
    print("P(N) = %.6f"%(En/len(raw1)))
    print("P(B) = %.6f"%(Eb/len(raw1)))

    l1 = 1000*Eb / (len(raw1))

    t = Trx/1000
    rt = l1*t

    print("r(B)(Events/s) = %.6f"%(l1))
    print("rt = %.6f"%(l1*t))

    Cb1 = countSuccess(raw2,raw1, Trx,Ttx)
    Cb2 = countSuccess(raw3,raw1, Trx,Ttx) 
    
    hist1 = buildHistogram(Cb1,Trx,Ttx)
    geodata = list(geometric(hist1[0],len(Cb1.values())))
    poidata = poisson(0.860605 ,len(Cb1.values()))
    expdata = exponential(rt,len(Cb1.values()))
    cbd1 = list(Cb1.values())
    cbd2 = list(Cb2.values())
    with open("cbdata.txt","w") as cbf:
        for d in cbd1:
            print(d,file=cbf)

    print(ks_2samp(cbd1,cbd2))
    print(ks_2samp(cbd1,geodata))
    print(ks_2samp(cbd2,geodata))
    print(ks_2samp(cbd1,poidata))
    print(ks_2samp(cbd2,poidata))
    print(ks_2samp(cbd1,expdata))
    print(ks_2samp(cbd2,expdata))
    
    P1 = poisson_dist(hist1[0],len(hist1))
    ex = geom(hist1[0],len(hist1))
    print(hist1)
    print("Success probability= %.6f"%sum(hist1[1:]))
    print("RMSE Poisson= %.6f"%rmse(P1,hist1)) 
    print("RMSE Geometric= %.6f"%rmse(ex,hist1)) 

    # pt.plot(range(len(hist1)),P1,'r',label='Poisson')
    # pt.plot(range(len(hist1)),ex,label='Geometric')
    # pt.bar(range(len(hist1)),hist1)

    # pt.legend()
    # pt.axis([0,len(hist1),0,1.0])
    # pt.xticks(range(len(hist1)), [str(int(n)) for n in range(len(hist1))])
    # pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
    # pt.ylabel(r'P(k-messages-received)')
    # pt.grid(True)
    # pt.show()