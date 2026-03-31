#%%
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(6401)


#%%
N = 10000
mean_x, mean_y = 0,0
var_x, var_y = 1,1
x = np.random.uniform(mean_x, np.sqrt(var_x), N)
y = np.random.uniform(mean_y, np.sqrt(var_y), N)

plt.figure(figsize=(8,8))
plt.plot(x,
         y,
         marker = 'o',
         linestyle = 'None',
         markerfacecolor = 'c',
         markeredgecolor = 'k',
         markersize = 10,
          )
plt.title("Scatter Plot")
plt.grid(True)
plt.tight_layout()
plt.show()


#%%
plt.figure(figsize=(8,8))
plt.hist(y, bins = 100, color = 'c')
plt.title("Histogram")
plt.grid(True)


#%%
from math import sqrt, sin, cos, pi
def randompointincircle(R=1, xc=0, yc=0):
    r = R * sqrt(np.random.random())
    theta = 2 * pi * np.random.random()
    x = r * cos(theta) + xc
    y = r * sin(theta) + yc
    return x,y
N = 10000
x, y = [], []
for i in range(N):
    P1, P2 = randompointincircle(R=1, xc=0, yc=0)
    x.append(P1)
    y.append(P2)
plt.figure(figsize=(8,8))
plt.plot(x,
         y,
         marker = 'o',
         linestyle = 'None',
         markerfacecolor = 'c',
         markeredgecolor = 'k',
         markersize = 10, )

plt.title("Scatter Plot Unit Disk")
plt.grid(True)
plt.tight_layout()
plt.show()


#%%
x = np.linspace(-10,10,100)
y1 = x ** 2
y2 = x ** (1/2)

y3 = x ** 3
y4 = x ** (1/3)

fig, ax = plt.subplots(2,2)
ax[0,0].plot(x,y1, label='$f(x) = x^{2}$')

ax[1,0].plot(x,y2, label='$f(x) = \sqrt{x}$')
ax[0,1].plot(x,y3, label='$f(x) = x^{3}$')
ax[1,1].plot(x,y4, label='$f(x) = x^{2}$')

plt.tight_layout()
plt.show()

#%%
x = np.linspace(-10,10,100)
y = [10 ** el for el in x]
z = [2 ** el for el in x]


#%%
#display first 20 person in dataset using plt.subplot(5x4)

