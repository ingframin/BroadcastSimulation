from math import e, factorial,log, gamma, sqrt, floor, fsum
from matplotlib import pyplot as pt
from analysis import *
from scipy.stats import ks_2samp

f= open("histograms.txt","w")

for i in range(1,10):
    #Load files
    f1 = open("r%d-d0-result.txt"%i)
    raw1 = f1.read()
    f1.close()
    f2 = open("r%d-d1-result.txt"%i)
    raw2 = f2.read()
    f2.close()

    Eb = 0
    Es = 0
    En = 0

    Ttx = 15
    Trx = 160
    Tn = 1

    Eb,Es,En = computeEvents(raw1,Ttx,Trx,Tn)
    l1 = 1000*Eb / len(raw1)

    t = Trx/1000
    rt = l1*t
    Cb1 = countSuccess(raw2,raw1, Trx, Ttx) 

    hist1 = buildHistogram(Cb1,Trx,Ttx)
    f.write(str(hist1))
    print(len(hist1))
    lam  = hist1[0]
    ex = geom(hist1[0],len(hist1))
    expd = exponential(lam,len(hist1))
    pois = poisson(lam,len(hist1))
    print("geom ks= "+str(ks_2samp(hist1,ex)))
    print("exponential ks= "+str(ks_2samp(hist1,expd)))
    print("poisson ks= "+str(ks_2samp(hist1,pois)))
    DB = round(100*Ttx*Eb/len(raw1),2)
    print("RMSE Geometric= %.6f"%rmse(ex,hist1))
    pt.plot(range(len(hist1)),ex,label="P(Rx)= %.3f,T(B)/T(Total)= %.2f%%"%(sum(hist1[1:]),DB))
    print("RMSE Exponential= %.6f"%rmse(expd,hist1))
    #pt.plot(range(len(hist1)),expd,label="P(Rx)= %.3f,T(B)/T(Total)= %.2f%%"%(sum(hist1[1:]),DB))
    pt.plot(range(len(hist1)),pois)

pt.axis([0,len(hist1),0,1.0])
#pt.legend()
pt.xticks(range(len(hist1)), [str(int(n)) for n in range(len(hist1))])
pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
pt.ylabel(r'P(k-messages-received)')
pt.grid(True)
pt.show()
f.close()