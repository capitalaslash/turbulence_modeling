#! /usr/bin/env python3

# author: Antonio Cervone <a.cervone@unibo.it>
# date: 2024-11-14

# import packages
import math

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim

from vtkio import VTKIO1D

# define domain (mesh)
a = 0.0
b = 1.0
nx = 21
dx = (b - a) / (nx - 1)
x = np.linspace(a, b, nx)

# define current and old solution
u = np.zeros(shape=(nx,))
uold = np.zeros(shape=(nx,))

# set initial condition
au = math.floor(0.2 * (b - a) / dx)
bu = math.floor(0.4 * (b - a) / dx)
u[au:bu] = 1.0

# set simulation parameters
#  physical
c = 0.1
#  numerical
dt = 0.4
nt = 25

# set up solution storage
storage = np.zeros(shape=(nx, nt + 1))
# store initial solution
storage[:, 0] = u

print(f"final time: {dt * nt}")
print(f"CFL number: {c * dt / dx}")

io = VTKIO1D(a, b, nx, "u")
io.print(u, 0, 0.0)

# start time loop
for k in range(nt):
    current_time = dt * (k + 1)
    print(f"current time: {current_time:.3f}")

    # update old solution
    uold = u.copy()

    # loop on mesh points
    for i in range(0, nx):
        # update the solution using the forward euler/upwind method
        u[i] = uold[i] - c * (dt / dx) * (uold[i] - uold[i - 1])

        # update the solution using the fe/centered method
        # u[i] = uold[i] - 0.5 * c * (dt / dx) * (uold[(i + 1) % nx] - uold[i - 1])

    # # fix boundary conditions (if necessary)
    # u[0] = 0.0
    # u[nx - 1] = u[nx - 2]

    # store current solution
    storage[:, k + 1] = u

    # print solution
    io.print(u, k + 1, current_time)

# exit()

# define plotting framework
fig, ax = plt.subplots()


# define function for plot animation
def update(k):
    # clear plot
    ax.cla()

    # add lower and upper bound
    ax.plot(x, np.zeros(shape=(nx,)), "g")
    ax.plot(x, np.ones(shape=(nx,)), "g")

    # plot solution at time k
    ax.plot(x, storage[:, k + 1], label=f"u, timestep {k + 1}")

    # add legend and grid
    ax.legend()
    ax.grid()


ani = anim.FuncAnimation(
    fig=fig, func=update, frames=nt, interval=2500 * dt, repeat=False
)
plt.show()
