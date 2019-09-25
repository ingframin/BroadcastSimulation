import re
from matplotlib import pyplot as plt

SSID = re.compile(r"D[0-9]+-[0-9]+\**")
COUNT = re.compile(r"count=[0-9]+")

def load(fn):
    f1 = open(fn)
    f1_raw = f1.readlines()
    f1.close()
    return f1_raw


def count(lines, evt):
    counter = 0
    for l in lines:
        if evt in l:
            counter += 1
    return counter


Ts = 60
Tb = 30
Tn = 205

lf1 = open('log-1.txt')
log1 = lf1.read()
lf1.close()

lf2 = open('log-2.txt')
log2 = lf2.read()
lf2.close()

lf3 = open('log-3.txt')
log3 = lf3.read()
lf3.close()

lf4 = open('log-4.txt')
log4 = lf4.read()
lf4.close()

rec1 = SSID.findall(log1)
print(rec1[-1])
rec2 = SSID.findall(log2)
print(rec2[-1])

rec3 = SSID.findall(log3)
print(rec3[-1])
rec4 = SSID.findall(log4)
print(rec4[-1])

print(len(rec1))
print(len(rec2))

cnt1 = COUNT.findall(log1)
cnt2 = COUNT.findall(log2)

print(cnt1[-1])
print(cnt2[-1])

msgs2 = []

for m in rec2:
    msgs2.append(int(m.replace('*','').split('-')[1]))

print(len(msgs2)/int(cnt1[-1].split('=')[1]))

msgs1 = []

for m in rec1:
    msgs1.append(int(m.replace('*','').split('-')[1]))

mset = set(msgs1)
print(len(mset)/int(cnt2[-1].split('=')[1]))

lines = log1.split('\n')
Nn = 0
Nb = 0
Ns = 0

for l in lines:
    if 'N' in l:
        Nn+=1
    elif 'B' in l:
        Nb+=1
    elif 'S' in l:
        Ns+=1

print(Nn*Tn/(Ns*Ts+Nb*Tb+Nn*Tn))
Pb = Nb*Tb/(Ns*Ts+Nb*Tb+Nn*Tn)
print(Pb)
Ps = Ns*Ts/(Ns*Ts+Nb*Tb+Nn*Tn)
print(Ps)
print(Pb*Ps)

timestamps = []
for l in lines:
    if 'count' in l or l=='':
        continue
    try:
        timestamps.append(float(l.split()[0].replace(',','').replace('(','')))
    except:
        print(l.split()[0].replace(',','').replace('(',''))
curr = 0
for t in timestamps:
    if t < curr:
        print(t)
    curr = t


plt.plot(timestamps)
plt.show()
