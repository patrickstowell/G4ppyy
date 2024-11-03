from . import _base_visualiser
# from . import _mpl_visualiser as mplvis
from . import _k3d_visualiser 
from . import _lazy_loader

global gVisExecutive
gVisExecutive = None

def build(option, settings):
    global gVisExecutive

    _lazy_loader.assign("gVisExecutive", gVisExecutive)

    if gVisExecutive: 
        print("Vis Executive already set!")
        return

    if option == "K3D":    
        gVisExecutive = _k3d_visualiser.K3DJupyterVisExecutive(settings)
        gVisExecutive.Start()

