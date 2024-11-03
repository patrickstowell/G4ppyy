import os 

_SCRIPT_DIR = os.path.dirname(__file__)
_MACRO_DIR = os.path.dirname(__file__) + "/macros/"

def handle_interactive(gRunManager):
    gRunManager.Initialize()
    ui = G4UIExecutive(1,["test"])

    visManager = G4VisExecutive()
    visManager.Initialize()

    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/interactive_vis.mac")

    ui.SessionStart()


global handle_objects
handle_objects = []

def add_default_actions(gRunManager):
    evaction = G4UserEventAction()
    gRunManager.SetUserAction(evaction)

    runaction = G4UserRunAction()
    gRunManager.SetUserAction(runaction)

    stepaction = G4UserSteppingAction()
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
    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/jupyter_quiet.mac")

def quiet_initialize(gRunManager):
    supress_startup()
    gRunManager.Initialize()

def handle_beam(gRunManager, events):
            
    gRunManager.Initialize()

    global detector_hooks
    for obj in detector_hooks:
        start_action = getattr(obj, "StartOfRunAction", None)
        if callable(start_action):
            start_action()
            
    gRunManager.BeamOn(events)

    for obj in detector_hooks:
        end_action = getattr(obj, "EndOfRunAction", None)
        if callable(end_action):
            end_action()


# Tools to handle vis components
global visManager
visManager = None

global ui
ui = None

def create_visualization(gRunManager):
    global visManager
    if not visManager:
        visManager = PyCRUSTVisExecutive("quiet")
        visManager.Initialize()

    global ui
    if not ui:
        ui = G4UIExecutive(1,["test"])

    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(_MACRO_DIR + "/jupyter_vis.mac")

def draw_visualization(gRunManager):
    

    global detector_hooks
    for obj in detector_hooks:
        start_action = getattr(obj, "VisualizationAction", None)
        if callable(start_action):
            start_action()
