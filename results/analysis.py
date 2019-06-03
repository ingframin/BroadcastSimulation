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

#print(b1[0:100])
    

l1 = len(b1)/len(raw1)
l2 = len(b2)/len(raw1)
l3 = len(b3)/len(raw1)
ls = len(s1)/len(raw1)
print("P(B) = %.6f"%((l1+l2+l3)/3))
print("P(S)= %.6f"%ls)

D = []
for i in range(1,len(b1)):
    D.append(b1[i]-b1[i-1])

D.sort()

H = {}

for d in D:
    if d in H:
        H[d] += 1
    else:
        H[d] = 1

#print(len(H))
#print(H)
hv = [H[i]/len(b1) for i in H.keys()]
#print(hv)
P1 = []

for k in range(len(hv)):
    v = 1.25*e**(k*log(l1)-l1-log(gamma((k+1))))
    
    P1.append(v)
#     #P1.append((t*l1*e**(-l1*t))/factorial(t))       
# #     P2 = e**(k*log(l2*10)-l2*10-log(gamma(k+1)))
# #     P3 = e**(k*log(l3*10)-l3*10-log(gamma(k+1)))
# #    # Ps = e**(k*log(ls*120)-ls*120-log(gamma(k+1)))
# #     #print(gamma(k+1))
# #     #input()
# #     pv1.append(P1)
# #     pv2.append(P2)
# #     pv3.append(P3)
# #     #ps.append(Ps)
# x = D[0:len(P1)]
# print(hv[0:100])
# print(D[0:100])
# print(len(x))
# print(len(D)-len(P1))
print([hv[i]-P1[i] for i in range(len(hv))])
# pt.plot(H.keys(),hv,'r',label="Simulation")
# pt.plot(H.keys(),P1[0:len(hv)],'g',label="Analytical")
# pt.legend()
# pt.show()

f = open('fun.txt','w')
for k,v in zip(H.keys(),hv):
    print("%.12f\t%.12f"%(k,v),file = f)
f.close()
# # pt.plot(range(100),pv1,'r',range(100),pv2,'b',range(100),pv3,'g')#,range(300),ps,'y')
# # pt.show()
