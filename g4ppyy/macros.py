from . import _lazy_loader

class _macro_callback_handler:
    def __init__(self, base=""):
        self.rdir = base

    def __getattr__(self, key):
        return _macro_callback_handler(self.rdir.replace("_","-") + "/" + key)

    def __dir__(self):
        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        UImanager.ListCommands(self.rdir)
    
    def __call__(self, *args):
        callstr = self.rdir + " "
        for obj in args:
            callstr += str(obj) + " "

        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        
        with open("./.G4temp.cmd", "w") as f:
            f.write(callstr + "\n")
        f.close()
        
        UImanager.ExecuteMacroFile("./.G4temp.cmd")


def macro(callstr):
    UImanager = _lazy_loader.G4UImanager.GetUIpointer()
    
    with open("./.G4temp.cmd", "w") as f:
        f.write(callstr + "\n")
    f.close()
    
    UImanager.ExecuteMacroFile("./.G4temp.cmd")

mc = _macro_callback_handler()