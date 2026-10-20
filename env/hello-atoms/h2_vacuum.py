#from ase.build import molecule
#from gpaw import GPAW, PW


# 1. Build a H2 molecule and put it in a box with vacuum around it 
#h2 = molecule("H2",  vacuum=1)

# 2. Attach GPAW as the calculator, specifying mode(Using the Plane-Wave mode 'PW') and xc='PBE'
#calc = GPAW(mode=PW(300), xc='PBE')
#h2.calc = calc

# 3. Print the potential energy
#potential_energy = h2.get_potential_energy()
#print(f"Potential Energy: {potential_energy} eV")



#ALTRNATIVE
from ase.build import molecule
from gpaw import GPAW, PW

vacuums = [2.5, 3.5]  # Å
print("vacuum_A  energy_eV")

for vac in vacuums:
    h2 = molecule("H2", vacuum=vac)
    h2.pbc=True 
    h2.calc = GPAW(mode=PW(300), xc="PBE")  # txt=None silences the log
    e = h2.get_potential_energy()
    print(f"{vac:8.1f}  {e:12.6f}")
