from matplotlib import pyplot as plt
import matplotlib

f = open('network_rate.txt')
raw = f.readlines()
f.close()

net = []
pb = []
for l in raw:
    ls = l.split()
    pb.append(float(ls[0]))

    net.append(float(ls[1]))


plt.rcParams["figure.figsize"] = (20,10)
plt.axis([0.225,0.425,0.24,2.5])
plt.plot(pb,net,'-Db')
plt.xlabel('$P_B = P_S$',fontsize=20)
plt.ylabel('Networking rate [msg/s]',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.savefig('net_rate_vs_pb.pdf',dpi=300,bbox_inches='tight')
plt.show()
