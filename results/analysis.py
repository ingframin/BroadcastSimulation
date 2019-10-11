from math import e, factorial, log, gamma, sqrt, floor, exp
from matplotlib import pyplot as pt
from numpy.random import geometric, poisson, exponential
from scipy.stats import ks_2samp
from scipy.stats import norm  # ,poisson
from numpy import linspace
from IPython.display import Markdown
import re


def computeEvents(V, ttx, trx, tn):
    Eb = 0
    Es = 0
    En = 0

    for c in V:
        if c == 'B':  # broadcast event is a B sorrounded by 14 X
            Eb += 1
        elif c == 'S':
            Es += 1
        elif c == 'N':
            En += 1

    return (Eb, Es/trx, En/tn)


def geom_dist(p, maxK, k0=0):
    return [p*(1-p)**(k-k0) for k in range(0, maxK)]


def poisson_dist(lam, maxK):
    return [e**(k*log(lam)-(lam)-log(gamma((k+1)))) for k in range(0, maxK)]


def exponential_dist(lam, maxK):
    return [lam*(e**(-lam*k)) for k in range(0, maxK)]


def gamma_dist(beta, maxK, alpha):
    k = (beta**alpha)/gamma(alpha)
    return [k*(x**(alpha-1))*exp(-beta*x) for x in range(maxK)]


def rmse(v1, v2):
    rmse = 0
    for x1, x2 in zip(v1, v2):
        rmse += (x1-x2)**2
    return sqrt(rmse/len(v1))


def checkSuccess(Vtx, Vrx):
    Cb = 0

    for b, s in zip(Vtx, Vrx):
        if b == 'B' and s == 'S':
            Cb += 1
    return Cb  # number of successfull events


def findScanInterval(Vtx, Vrx, Ttx, Trx):
    scan_intervals = [{'s': m.start(), 'e': m.end(), 'n': 0}
                      for m in re.finditer(Trx*'S', Vrx)]
    for si in scan_intervals:
        si['n'] = Vtx[si['s']:si['e']].count(Ttx*'B')

    return scan_intervals


def generateHistogram(sc_int, Trx):
    hist = [0 for x in range(Trx+1)]
    for si in sc_int:
        hist[si['n']] += 1
    for i in range(Trx+1):
        hist[i] /= len(sc_int)
    return hist


def genWindowHistogram(r1, r2, wnd):
    windows = []
    for i in range(0, len(r1), wnd):
        count = 0
        for j in range(i, i+wnd):
            try:
                if r1[j] == 'S' and r2[j] == 'B':
                    count += 1
            except:
                pass
        windows.append(count)

    result = [0 for i in range(wnd)]
    for n in range(len(result)):
        result[n] = windows.count(n)/len(windows)
    print(sum(result))
    return result


def compute_histogram(r1, r2, Trx, Ttx, Tn):

    Eb1, Es1, En1 = computeEvents(r1, Ttx, Trx, Tn)
    Eb2, Es2, En2 = computeEvents(r2, Ttx, Trx, Tn)
    display(Markdown('<span style="color: #af0000">' +
                     "P(S) = %.6f" % (Trx*Es1/len(r1))+'</span>'))
    display(Markdown('<span style="color: #00af00">' +
                     "P(N) = %.6f" % (Tn*En1/len(r1))+'</span>'))
    display(Markdown('<span style="color: #0000af">' +
                     "P(B) = %.6f" % (Ttx*Eb1/len(r1))+'</span>'))

    Pb2 = Eb2*Ttx/(Eb2*Ttx+En2*Tn+Es2*Trx)
    rt1 = Pb2/(Ttx/1000)

    print("r(B)(Events/s) = %.6f" % (rt1))

    hist1 = genWindowHistogram(r1, r2, 1000)
    Esuc = checkSuccess(r2, r1)
    Ps = Esuc/Eb2
    rs2 = Esuc*1000/len(r1)
    print("r(Suuccess)(Events/s) = %.6f" % rs2)
    Pscan = Trx*Es1/len(r1)
    r_scan = 1000*Pscan/Trx
    print("r(S)(Events/s) = %.6f" % r_scan)
    Ns = Ps*1000/Ttx
    Nb = rt1*1000
    print("Success probability evts: %.6f" % (Ps))
    return hist1, Eb1, Es1, En1, Ps


