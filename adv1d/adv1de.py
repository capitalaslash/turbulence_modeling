import matplotlib.pyplot as plt
import numpy as np


# local
import vtkio

# problem definition
a = 0.0
b = 1.0

# operating conditions
c = 0.1

# space discretization
nx = 40
hx = (b - a) / nx

# time discretization
dt = 0.02
nt = 100

cfl = c * dt / hx
print(f"CFL: {cfl:.6f}")
if cfl > 1.0:
    print(f"CFL > 1!!!")
    exit(1)

# solution arrays
u = np.zeros(shape=(nx + 1,))
uold = np.zeros(shape=(nx + 1,))

# initial condition
nl = 0 #(2 * nx) // 5
nr = (3 * nx) // 5
u[nl:nr] = 1.0
# x = np.linspace(a, b, nx + 1)
# u = np.exp(-((x - 0.5) / 0.1)**2)

# boundary condition
uleft = 1.0


# flux limiter
def minmod(r):
    return max(0.0, min(1.0, r))


def superbee(r):
    return max(
        0.0,
        min(1.0, 2 * r),
        min(2.0, r),
    )


def vanleer(r):
    if np.isnan(r):
        return 0.0
    if np.isinf(r):
        return 2.0
    return (r + np.abs(r)) / (1.0 + np.abs(r))


# print
io = vtkio.VTKIO1D("output/u", a, b, nx)
io.print(u, 0, 0.0)

# time loop
current_time = 0.0
for k in range(nt):
    current_time += dt
    print(f"solving step {k + 1:6d}, time: {current_time:.3e}")

    # update
    uold = u.copy()

    # space loop
    u[0] = uleft
    # u[0] = uold[0] - c * (dt / hx) * (uold[0] - uold[nx])
    # u[0] = uold[0] - 0.5 * c * (dt / hx) * (uold[1] - uold[nx])
    # u[nx] = uold[nx] - 0.5 * c * (dt / hx) * (uold[nx - 1] - uold[0])
    for i in range(1, nx):

        # # explicit Euler/upwind
        # u[i] = uold[i] - c * (dt / hx) * (uold[i] - uold[i - 1])

        # # explicit Euler/centered
        # u[i] = uold[i] - 0.5 * c * (dt / hx) * (uold[i + 1] - uold[i - 1])

        # limited
        # r = (uold[i + 1] - uold[i]) / (uold[i] - uold[i - 1])
        r = (uold[i] - uold[i - 1]) / (uold[i + 1] - uold[i])
        phi = minmod(r)
        # phi = superbee(r)
        # phi = vanleer(r)
        # phi = 0.0
        u[i] = (
            uold[i]
            - (1.0 - phi) * cfl * (uold[i] - uold[i - 1])
            - phi * 0.5 * cfl * (uold[i + 1] - uold[i - 1])
        )

    # print
    io.print(u, k + 1, current_time)

    # print(f"min: {np.min(u):.6e}")
    # print(f"max: {np.max(u):.6e}")

print("end")
