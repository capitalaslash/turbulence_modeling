import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

# parameters
time_final = 2000.0
h = 0.0127  # m
u_in = 44.2  # m/s

# load case
reader = pv.POpenFOAMReader("sol.foam")
reader.set_active_time_value(time_final)
mesh = reader.read()

# extract mesh patch of interest
mesh_wall = mesh["boundary"]["lowerWall"]

# interpolate on line
xLeft, xRight, yBottom, yTop, zFront, zBack = mesh_wall.bounds
pStart = (0.0, yBottom, 0.5 * (zFront + zBack))
pEnd = (xRight, yBottom, 0.5 * (zFront + zBack))
line_data = mesh_wall.sample_over_line(
    pStart,
    pEnd,
    resolution=1000,
)
# print(line_data.array_names)

# create non-dimensional coordinate
x_hat = line_data["Distance"] / h

# compute friction coefficient
cf = -line_data["wallShearStress"][:, 0] / (0.5 * u_in**2)

# grab experimental data
data_exp = np.loadtxt("../experimental/cf.exp.csv", delimiter=",", skiprows=1)
x_exp = data_exp[:, 0]
cf_exp = data_exp[:, 1]

# create plot
fig, ax = plt.subplots(1, 1, figsize=(7, 4))

# plot friction coefficient
ax.plot(x_hat, cf, label="OpenFOAM")
ax.plot(x_exp, cf_exp, marker="+", label="exp")

# visualize/print
plt.legend()
plt.grid()
plt.show()
