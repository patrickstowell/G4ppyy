from . import _base_visualiser
from . import mpl_visualiser as _mpl_visualiser
from . import k3d_visualiser as _k3d_visualiser
from . import _lazy_loader as _g4

_g4.include("G4VisExecutive.icc")
_g4.include("G4VisExecutive.hh")
_g4.include("G4String.hh")
_g4.G4VisExecutive
_g4.G4String

global gVisExecutive
gVisExecutive = None

global visManager
visManager = None

class JupyterVisExecutive(_g4.G4VisExecutive):
    def RegisterGraphicsSystems(self):
        try:
            self.k3d_graphics_system = _k3d_visualiser.K3DJupyterGraphicsSystem()
            self.RegisterGraphicsSystem(self.k3d_graphics_system)
        except:
            pass

        try:
            self.mpl_graphics_system = _mpl_visualiser.MPLJupyterGraphicsSystem()
            self.RegisterGraphicsSystem(self.mpl_graphics_system)
        except:
            pass

    def Start(self):
        print("Python-side Vis Activated.")

    def Finish(self):
        self.k3d_graphics_system.scenehandler.Finish() 



def register_graphics_systems():
    global gVisExecutive
    if gVisExecutive: 
        print("Vis Executive already set!")
        return gVisExecutive

    gVisExecutive = JupyterVisExecutive("quiet")
    gVisExecutive.Initialize()

    return gVisExecutive


def check_world(detector, 
                runManager=None, 
                visExecutive=None, 
                graphic_system="K3DJupyter"):

    if not runManager:
        runManager = _g4.gRunManager
    
    if not visExecutive:
        visExecutive = _g4.gVisExecutive

    from .macros import mc
    runManager.SetUserInitialization(detector)


    # run.GeometryHasBeenModified()
    runManager.InitializeGeometry()
    mcb = mc
    mcb.vis.open(graphic_system,"600x600-0+0")
    mcb.vis.drawVolume()
    mcb.vis.viewer.refresh()
    mcb.vis.viewer.set.autoRefresh(False)

_g4.G4VUserDetectorConstruction.check = check_world