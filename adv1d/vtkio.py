#! /usr/bin/env python3

# author: Antonio Cervone <a.cervone@unibo.it>
# date: 2025-12-05

from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class VTKIO1D:
    basename: Path
    a: float
    b: float
    nx: int

    # _steps: list[int] = field(default_factory=list)
    # _times: list[float] = field(default_factory=list)

    def __post_init__(self):
        self.basename = Path(self.basename)
        Path(self.basename.parent).mkdir(parents=True, exist_ok=True)
        

    def print(self, sol, step: int, time: float):
        # self._steps.append(step)
        # self._times.append(time)
        with open(f"{self.basename}.{step:06d}.vtk", "w") as f:
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
            f.write(f"SCALARS {self.basename} double\n")
            f.write("LOOKUP_TABLE default\n")
            for i in range(self.nx):
                f.write(f"{sol[i]}\n")
        # self.print_pvd()

    # def print_pvd(self):
    #     with open(f"{self.basename}.pvd", "w") as f:
    #         f.write('<VTKFile type="Collection" version="1.0" byte_order="LittleEndian" header_type="UInt64">\n')
    #         f.write("  <Collection>\n")
    #         for step, time in zip(self._steps, self._times):
    #             f.write(f'    <DataSet timestep="{time:.6e}" part="0" file="{self.basename.name}.{step:06d}.vtk"/>\n')
    #         f.write("  </Collection>\n")
    #         f.write("</VTKFile>\n")