if __name__ == '__main__':
    f1 = open("r1-d0-result.txt")
    raw1 = f1.read()
    f1.close()

    f2 = open("r1-d1-result.txt")
    raw2 = f2.read()
    f2.close()

    f3 = open("r2-d0-result.txt")
    raw3 = f3.read()
    f3.close()

    f4 = open("r2-d1-result.txt")
    raw4 = f4.read()
    f4.close()

    f5 = open("r3-d0-result.txt")
    raw5 = f5.read()
    f5.close()

    f6 = open("r3-d1-result.txt")
    raw6 = f6.read()
    f6.close()

    f7 = open("r4-d0-result.txt")
    raw7 = f7.read()
    f7.close()

    f8 = open("r4-d1-result.txt")
    raw8 = f8.read()
    f8.close()

    f9 = open("r5-d0-result.txt")
    raw9 = f9.read()
    f9.close()

    f10 = open("r5-d1-result.txt")
    raw10 = f10.read()
    f10.close()

    f11 = open("r6-d0-result.txt")
    raw11 = f11.read()
    f11.close()

    f12 = open("r6-d1-result.txt")
    raw12 = f12.read()
    f12.close()

    f13 = open("r7-d0-result.txt")
    raw13 = f13.read()
    f13.close()

    f14 = open("r7-d1-result.txt")
    raw14 = f14.read()
    f14.close()

    f15 = open("r8-d0-result.txt")
    raw15 = f15.read()
    f15.close()

    f16 = open("r8-d1-result.txt")
    raw16 = f16.read()
    f16.close()
    Ttx = 30
    Trx = 60
    Tn = 100
    hist1, Eb1, Es1, En1, Ps1 = compute_histogram(raw1, raw2)
    print(1-hist1[0])
    print('---------------------')
    hist2, Eb2, Es2, En2, Ps2 = compute_histogram(raw3, raw4)
    print(1-hist2[0])
    print('---------------------')
    hist3, Eb3, Es3, En3, Ps3 = compute_histogram(raw5, raw6)
    print(1-hist3[0])
    print('---------------------')
    hist4, Eb4, Es4, En4, Ps4 = compute_histogram(raw7, raw8)
    print(1-hist4[0])
    print('---------------------')
    hist5, Eb5, Es5, En5, Ps5 = compute_histogram(raw9, raw10)
    print(1-hist5[0])
    print('---------------------')
    hist6, Eb6, Es6, En6, Ps6 = compute_histogram(raw11, raw12)
    print(1-hist6[0])
    print('---------------------')
    hist7, Eb7, Es7, En7, Ps7 = compute_histogram(raw13, raw14)
    print(1-hist7[0])
    print('---------------------')
    hist8, Eb8, Es8, En8, Ps8 = compute_histogram(raw15, raw16)
    print(1-hist8[0])
    print('---------------------')
    pt.rcParams["figure.figsize"] = (20, 10)
    pt.plot(range(len(hist1)), hist1, label="P(succ)= %.3f" % (100*Ps1))
    #pt.plot(range(len(hist2)),hist2,label="P(succ)= %.3f"%(100*Ps2))
    #pt.plot(range(len(hist3)),hist3,label="P(succ)= %.3f"%(100*Ps3))
    pt.plot(range(len(hist4)), hist4, label="P(succ)= %.3f" % (100*Ps4))
    #pt.plot(range(len(hist5)),hist5,label="P(succ)= %.3f"%(100*Ps5))
    #pt.plot(range(len(hist6)),hist6,label="P(succ)= %.3f"%(100*Ps6))
    pt.plot(range(len(hist7)), hist7, label="P(succ)= %.3f" % (100*Ps7))
    #pt.plot(range(len(hist8)),hist8,label="P(succ)= %.3f"%(100*Ps8))
    pt.legend()
    pt.axis([0, 30, 0, 0.25])
    pt.xticks(range(30), [str(n) for n in range(30)])
    pt.xlabel(r'$\mathcal{k}$', fontsize=18)
    pt.ylabel(r'P(k-messages-received)')
    pt.savefig('test.svg', format='svg', dpi=300, bbox_inches='tight')
    pt.grid(True)
    pt.show()
