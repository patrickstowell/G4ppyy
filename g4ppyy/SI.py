"""
G4PPYY.SI : Geant4 Standard Units
=============

SI Units wrapper to make it easier to import many units at once from Geant4.

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

# Load Geant4's units file
from . import _lazy_loader as lzl
lzl.include("G4SystemOfUnits.hh")

# Register all mains
cm = lzl.gbl.cm
mm = lzl.gbl.mm
m  = lzl.gbl.m
eV = lzl.gbl.eV
MeV = lzl.gbl.MeV
GeV = lzl.gbl.GeV
kg = lzl.gbl.kg
g = lzl.gbl.g
deg = lzl.gbl.deg
twopi = 360.*deg
