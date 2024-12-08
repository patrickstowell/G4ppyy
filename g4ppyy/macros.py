"""
G4PPYY.macros : Geant4 Macro Helpers G4ppyy
=============

Python based helper layer to make it easier to build and run macros
directly inside a jupyter or python script.

The macro_callback_handler can be used to build calls.

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

# G4ppyy imports (require use of uimanagers)
from . import _lazy_loader


class _macro_callback_handler:
    """Callback helper tool that loops back on itself to allow
    macros to be built on the fly.

    e.g. g4.mc.run.beamOn(1000) is equivalent to /run/beamOn 1000
    """
    def __init__(self, base=""):
        """Constructor, uses base as a starting prepended input

        Args:
            base (str, optional): path input to start with. Defaults to "".
        """
        self.path = base

    def __getattr__(self, key):
        """Get attribute produces a new handler that loops back on itself

        Args:
            key (str): New key value to add, equivalent to /arg/ in a macro.

        Returns:
            _macro_callback_handler: Extended callback allowing cb.vis.trajectories, etc.
        """
        return _macro_callback_handler(self.path.replace("_","-") + "/" + key)

    def help(self):
        """Calling help on the macro prints list of available commands for the current path.
        """
        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        UImanager.ListCommands(self.path)
    
    def __call__(self, *args):
        """Main operator for the callback, which runs it int he G4UiManager

        Arguments correspond to a list of arguments in the original g4 Macro.
        .build.Box(5,5,5,cm)
        """
        callstr = self.path + " "
        for obj in args:
            callstr += str(obj) + " "

        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        
        with open("./.G4temp.cmd", "w") as f:
            f.write(callstr + "\n")
        f.close()
        
        UImanager.ExecuteMacroFile("./.G4temp.cmd")


def macro(callstr):
    """Single larger macro call across many lines

    Args:
        callstr (str): Many line macro
    """
    UImanager = _lazy_loader.G4UImanager.GetUIpointer()
    
    with open("./.G4temp.cmd", "w") as f:
        f.write(callstr + "\n")
    f.close()
    
    UImanager.ExecuteMacroFile("./.G4temp.cmd")

def build_macro_callback():
    return _macro_callback_handler()

mc = build_macro_callback()