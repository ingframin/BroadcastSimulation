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

def countSuccessT1(V1,V2):
    Cb = []
    i = 0
    for b,s in zip(V1,V2):
        if b =='B' and s =='S':
            Cb.append(i)
        i+=1
    return Cb

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

def buildHistogramV(V, l = 0):
    hist = None
    if l:
        hist = [0 for x in range(len(V))]
    else:
        hist = [0 for x in range(len(V))]

    for k in V:
        try:
            hist[k] += 1
        except:
            break
        
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

    f1 = open("r1-d0-result.txt")
    raw1 = f1.read()
    f1.close()

    f2 = open("r1-d1-result.txt")
    raw2 = f2.read()
    f2.close()

    f3 = open("r1-d2-result.txt")
    raw3 = f3.read()
    f3.close()

    Eb = 0
    Es = 0
    En = 0

    Ttx = 1
    Trx = 11
    Tn = 1

    Eb,Es,En = computeEvents(raw1,Ttx,Trx,Tn)

    print("P(S) = %.6f"%(Trx*Es/len(raw1)))
    print("P(N) = %.6f"%(Tn*En/len(raw1)))
    print("P(B) = %.6f"%(Ttx*Eb/len(raw1)))

    l1 = 1000*Eb / (len(raw1))

    t = Trx/1000
    rt = l1*t

    print("r(B)(Events/s) = %.6f"%(l1))
    print("rt = %.6f"%(l1*t))

    Cb1 = countSuccess(raw2,raw1, Trx,Ttx)
    Cb2 = countSuccess(raw3,raw1, Trx,Ttx) 
    
    hist1 = buildHistogram(Cb1,Trx,Ttx)
        
    pois_d = poisson_dist(0.0454545,len(hist1))
    #geom_d = geom(hist1[0],len(hist1))
    print(hist1)
    print("Success probability= %.6f"%sum(hist1[1:]))
    print("RMSE Poisson= %.6f"%rmse(pois_d,hist1)) 
    
    pt.plot(range(len(hist1)),pois_d,'r',label='Poisson')
    
    pt.bar(range(len(hist1)),hist1,label="P(Rx)= %.3f,T(B)/T(Total)= %.2f%%"%(sum(hist1[1:]),100*Ttx*Eb/len(raw1)))

    pt.legend()
    pt.axis([0,len(hist1),0,1.0])
    pt.xticks(range(len(hist1)), [str(int(n)) for n in range(len(hist1))])
    pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
    pt.ylabel(r'P(k-messages-received)')
    pt.grid(True)
    pt.show()