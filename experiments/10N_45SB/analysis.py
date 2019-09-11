import re
ID = re.compile(r'D[0-9]+-[0-9]+\**')
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
Tn = 200

node1_l = load('res-1.txt')
node2_l = load('res-2.txt')
node_U_l = load('res-udp.txt')

B1 = count(node1_l,'B')
S1 = count(node1_l,'S')
N1 = count(node1_l,'N')

print(B1*Tb/(B1*Tb+S1*Ts+N1*Tn))
print(S1*Ts/(B1*Tb+S1*Ts+N1*Tn))
print(N1*Tn/(B1*Tb+S1*Ts+N1*Tn))

