#! /usr/bin/env python3

# author: Antonio Cervone <a.cervone@unibo.it>
# date: 2024-11-14

from dataclasses import dataclass
import os


@dataclass
class VTKIO1D:
    a: float
    b: float
    nx: int
    filename: str

    def __post_init__(self):
        os.makedirs("output", exist_ok=True)

    def print(self, sol, step: int, time: float):
        with open(f"output/{self.filename}.{step:03d}.vtk", "w") as f:
            f.write("# vtk DataFile Version 5.1\n")
            f.write("VTKIO1D\n")
            f.write("ASCII\n")
            f.write("DATASET UNSTRUCTURED_GRID\n")
            f.write(f"POINTS {self.nx} double\n")
            dx = (self.b - self.a) / (self.nx - 1)
            for i in range(self.nx):
                f.write(f"{self.a + i * dx} 0.0 0.0\n")
            f.write(f"\nCELLS {self.nx} {(self.nx - 1) * 2}\n")
            f.write("OFFSETS vtktypeint64\n")
            for k in range(self.nx):
                f.write(f"{k * 2}\n")
            f.write("CONNECTIVITY vtktypeint64\n")
            for k in range(self.nx - 1):
                f.write(f"{k} {k + 1}\n")
            f.write(f"CELL_TYPES {self.nx - 1}\n")
            for k in range(self.nx - 1):
                f.write(f"{4}\n")
            f.write(f"\nPOINT_DATA {self.nx}\n")
            f.write(f"SCALARS {self.filename} double\n")
            f.write("LOOKUP_TABLE default\n")
            for i in range(self.nx):
                f.write(f"{sol[i]}\n")
