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
# if cfl > 1.0:
#     print(f"CFL > 1!!!")
#     exit(1)

# solution arrays
u = np.zeros(shape=(nx + 1,))
uold = np.zeros(shape=(nx + 1,))

# linear algebra
m = np.zeros(shape=(nx + 1, nx + 1))
rhs = np.zeros(shape=(nx + 1,))

# flux limiter
def minmod(r):
    return max(
        0.0, 
        min(1.0, r)
    )

def superbee(r):
    return max(
        0.0, 
        min(1.0, 2 * r), 
        min(2.0, r),
    )
def vanleer(r):
    if np.isinf(r):
        return 2.0
    return (r + np.abs(r)) / (1.0 + np.abs(r))


# initial condition
nl = (2 * nx) // 5
nr = (3 * nx) // 5
u[nl:nr] = 1.0

# boundary condition
uleft = 0.0

# print
io = vtkio.VTKIO1D("output/ui", a, b, nx)
io.print(u, 0, 0.0)

# time loop
current_time = 0.0
for k in range(nt):
    current_time += dt
    print(f"solving step {k + 1:6d}, time: {current_time:.3e}")

    # update
    uold = u.copy()

    # space loop
    # u[0] = uleft
    m[0, 0] = 1
    rhs[0] = uleft
    m[nx, nx] = 1
    rhs[nx] = uleft
    # u[0] = uold[0] - c * (dt / hx) * (uold[0] - uold[nx])
    # u[0] = uold[0] - 0.5 * c * (dt / hx) * (uold[1] - uold[nx])
    # u[nx] = uold[nx] - 0.5 * c * (dt / hx) * (uold[nx - 1] - uold[0])
    for i in range(1, nx):

        # # implicit Euler/upwind
        # # u[i] = uold[i] - cfl * (u[i] - u[i - 1])
        # # (1 + cfl) * u[i] - cfl * u[i - 1] = uold[i]
        # m[i, i] = 1 + cfl
        # m[i, i - 1] = -cfl
        # rhs[i] = uold[i]


        # # implicit Euler/centered
        # # u[i] = uold[i] - 0.5 * cfl * (u[i + 1] - u[i - 1])
        # # 0.5 * cfl * u[i + 1] + u[i] - 0.% * cfl * u[i - 1] = uold[i]
        # m[i, i] = 1
        # m[i, i - 1] = -0.5 * cfl
        # m[i, i + 1] = 0.5 * cfl
        # rhs[i] = uold[i]

        # implicit Euler/limited
        # u[i] = uold[i] - 0.5 * cfl * ((u[i + 1] - u[i]) + (u[i] - u[i - 1]))
        r = (uold[i + 1] - uold[i]) / (uold[i] - uold[i - 1])
        r = 0.0 if np.isnan(r) else r
        lim = minmod(r)
        # lim = superbee(r)
        # lim = vanleer(r)
        # u[i] = uold[i] - 0.5 * cfl * lim * (u[i + 1] - u[i - 1]) - cfl * (1 - lim) * (u[i] - u[i - 1])
        # 0.5 * cfl * lim * u[i + 1] + u[i] - 0.5 * cfl * u[i - 1] = uold[i]
        m[i, i] = 1 + cfl * (1 - lim)
        m[i, i - 1] = - cfl * (1 - 0.5 * lim)
        m[i, i + 1] = 0.5 * cfl * lim
        rhs[i] = uold[i]

    # solve
    u = np.linalg.solve(m, rhs)

    # print
    io.print(u, k + 1, current_time)

    # print(f"min: {np.min(u):.6e}")
    # print(f"max: {np.max(u):.6e}")

def minmodv(r):
    return np.maximum(
        np.zeros(shape=r.shape), 
        np.minimum(np.ones(shape=r.shape), r),
    )

def superbeev(r):
    return np.maximum(
        np.maximum(0.0, np.minimum(1.0, 2 * r)),
        np.minimum(2.0, r),
    )
def vanleerv(r):
    return (r + np.abs(r)) / (1.0 + np.abs(r))

# r = np.linspace(0, 5, 100)
# plt.plot(r, minmodv(r), label="minmod")
# plt.plot(r, superbeev(r), label="superbee")
# plt.plot(r, vanleerv(r), label="vanleer")
# plt.legend()
# plt.show()

print("end")