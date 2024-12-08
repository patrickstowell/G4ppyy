"""
G4PPYY.managers : Easier interfaces to standard G4 Run Objects that benefit in global
=============

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

from . import _lazy_loader as _g4


# Central Run Manager
global RunManager
RunManager = _g4.G4RunManager()
_g4.assign("gRunManager", RunManager)


# NIST Material Manager
global NistManager
NistManager = _g4.G4NistManager.Instance()
_g4.assign("gNistManager", NistManager)


# Visualisation Tools
from . import vis as _vis

global VisExecutive
VisExecutive = _vis.register_graphics_systems()
_g4.assign("gVisExecutive", VisExecutive)



