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

f4 = open("d3-result.txt")
raw4 = f4.read()
f4.close()

good = 0
b1 = []

i = 0
Ttx = 8
Trx = 120
while i < len(raw1) - Ttx :
    if raw1[i] == 'B':
        b1.append(i)
    i+=1
Es = 0
for c in raw1:
    if c =='S':
        Es+=1

print("P(S) = %.6f"%(Es/len(raw1)))


l1 = 1000*len(b1) / (Ttx*len(raw1))

t = 120e-3
rt = l1*t
print("P(B) = %.6f"%(len(b1)/len(raw1)))
print("r(B) = %.6f"%(l1))
print("rt = %.6f"%(l1*t))
Erx1 = 0
Erx2 = 0
Erx3 = 0

def count_erx(Vb,Raw):
    erx = 0
    for b in Vb:
        for s in range(b,b+Ttx):
            if Raw[s] == 'S':
                erx += 1
                break
    return erx

print(count_erx(b1,raw2)/len(b1))
print(count_erx(b1,raw3)/len(b1))
print(count_erx(b1,raw4)/len(b1))


P1 = []

for k in range(20):
    v = e**(k*log(rt)-rt-log(gamma((k+1))))
    
    P1.append(v)

print(sum(P1[1:]))
print(1-e**(-rt))


pt.plot(range(20),P1,'r',label="Analytical")
# # pt.plot(H.keys(),P1[0:len(hv)],'g',label="Analytical")
pt.legend()
pt.show()

# f = open('fun.txt','w')
# for k,v in zip(H.keys(),hv):
#     print("%.12f\t%.12f"%(k,v),file = f)
# f.close()
# # # pt.plot(range(100),pv1,'r',range(100),pv2,'b',range(100),pv3,'g')#,range(300),ps,'y')
# # # pt.show()
