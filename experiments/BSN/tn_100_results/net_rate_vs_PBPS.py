from matplotlib import pyplot as plt
import matplotlib

f = open('network_rate.txt')
raw = f.readlines()
f.close()

net = []
tx = []
pb = []
for l in raw:
    ls = l.split()
    pb.append(float(ls[0]))
    tx.append(float(ls[1]))
    net.append(float(ls[2]))
    

plt.rcParams["figure.figsize"] = (20,10)

plt.plot(pb,net,'-Dg',markersize=25, label="Networking")
plt.plot(pb,tx,'-vr',markersize=25, label="BS throughput")
plt.xlabel('$P_B = P_S$',fontsize=30)
plt.ylabel('Networking rate [msg/s]',fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.grid(True)
plt.legend(fontsize=30)
plt.savefig('net_rate_vs_pb.pdf',dpi=300,bbox_inches='tight')
plt.show()
