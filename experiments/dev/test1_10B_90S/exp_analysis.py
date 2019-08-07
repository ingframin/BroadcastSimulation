import re
MSG = re.compile(r'D[0-9]+-[0-9]+.*')

def find_last(lines):
    for l in lines[-1::]:
        if len(l)>1:
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



f = open('res-1.txt')
raw = f.read()
f.close()

Ns = raw.count('S')
Nb = raw.count('B')
print(Ns/(Ns+Nb))
print(Nb/(Ns+Nb))
lines = raw.split('\n')
l0 = lines[0]
l1 = find_last(lines)
d = duration(l0,l1)
print('duration: %.6f'%d)
Ttx=(Nb*28e-3/d)
Trx=(Ns*60e-3/d)

e,w = get_windows(lines)
