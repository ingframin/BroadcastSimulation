from math import cos,sin
from matplotlib import pyplot as plt

x = [t/100 for t in range(1258)]
y = [sin(t) for t in x]

plt.plot(x,y)
plt.show()
