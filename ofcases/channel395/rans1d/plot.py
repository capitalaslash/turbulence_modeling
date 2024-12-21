import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

# parameters
time_final = 800.0
nu = 1.7833656e-07

# load csv
data_dns = np.loadtxt("../exp/395.csv", delimiter=",", skiprows=1)

# csv header
csv_headers = {
    "y+1": 0,
    "u_mean": 1,
    "uu+": 2,
    "ww+": 3,
    "y+2": 4,
    "vv+": 5,
    "-uv+": 6,
    "-uv/urmsvrms": 7,
    "nu_t+": 8,
    "Diss.": 9,
    "Prod.": 10,
    "Mole_Diff.": 11,
    "vel_p_grad.": 12,
    "Turb_Diff.": 13,
}

# load case
reader = pv.POpenFOAMReader("sol.foam")
reader.set_active_time_value(time_final)
# reader.cell_to_point_creation = False
mesh = reader.read()

# extract mesh objects of interest
mesh_internal = mesh["internalMesh"]
mesh_wall = mesh["boundary"]["bottomWall"]

# get wss from the wall
yPlusMin = mesh_wall["yPlus"][0]
wss = -mesh_wall["wallShearStress"][0][0]
uTau = np.sqrt(wss)

print(f"yPlus min:       {yPlusMin:.6e}")
print(f"wallShearStress: {wss:.6e}")
print(f"uTau:            {uTau:.6e}")

# create a slice with normal on z and move it the z=0 plane
mesh_slice = mesh_internal.slice(normal="z")
mesh_slice.translate((0.0, 0.0, -mesh_slice.center[-1]), inplace=True)
# mesh_slice.set_active_scalars("k", preference="cell")

# extract data on a line normal to wall
xMid = 0.5 * (mesh_slice.bounds[0] + mesh_slice.bounds[1])
yMid = 0.5 * (mesh_slice.bounds[2] + mesh_slice.bounds[3])
pBottom = [xMid, mesh_slice.bounds[2], 0.0]
pTop = [xMid, yMid, 0.0]
# line = pv.Line(pBottom, pTop)
line_data = mesh_slice.sample_over_line(
    pBottom,
    pTop,
    resolution=1000,
)
print(f"ReTau:           {uTau * yMid / nu:.0f}")

# compute yPlus
yPlus = line_data["Distance"] * uTau / nu

# compute uPlus
uPlus = line_data["U"][:, 0] / uTau

# create canvas for plotting
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# plot DNS data
axes[0].scatter(
    data_dns[:, csv_headers["y+1"]],
    data_dns[:, csv_headers["u_mean"]],
    marker="x",
    color="r",
    label="DNS",
)

# plot uPlus on same graph
axes[0].plot(yPlus, uPlus, label="openFOAM 1D")

# plot viscous sublayer
yPlusViscous = yPlus[np.where((yPlus >= 0.1) & (yPlus <= 10))]
uViscous = yPlusViscous
axes[0].plot(yPlusViscous, uViscous, label="viscous sublayer")

# plot log sublayer
yPlusLog = yPlus[np.where((yPlus >= 20) & (yPlus <= 250))]
uLog = np.log(yPlusLog) / 0.41 + 5.0
axes[0].plot(yPlusLog, uLog, label="log sublayer")

# set up plot
axes[0].set_xlabel("yPlus")
axes[0].set_ylabel("uPlus")
axes[0].grid()
axes[0].semilogx()
axes[0].legend()


# plot DNS data
# warning: uu+ and ww+ are given on y+1, while vv+ is on y+2, they should not
# be summed up raw, they should be interpolated. Here uu+ dominates so the
# error is not too bad
k_dns = 0.5 * (
    data_dns[:, csv_headers["uu+"]]
    + data_dns[:, csv_headers["vv+"]]
    + data_dns[:, csv_headers["ww+"]]
)

axes[1].scatter(
    data_dns[:, csv_headers["y+1"]],
    k_dns,
    marker="x",
    color="r",
    label="DNS",
)

# plot kPlus
axes[1].plot(yPlus, line_data["k"] / (uTau * uTau), label="kPlus")

# set up plot
axes[1].set_xlabel("yPlus")
axes[1].set_ylabel("kPlus")
axes[1].grid()
axes[1].semilogx()
axes[1].legend()

# show plots
axes[0].set_title(f"yPlus min = {yPlusMin:.6e}")
plt.show()
# plt.savefig("plot40.pdf")
