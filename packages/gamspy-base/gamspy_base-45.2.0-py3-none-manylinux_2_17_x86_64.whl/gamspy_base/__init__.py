import os
from pathlib import Path

from .version import __version__

directory = str(Path(__file__).resolve().parent)

available_solvers = ['NLPEC', 'SBB', 'CONOPT', 'CONVERT', 'CPLEX', 'PATH', 'BARON', 'CONOPT4', 'COPT', 'DICOPT', 'GUROBI', 'HIGHS', 'IPOPT', 'IPOPTH', 'KNITRO', 'MINOS', 'MOSEK', 'SCIP', 'SHOT', 'SNOPT', 'XPRESS']

files = ['libgdxdclib64.so', 'libgmszlib164.so', 'libstdc++.so.6', 'liboptdclib64.so', 'optgams.def', 'optsbb.def', 'gmscmpun.txt', 'optpath.def', 'libcvdcclib64.so', 'gmscvnus.run', 'eula.pdf', 'libconsub3.so', 'gamsstmp.txt', 'libptccclib64.so', 'libjoatdclib64.so', 'optnlpec.def', 'libcpxcclib64.so', 'libdctmdclib64.so', 'libconcclib64.so', 'libcplex2211.so', 'libgcc_s.so.1', 'gamserrs.txt', 'gamscmex.out', 'gmsgenux.out', 'libgmdcclib64.so', 'libguccclib64.so', 'libquadmath.so.0', 'optconopt.def', 'libgfortran.so.5', 'gmssb_ux.out', 'gmsprmun.txt', 'libpath50.so', 'libgdxcclib64.so', 'gevopt.def', 'gmscvnux.out', 'gmsgenus.run', 'libcplex.so', 'gams', 'libscncclib64.so', 'gamslice.txt', 'libgomp.so.1', 'optcplex.def', 'gmssb_us.run', 'optconvert.def']

file_paths = [directory + os.sep + file for file in files]
