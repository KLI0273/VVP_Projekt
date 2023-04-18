import numpy as np
import matplotlib.pyplot as plt

n,k = 5,0
matr = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        k += 1
        matr[i,j] = k

plt.imshow(matr, cmap='magma')
plt.colorbar()
plt.show()