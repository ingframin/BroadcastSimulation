from math import e, factorial,log, gamma, sqrt
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

f4 = open("d3-result.txt")
raw4 = f4.read()
f4.close()

good = 0
b1 = []
Es = 0
En = 0
i = 0
Ttx = 10
Trx = 120
while i < len(raw1) - Ttx :
    if raw1[i] == 'B':
        b1.append(i)
    elif raw1[i] == 'S':
        Es += 1
    elif raw1[i] == 'N':
        En += 1
    i+=1

print("P(S) = %.6f"%(Es/len(raw1)))
print("P(N) = %.6f"%(En/len(raw1)))
print("P(B) = %.6f"%(len(b1)/len(raw1)))

l1 = 1000*len(b1) / (Ttx*len(raw1))

t = 120e-3
rt = l1*t

print("r(B) = %.6f"%(l1))
print("rt = %.6f"%(l1*t))


def count_BS(V1,V2):
    Cb = {}
    i_s = 0
    
    while i_s < len(V2):
        if V2[i_s] == 'S':
            Cb[i_s] = 0
            for i_b in range(i_s,i_s+Trx):
                try:
                    if V1[i_b] == 'B':
                        Cb[i_s] += 1
                except:
                    break
            Cb[i_s] /= Ttx
            i_s += Trx
        else:
            i_s += 1
    return Cb

Cb1 = count_BS(raw2,raw1) 
Cb2 = count_BS(raw3,raw1) 
Cb3 = count_BS(raw4,raw1) 

hist1 = [0 for x in range(20)]
hist2 = [0 for x in range(20)]
hist3 = [0 for x in range(20)]



for k in Cb1:
    hist1[int(Cb1[k])] += 1
for i in range(len(hist1)):
    hist1[i] /= len(Cb1)


for k in Cb2:
    hist2[int(Cb2[k])] += 1
for i in range(len(hist2)):
    hist2[i] /= len(Cb2)

for k in Cb3:
    hist3[int(Cb3[k])] += 1
for i in range(len(hist3)):
    hist3[i] /= len(Cb3)



P1 = []

for k in range(20):
    v = e**(k*log(rt)-rt-log(gamma((k+1))))
    P1.append(v)

rms = 0
for p,h in zip(P1,hist1):
    rms += (p-h)**2

rms = sqrt(rms/len(P1))
print("RMSE= %.6f"%rms) 

pt.plot(range(20),hist1,'r',label='Simulation')
pt.plot(range(20),P1,'g',label='Analytical')
pt.legend()
pt.axis([0,20,0,0.5])
pt.xticks(range(20), [str(int(n)) for n in range(20)])
pt.xlabel(r'$\mathcal{k}$', fontsize = 18)
pt.ylabel(r'P(k-messages-received)')
pt.grid(True)
pt.annotate("RMSE= %.6f"%rms,(3,0.2),fontsize=16,
            horizontalalignment='left', verticalalignment='bottom', backgroundcolor='white')
pt.show()

# input()
# def count_erx(Vb,Raw):
#     erx = 0
    
#     for b in Vb:
#         for s in range(b,b+Ttx):
#             if Raw[s] == 'S':
#                 erx += 1
#                 break
#     return erx

# print(count_erx(b1,raw2)/len(b1))
# print(count_erx(b1,raw3)/len(b1))
# print(count_erx(b1,raw4)/len(b1))


# P1 = []

# for k in range(20):
#     v = e**(k*log(rt)-rt-log(gamma((k+1))))
    
#     P1.append(v)

# print(sum(P1[1:]))
# print(1-e**(-rt))


#pt.plot(range(20),P1,'r',label="Analytical")
# # pt.plot(H.keys(),P1[0:len(hv)],'g',label="Analytical")
#pt.legend()
#pt.show()

# f = open('fun.txt','w')
# for k,v in zip(H.keys(),hv):
#     print("%.12f\t%.12f"%(k,v),file = f)
# f.close()
# # # pt.plot(range(100),pv1,'r',range(100),pv2,'b',range(100),pv3,'g')#,range(300),ps,'y')
# # # pt.show()
