"""
G4PPYY._lazy_loader : Geant4 Loading interface for G4ppyy
=============

Automated library loading tool setup to query geant4-config
and use this to auto load the Geant4 requirements.

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

# System Imports
import os as _os
import glob as _glob
import cppyy
import sys as _sys

# Module-level constants
global _G4PREFIX
_G4PREFIX = "WARNING_NOT_SET"

global _TOPLEVEL
_TOPLEVEL = ""

# -----------------------
# CPPYY
# -----------------------

# Add wrappers around cppyy just to make g4ppyy functions easier.
gbl = cppyy.gbl
include = cppyy.include

# -----------------------
# HELPERS
# -----------------------
# Helper function for fixing global
def set_top_level(name):
    """Set the top level module to be `name` for the attribute handler"""
    global _TOPLEVEL
    _TOPLEVEL = name

# Simple external command call
def ext_cmd(cmd : str):
    """Calls an external command with subprocess and parses the result

    Args:
        cmd (str): Full command as string

    Returns:
        str: STDOUT of main function call from the command line
    """
    import subprocess
    process = subprocess.Popen(cmd.split(" "), 
                    stdout=subprocess.PIPE)
    (lib_output, err) = process.communicate()
    exit_code = process.wait()

    return str(lib_output.decode()).strip()

# -----------------------
# GEANT4 IMPORTS
# -----------------------
# Code below is one long processing chain
print("[G4PPYY] : Loading G4 Modules.")

# Check geant4-config present
def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


if not is_tool("geant4-config"):
    # print("[G4PPYY] : ERROR : geant4-config not found. Is GEANT4 setup?")
    raise RuntimeError("ERROR : geant4-config not found. Is GEANT4 setup?")


# Get GEANT4 PREFIX
_G4PREFIX = ext_cmd("geant4-config --prefix")
print(f"[G4PPYY] : G4PREFIX : {_G4PREFIX}")

# Get GEANT4 Version and check valid
_G4VERSION = ext_cmd("geant4-config --version")
print(f"[G4PPYY] : G4VERSION : {_G4VERSION}")

if (int(_G4VERSION.split(".")[0]) < 11):
    raise RuntimeError("ERROR : Only tested in G4 4.11.xx")

# Add main include + lib DIRS
_G4INCLUDE_PATH=f'{_G4PREFIX}/include/Geant4/'
if (not _os.path.isdir(_G4INCLUDE_PATH)):
    raise RuntimeError(f"Failed to find Geant4 include path : {_G4INCLUDE_PATH}")

try:
    cppyy.add_include_path(_os.path.abspath(f'{_G4PREFIX}/include/Geant4/'))
except:
    raise RuntimeError(f"Failed to add Geant4 include path to cppyy : {_G4INCLUDE_PATH}")

# Add library locations
_G4LOAD_PATH=f'{_G4PREFIX}/lib64/'
if (_os.path.isdir(_G4LOAD_PATH)):
    cppyy.add_library_path(_os.path.abspath(_G4LOAD_PATH))

_G4LOAD_PATH=f'{_G4PREFIX}/lib/'
if (_os.path.isdir(_G4LOAD_PATH)):
    cppyy.add_library_path(_os.path.abspath(_G4LOAD_PATH))


# Consider additional include folders
if "G4PPYY_INCLUDE_DIRS" in _os.environ:
    for dirs in str(_os.environ["G4PPYY_INCLUDE_DIRS"]).split(":"):
        if _os.path.isdir(dirs):
            if len(dirs) > 0:
                cppyy.add_include_path(dirs)

# Consider additional precomp files
if "G4PPYY_INCLUDE_FILES" in _os.environ:
    for fname in str(_os.environ["G4PPYY_INCLUDE_FILES"]).split(":"):
        if len(fname) > 0:
            cppyy.include(fname)

# Consider additional library folders
if "G4PPYY_LIBRARY_DIRS" in _os.environ:
    for dirs in str(_os.environ["G4PPYY_LIBRARY_DIRS"]).split(":"):
        if _os.path.isdir(dirs):
            if len(dirs) > 0:
                cppyy.add_library_path(dirs)

# Consider additional library files
if "G4PPYY_LIBRARY_FILES" in _os.environ:
    for fname in str(_os.environ["G4PPYY_LIBRARY_FILES"]).split(":"):
        if len(fname) > 0:
            cppyy.load_library(fname)


# Load Libraries (recursively if required)
def _load_g4_libraries():
    """Attempts to load all libraries quoted in geant4-config --libs
    """
        
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

# Call the library handler
_load_g4_libraries()

# Load all virtual files
for file in _glob.glob("{_G4PREFIX}/include/Geant4/G4V*.hh"):
    try:
        cppyy.include(file)
    except:
        pass

# -----------------------
# LAZY LOADER DEFINITIONS
# -----------------------

# Adds headers to CPPYY for access
def lazy_include(name):
    """Adds a specific file by name

    Args:
        name (str): Geant4 header file
    """
    try:
        cppyy.include(name)
    except:
        pass


# Attempts to find the corresponding GEANT4 Header File
def lazy_load(name, g4dir="{_G4PREFIX}/include/Geant4/"):
    """Helper function that attempts to find the corresponding header file for a class
    based on usual G4 structures. E.g. G4Box in G4Box.hh

    Args:
        name (str): Class name
        g4dir (str, optional): Path to search in. Defaults to "{_G4PREFIX}/include/Geant4/".
    """
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
    """ 
        Module level lazy loader, intercepts attr calls
        for the module allowing access of G4 variables through this
        e.g. lazy_loader.G4VisAttributes,
    
    Args:
        name (str): Name of the class in Geant4 or local module attribute

    Raises:
        AttributeError: If no class/object found in g4 or local module.

    Returns:
        object: CPPYY class/function binding or local attribute if present.
    """

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
    """Lazy registration for a function considering the `name`.hh

    Args:
        name (str): Object name

    Returns:
        object: Cppyy binding object if found
    """
    lazy_include(name + ".hh")
    return __getattr__(name)    


# Assign as a local to consider g4.G4Box
def assign(name, obj):
    """Assigns an object as an attribute to the module

    Args:
        name (str): Name to set the attr to
        obj (object): Bound object to be assigned
    """
    current_module = _sys.modules[__name__]
    setattr(current_module, name, obj)

    top_module = _sys.modules[_TOPLEVEL]
    setattr(top_module, name, obj)

print("[G4PPYY] : Module loading complete.")
