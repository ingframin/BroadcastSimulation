f1 = open("d0-result.txt")
raw1 = f1.read()
f1.close()

f2 = open("d1-result.txt")
raw2 = f2.read()
f2.close()

good = 0
s1 = 0
b1 = 0
s2 = 0
b2 = 0

for r1,r2 in zip(raw1,raw2):
    if r1 == 'S':
        s1 += 1
    elif r1 == 'B':
        b1 += 1
    if r2 == 'S':
        s2 += 1
    elif r2 =='B':
        b2 += 1

    if r1 == 'S' and r2 == 'B':
        good+=1
    
print(good/len(raw1))
print("P1(S)=%.6f"%(s1/len(raw1)))
print("P1(B)=%.6f"%(b1/len(raw1)))
print("P2(S)=%.6f"%(s2/len(raw1)))
print("P2(B)=%.6f"%(b2/len(raw1)))
print(s1)
print(b2)