"""
G4PPYY : Geant4 - CPPYY library interface
=============

A wrapper module to handle automatic building of Geant4 python
bindings using CPPYY.

The module includes both a lazy loader to initialize Geant4 
classes on demand, as well as tools to support development 
of simple Geant4 applications in python.

Author: Patrick Stowell, Rob Foster
Date: 2024-12-06
License: MIT
"""

# First Load Handler
print("[G4PPYY] : Geant4 Python wrapper for CPPYY")
print("[G4PPYY] : Author: P. Stowell (p.stowell@sheffield.ac.uk)")
print("[G4PPYY] :         R. Foster")

# System Imports
import sys as _sys

# Add g4 library and set this module as parent
from . import _lazy_loader
_lazy_loader.set_top_level(__name__)

# Registration of cppyy wrapper to allow g4.include
from ._lazy_loader import lazy_include as include
from ._lazy_loader import lazy_load as load
from ._lazy_loader import cppyy


# Register python specific modules

# Standard Units
from . import SI 

# Pre-loading class registration
from . import register 

# Visualisation Tools
from . import vis

# Run Manager Helpers
from . import run 

# Macro Helpers
from .macros import *

# CPPYY Memory Management Helpers
from .destructor import *

# Jupyter Magic Helpers
from . import magic as _magic

# Global manager helpers
from . import managers as _managers

# Geometry Helpers
from . import builder

# Main Component Caller allowing g4.G4Box etc
def __getattr__(name : str):
    """ 
        Module level lazy loader, intercepts attr calls
        for the module allowing access of G4 variables through this
        e.g. g4ppyy.G4VisAttributes,
    
    Args:
        name (str): Name of the class in Geant4 or local module attribute

    Raises:
        AttributeError: If no class/object found in g4 or local module.

    Returns:
        object: CPPYY class/function binding or local attribute if present.
    """
    
    # First try to find locally
    try:
        return globals()[name]
    except:
        pass   

    # If not try to find it available in lazy loader
    try:
        globals()[name] =  _lazy_loader.__getattr__(name)

        current_module = _sys.modules[__name__]
        setattr(current_module, name, globals()[name])

        return _lazy_loader.__getattr__(name)
    except:
        pass  

    # If the attribute is not found, it isn't in cppyy, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Close out on successful completion
print("[G4PPYY] : Imported all definitions.")



