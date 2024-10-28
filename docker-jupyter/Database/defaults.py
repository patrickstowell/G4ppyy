from g4ppyy import build_material
from g4ppyy import eV

water = build_material("G4_WATER",
                       RINDEX_X=[0.1*eV, 100*eV],
                       RINDEX_Y=[1.33, 1.33])

hdpe  = build_material("G4_POLYETHYLENE")

