#!/usr/bin/env python
# coding: utf-8



import re
from matplotlib import pyplot as pt

MSG = re.compile(r'D[0-9]+-[0-9]+.*')

def find_last(lines):
    for l in lines[-1::]:
        if len(l.split())>1:
            return l

def duration(l0,l1):
    start = float(l0.split()[0])
    stop = float(l1.split()[0])
    return stop - start

def get_windows(lines):
    events = []
    for l in lines:
        if l =='' or 'count' in l:
            continue
        ls = l.split()
        if len(ls)<2:
            continue
        e = (float(ls[0]),ls[1])
        events.append(e)
    w0 = None
    
    windows = []
    w = []
    for e in events:
        if w0 == None:
            w0 = e
            w.append(w0)
            continue
        if w0 != None:
            if e[0] - w0[0] < 1:
                w.append(e)
            else:
                windows.append(w.copy())
                w = []
                w0 = e
                w.append(w0)

    return events,windows



def computePrx(windows):
    hist = {}
    for w in windows:
        c = 0
        for e in w:
            if MSG.match(e[1]):
                c+=1
        try:
            hist[c] += 1
        except:
            hist[c] = 1
    return hist


# In[14]:


f = open('res-1.txt')
lines = f.readlines()
f.close()
f2 = open('res-2.txt')
lines2 = f2.readlines()
f2.close()

e,w = get_windows(lines)
d = duration(lines[0],find_last(lines))
e2,w2 = get_windows(lines2)
print(find_last(lines2))
d2 = duration(lines2[0],find_last(lines2))


h = computePrx(w)
x = []
y = []

for c in sorted(h):
    x.append(c)
    y.append(h[c]/d)
    
h2 = computePrx(w2)
x2 = []
y2 = []

for c in sorted(h2):
    x2.append(c)
    y2.append(h2[c]/d2)

sim = [0.01153386171528186, 0.04579084993817526, 0.10275069426144771, 0.14996047270589666, 0.17925121115683215, 0.16514300772302515, 0.13382522854884155, 0.09166278150528044, 0.05797336468489652, 0.03168264650436827, 0.016297407414914967, 0.008331137372549815, 0.0034662396367543024, 0.0015202805424360975, 0.0006486530314394017, 4.0540814464962604e-05]
pt.plot(x,y, label="Device 1")
pt.plot(x2,y2, label = "Device 2")
pt.plot(x,sim, label = "Simulation")
pt.legend()
pt.axis([0,len(x),0,0.2])
pt.xticks(range(0,len(x),1), [str(n) for n in range(0,len(x),1)])
pt.grid(True)

pt.show()





