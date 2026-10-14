from ase.build import bulk
from ase.calculators.emt import EMT
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS

# 1. Build a Cu FCC cube. cubic=True gives the full cube, not the smaller primitive cell
atoms = bulk("Cu", "fcc", a=3.8, cubic=True)
print("Start: a =", atoms.cell.cellpar()[0], "A")

# 2. Attach the rulebook that gives energy and forces
atoms.calc = EMT()

# 3. Allow the cube itself to change size, to change size, not just the atoms inside of it
relax_target = FrechetCellFilter(atoms)

# 4. Run the optimizer until forces are tiny (below 0.01 eV/A)
optimiser = BFGS(relax_target)
optimiser.run(fmax=0.01)

# 5. Report the result
print("Result: a=", atoms.cell.cellpar()[0], "A")
print("Energy =", atoms.get_potential_energy(), "eV")
