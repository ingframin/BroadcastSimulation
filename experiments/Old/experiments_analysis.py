#!/usr/bin/env python
# coding: utf-8
class TimeStamp:

    def __init__(self,stamp):
        ss = stamp.split(':')
        self.days = 0
        self.hours = int(ss[0])
        self.minutes = int(ss[1])
        self.seconds = float(ss[2])

    def __add__(self,ts):
        self.seconds += ts.seconds
        while self.seconds > 60:
            self.minutes += 1
            self.seconds -= 60
            
        self.minutes += ts.minutes
        while self.minutes > 60:
            self.hours += 1
            self.minutes -= 60

        self.hour += ts.hour
        while self.hours > 24:
            self.days += 1
            self.hours -= 24

        return self
    
    def __sub__(self,ts):
        
        hours = abs(self.hours -ts.hours)
        minutes = abs(self.minutes - ts.minutes)
        seconds = abs(self.seconds - ts.seconds)
        s = "%d:%d:%.8f"%(hours,minutes,seconds)
        return TimeStamp(s)

    def compareTo(self, ts):
        h = self.hours - ts.hours
        if h < 0:
            return -1
        if h > 0:
            return 1
        m = self.minutes - ts.minutes
        if m < 0:
            return -1
        if m > 0:
            return 1
        s = self.seconds - ts.seconds
        if s < 0:
            return -1
        if s > 0:
            return 1

        return 0

    def __str__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)

    def __repr__(self):
        return "%d:%d:%.8f"%(self.hours,self.minutes,self.seconds)
    
    def toSeconds(self):
        h = self.hours*3600
        m = self.minutes*60
        s = self.seconds
        return h+m+s


# In[9]:


import re
from matplotlib import pyplot as pt

MSG = re.compile(r'D[0-9]+-[0-9]+.*')
SENT = re.compile(r'[0-9]+:[0-9]+:[0-9]+\.[0-9]+')

def find_last(lines):
    for l in lines[-1::-1]:
        if len(l.split())>1:
            return l

def duration(l0,l1):
    print(l0)
    print(l1)
    x = SENT.findall(l0)[0]
    start = TimeStamp(x).toSeconds()
    stop = TimeStamp(l1.split()[0]).toSeconds()
    return stop - start

def get_windows(lines):
    events = []
    for l in lines:
        if l =='' or 'count' in l:
            continue
        ls = l.split()
        if len(ls)<2:
            continue
        t = TimeStamp(ls[0])
        e = (t.toSeconds(),ls[1])
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


f = open('test-1.txt')
lines = f.readlines()
f.close()
f2 = open('test-2.txt')
lines2 = f2.readlines()
f2.close()


# In[15]:


e,w = get_windows(lines)
d = duration(lines[0],find_last(lines))
e2,w2 = get_windows(lines2)
print(find_last(lines2))
d2 = duration(lines2[0],find_last(lines2))


# In[16]:


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

pt.plot(x,y)
pt.plot(x2,y2)
pt.show()


# In[ ]:




