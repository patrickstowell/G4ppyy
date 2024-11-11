import os as _os
import glob as _glob
import cppyy
import sys as _sys

global _G4PREFIX
_G4PREFIX = "WARNING_NOT_SET"

global _TOPLEVEL
_TOPLEVEL = ""

# -----------------------
# HELPERS
# -----------------------

def set_top_level(name):
    global _TOPLEVEL
    _TOPLEVEL = name

# Simple external command call
def ext_cmd(cmd):
    import subprocess
    process = subprocess.Popen(cmd.split(" "), 
                    stdout=subprocess.PIPE)
    (lib_output, err) = process.communicate()
    exit_code = process.wait()

    return str(lib_output.decode()).strip()

# -----------------------
# GEANT4 IMPORTS
# -----------------------
print("[G4PPYY] : Loading G4 Modules.")

# Check geant4-config present
def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

if not is_tool("geant4-config"):
    print("[G4PPYY] : ERROR : geant4-config not found. Is GEANT4 setup?")
    raise RuntimeError

# Get GEANT4 PREFIX
_G4PREFIX = ext_cmd("geant4-config --prefix")
print(f"[G4PPYY] : G4PREFIX : {_G4PREFIX}")

_G4VERSION = ext_cmd("geant4-config --version")
print(f"[G4PPYY] : G4VERSION : {_G4VERSION}")

if (int(_G4VERSION.split(".")[0]) < 11):
    print("[G4PPYY] : ERROR : Only tested in G4 4.11.xx")
    raise RuntimeError

# Add include + lib DIRS
try:
    cppyy.add_include_path(_os.path.abspath(f'{_G4PREFIX}/include/Geant4/'))
except:
    pass

try:
    cppyy.add_library_path(_os.path.abspath(f"{_G4PREFIX}/lib64/"))
except:
    pass

try:
    cppyy.add_library_path(_os.path.abspath(f"{_G4PREFIX}/lib/"))
except:
    pass


# _os.environ["LD_LIBRARY_PATH"] = _os.environ["LD_LIBRARY_PATH"] + ":" + f'{_G4PREFIX}/lib64/'
# _os.environ["LD_LIBRARY_PATH"] = _os.environ["LD_LIBRARY_PATH"] + ":" + f'{_G4PREFIX}/lib64/'

# Load Libraries (recursively if required)
def _load_g4_libraries():
        
    lib_output = ext_cmd("geant4-config --libs")

    vals = lib_output.split()
    lib_dir = vals[0].replace("-L","")

    libraries = []
    for x in vals[1:]:
        libraries.append( x.replace("-l","") )

    count = 0
    while len(libraries) > 0 and count < 5:
        remaining = []
        for val in libraries:
            try:
                cppyy.load_library(val)        
            except:
                remaining.append(val)

        if (len(remaining) > 0):
            print("[G4PPYY] : Failed to load : ", remaining, len(remaining))
            
        libraries = remaining
        count += 1

_load_g4_libraries()

# -----------------------
# LAZY LOADER DEFINITIONS
# -----------------------

# Adds headers to CPPYY for access
def lazy_include(name):
    try:
        cppyy.include(name)
    except:
        pass

# Attempts to find the corresponding GEANT4 Header File
def lazy_load(name, g4dir="{_G4PREFIX}/include/Geant4/"):

    if not isinstance(name, list):
        name = [name]
        
    for n in name:
        for file in _glob.glob(g4dir + "/" + n):
            file = (file.replace(g4dir,""))
            classname = file.replace(".hh","")
            try:
                cppyy.gbl.include(file)
            except:
                pass

            try:
                __getattr__(classname)
            except:
                pass
    

# Module level lazy loader, intercepts attr calls
# for the module allowing for access of G4 variables through this
# e.g. g4ppyy.G4VisAttributes,
def __getattr__(name):
    
    try:
        return globals()[name]
    except:
        pass   

    # Run slightly dodgy eval, needs to be replaced
    # with a scopped attribute check
    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        current_module = _sys.modules[__name__]
        setattr(current_module, name, globals()[name])

        top_module = _sys.modules[_TOPLEVEL]
        setattr(top_module, name, globals()[name])
        
        return globals()[name]
    except AttributeError:
        pass

    try:
        cppyy.include(name + '.hh')
    except:
        pass

    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        current_module = _sys.modules[__name__]
        setattr(current_module, name, globals()[name])

        top_module = _sys.modules[_TOPLEVEL]
        setattr(top_module, name, globals()[name])

        return globals()[name]
    except AttributeError:
        pass
    
    # If the attribute is not found, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Simplified register for standard headers
def lazy_register(name):
    lazy_include(name + ".hh")
    return __getattr__(name)    

def assign(name, obj):
    current_module = _sys.modules[__name__]
    setattr(current_module, name, obj)

    top_module = _sys.modules[_TOPLEVEL]
    setattr(top_module, name, obj)

# Add wrappers around cppyy just to make g4ppyy functions easier.
gbl = cppyy.gbl
include = cppyy.include

print("[G4PPYY] : Module loading complete.")
