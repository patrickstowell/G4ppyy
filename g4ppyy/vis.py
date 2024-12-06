from . import _base_visualiser
from . import _mpl_visualiser 
from . import _k3d_visualiser 
from . import _lazy_loader

global gVisExecutive
gVisExecutive = None

_lazy_loader.include("G4VisExecutive.icc")
_lazy_loader.include("G4VisExecutive.hh")
_lazy_loader.include("G4String.hh")
_lazy_loader.G4VisExecutive
_lazy_loader.G4String


global visManager
visManager = None

def build(option, settings):
    global gVisExecutive

    if gVisExecutive: 
        print("Vis Executive already set!")
        return gVisExecutive

    if option == "K3D":    
        gVisExecutive = _k3d_visualiser.K3DJupyterVisExecutive("quiet")
        gVisExecutive.Initialize()
        _lazy_loader.assign("gVisExecutive", gVisExecutive)

    return gVisExecutive

