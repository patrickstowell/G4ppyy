import os 
from . import _lazy_loader as lzl
from . import vis as _vis

lzl.include("G4UserEventAction.hh")
lzl.include("G4UserRunAction.hh")
lzl.include("G4UserSteppingAction.hh")
lzl.include("G4UImanager.hh")
lzl.include("G4UIExecutive.hh")
lzl.include("G4VisExecutive.hh")

_SCRIPT_DIR = os.path.dirname(__file__)
_MACRO_DIR = os.path.dirname(__file__) + "/macros/"

def handle_interactive(gRunManager):
    gRunManager.Initialize()
    ui = lzl.G4UIExecutive(1,["test"])

    visManager = lzl.G4VisExecutive()
    visManager.Initialize()

    UImanager = lzl.G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/interactive_vis.mac")

    ui.SessionStart()


global handle_objects
handle_objects = []



def add_default_actions(gRunManager):
    evaction = lzl.G4UserEventAction()
    gRunManager.SetUserAction(evaction)

    runaction = lzl.G4UserRunAction()
    gRunManager.SetUserAction(runaction)

    stepaction = lzl.G4UserSteppingAction()
    gRunManager.SetUserAction(stepaction)

    global handle_objects
    handle_objects.append(evaction)
    handle_objects.append(runaction)
    handle_objects.append(stepaction)

global detector_hooks
detector_hooks = []

def register_detector_hooks(det):
    global detector_hooks
    detector_hooks.append(det)

def register_processor_hooks(det):
    register_detector_hooks(det)

def register_tracking_hooks(det):
    register_detector_hooks(det)
        

def supress_startup():
    UImanager = lzl.G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/jupyter_quiet.mac")

def quiet_initialize(gRunManager):
    supress_startup()
    gRunManager.Initialize()

def start_of_run_detectors():
    global detector_hooks
    for obj in detector_hooks:
        start_action = getattr(obj, "StartOfRunAction", None)
        if callable(start_action):
            start_action()

def end_of_run_detectors():
    
    for obj in detector_hooks:
        end_action = getattr(obj, "EndOfRunAction", None)
        if callable(end_action):
            end_action()
            
def handle_beam(gRunManager, events):
            
    gRunManager.Initialize()

    start_of_run_detectors()
            
    gRunManager.BeamOn(events)

    end_of_run_detectors()

# Tools to handle vis components
global visManager
visManager = None

global ui
ui = None

def draw_detectors():
    global detector_hooks
    for obj in detector_hooks:
        start_action = getattr(obj, "VisualizationAction", None)
        if callable(start_action):
            start_action()

def create_mpl_visualization(gRunManager):
    global visManager
    if not visManager:
        visManager = _vis.build("MPL", "quiet")
        print("Running initializer")

    global ui
    if not ui:
        ui = lzl.G4UIExecutive(1,["test"])

    UImanager = lzl.G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/mpljupyter_vis.mac")
    
def create_visualization(gRunManager, option="K3D"):
    global visManager
    if not visManager:
        visManager = _vis.register_graphics_systems()
        print("Running initializer")

    global ui
    if not ui:
        ui = lzl.G4UIExecutive(1,["test"])

    UImanager = lzl.G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/jupyter_vis.mac")

def draw_visualization(gRunManager):

    if visManager:
        visManager.Finish()

    draw_detectors()
    

    
    