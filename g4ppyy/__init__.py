print("[G4PPYY] : Geant4 Python wrapper for CPPYY")
print("[G4PPYY] : author: P. Stowell")
import sys as _sys

from . import _lazy_loader
from ._lazy_loader import lazy_include as include
from ._lazy_loader import lazy_load as load
from ._lazy_loader import cppyy

_lazy_loader.set_top_level(__name__)

# Module level lazy loader, intercepts attr calls
# for the module allowing for access of G4 variables through this
# e.g. g4ppyy.G4VisAttributes,
def __getattr__(name):
    
    try:
        return globals()[name]
    except:
        pass   

    try:
        globals()[name] =  _lazy_loader.__getattr__(name)
        current_module = _sys.modules[__name__]
        setattr(current_module, name, globals()[name])
        return _lazy_loader.__getattr__(name)
    except:
        pass  

    # If the attribute is not found, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


from . import SI 

# from ._bindings import *

from . import register 

from . import run 

from . import vis

from . import builder

print("[G4PPYY] : Imported all definitions.")



