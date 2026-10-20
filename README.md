# Atoms to Architecture

26-week computational materials science project: MLIP benchmark, FEA surrogate, verified agent, digital twin.


## GPAW hello-world: H2 in a box
- GPAW 26.7.0 installs from conda-forge on Ubuntu 26.04 and runs a PW(300 eV), PBE single-point on H2. The SCF converges in 8 steps.
- Energies are "relative to reference atoms", not binding energies. Not compared with literature (not yet checked).
- Vacuum scan (eV): 1.0: -15.449940 | 1.5: -8.351266 | 2.0: -6.917087 | 2.5: -6.629410 | 3.5: -6.580476 | 5.0: -6.585325
- 1.0 Å is not trustworthy: the SCF briefly blew up (-364458 eV at iteration 3) and the cell is tiny. Cause not investigated.
- From 3.5 to 5.0 Å the energy changes by about 0.005 eV; from 2.5 to 3.5 Å it changes by about 0.05 eV.
- Convergence tolerance and chosen vacuum: <YOUR CHOICE AND REASON>
- pbc=True changed the reported periodicity and occupation smearing, but not the energy.
- Not done: H-H bond-length optimisation, cutoff convergence, literature comparison (Week 4).
