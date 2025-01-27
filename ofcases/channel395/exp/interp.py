import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("395.csv")

# fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# diag = np.linspace(0.1, 400.0, 400)
# ax.plot(diag, diag, label="diag")
# data.plot("y+", "y+2", ax=ax)

# plt.legend()
# plt.loglog()
# plt.show()

data["u_mean2"] = np.interp(data["y+2"], data["y+"], data["u_mean"])

data["uu+2"] = np.interp(data["y+2"], data["y+"], data["uu+"])

data.to_csv("395_interp.csv", index=False)
