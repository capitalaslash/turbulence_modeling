import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt(
    "postProcessing/residuals(fields=(Upkomega))/0/residuals.dat",
    skiprows=3,
)

plt.plot(data[:, 0], data[:, 1], label="Ux")
plt.plot(data[:, 0], data[:, 2], label="Uy")
plt.plot(data[:, 0], data[:, 3], label="p")
plt.plot(data[:, 0], data[:, 4], label="k")
plt.plot(data[:, 0], data[:, 5], label="omega")

plt.legend()
plt.grid()
plt.semilogy()
plt.show()
