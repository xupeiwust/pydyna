"""
Sloshing
========

This example shows how to directly impose a displacement of the entire volume mesh
through the use of the ``ICFD_CONTROL_IMPOSED_MOVE`` keyword. The executable file
for LS-DYNA is ``ls-dyna_smp_d_R13.0_365-gf8a97bda2a_winx64_ifort190.exe``.
"""

import os
import sys


from ansys.dyna.core.pre.dynasolution import DynaSolution
from ansys.dyna.core.pre.dynaicfd import (
    DynaICFD,
    MatICFD,
    ICFDPart,
    ICFDDOF,
    Curve,
    ICFDVolumePart,
    MeshedVolume,
    ICFDAnalysis,
    Curve,
    Gravity,
    GravityOption,
    Compressible
    )
from ansys.dyna.core.pre import examples
# sphinx_gallery_thumbnail_path = '_static/pre/icfd/sloshing.png'

hostname = "localhost"
if len(sys.argv) > 1:
    hostname = sys.argv[1]

solution = DynaSolution(hostname)
# Import the initial mesh data(nodes and elements)
fns = []
path = examples.sloshing + os.sep
fns.append(path + "sloshing.k")
solution.open_files(fns)
solution.set_termination(termination_time=1)
icfd = DynaICFD()
solution.add(icfd)

icfdanalysis = ICFDAnalysis()
icfdanalysis.set_timestep(0.02)
icfd.add(icfdanalysis)

# define model
mat1 = MatICFD(flow_density=1000, dynamic_viscosity=0.001)
mat2 = MatICFD(flag=Compressible.VACUUM)

part_bottom = ICFDPart(1)
part_bottom.set_material(mat1)
part_bottom.set_non_slip()
icfd.parts.add(part_bottom)

part_top = ICFDPart(2)
part_top.set_material(mat2)
part_top.set_non_slip()
icfd.parts.add(part_top)

part_mid = ICFDPart(3)
part_mid.set_material(mat1)
icfd.parts.add(part_mid)

g = Gravity(dir=GravityOption.DIR_Z, load=Curve(x=[0, 10000], y=[9.81, 9.81]))
icfd.add(g)

icfd.set_imposed_move(vx=Curve(x=[0, 0.5, 0.52, 0.8, 0.82, 2.0], y=[1, 1, -1, -1, 0, 0]))

partvol_bottom = ICFDVolumePart(surfaces=[1, 3])
partvol_bottom.set_material(mat1)
icfd.parts.add(partvol_bottom)

partvol_top = ICFDVolumePart(surfaces=[2, 3])
partvol_top.set_material(mat2)
icfd.parts.add(partvol_top)
# define the volume space that will be meshed,The boundaries
# of the volume are the surfaces "spids"
meshvol = MeshedVolume(surfaces=[1, 2])
meshvol.set_fluid_interfaces([3])
icfd.add(meshvol)

solution.create_database_binary(dt=0.02)
solution.save_file()
