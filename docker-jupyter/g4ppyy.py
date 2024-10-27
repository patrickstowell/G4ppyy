import cppyy

# global g4_imported
# if not g4_imported:
#     g4_imported = True
#     print("Importing GEANT4")

# Intercepts attribute access for this module
def __getattr__(name):
    
    if name in globals():
      return globals()[name]
    
    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        return cppyy.gbl.hasattr(name)
    except AttributeError:
        pass

    try:
        cppyy.include(name + '.hh')
    except:
        pass

    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        return globals()[name]
    except AttributeError:
        pass
    
    # If the attribute is not found, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    
from subprocess import Popen, PIPE
import os
import glob

def lazy_load(name, g4dir="/app/Geant4-11.2.2-Linux/include/Geant4/"):

    if not isinstance(name, list):
        name = [name]
        
    for n in name:
        for file in glob.glob(g4dir + "/" + n):
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
    


from subprocess import Popen, PIPE
import os

print("GEANT4 : Loading modules")
twopi = 2*3.14159 

#cppyy.include('/data/test.hh')
cppyy.add_include_path(os.path.abspath('/app/Geant4-11.2.2-Linux/include/Geant4/'))
os.environ["LD_LIBRARY_PATH"] = '/app/Geant4-11.2.2-Linux/lib64/'

process = Popen(["geant4-config", "--libs"], stdout=PIPE)
(lib_output, err) = process.communicate()
exit_code = process.wait()

vals = (str(lib_output.decode()).split())
lib_dir = vals[0].replace("-L","")

libraries = []
for x in vals[1:]:
    libraries.append( x.replace("-l","") )
# libraries.reverse()

# print(lib_dir, libraries)

cppyy.add_library_path(os.path.abspath("/app/Geant4-11.2.2-Linux/lib64/"))


count = 0
while len(libraries) > 0 and count < 5:
    remaining = []
    for val in libraries:
        # try:
        # cppyy.load_library(lib_dir + "/lib" + val + ".dylib")
        cppyy.load_library(val)
        # print("Loading", val)
        
        # except:
            # remaining.append(val)
    if (len(remaining) > 0):
        print("remaining : ", remaining, len(remaining))
    libraries = remaining
    count += 1

#cppyy.load_library("libG4visQt3D.dylib")
print("GEANT4 : Loading complete.")


cppyy.include('G4UImanager.hh')
cppyy.include('G4UIterminal.hh')

cppyy.include('G4VisExecutive.hh')
cppyy.include('G4VisExecutive.icc')

cppyy.include('G4UItcsh.hh')
cppyy.include('Randomize.hh')
cppyy.include('globals.hh')
cppyy.include('G4VisExecutive.hh')
cppyy.include('G4UIExecutive.hh')
cppyy.include("G4ParticleTable.hh")
cppyy.include("G4String.hh")
G4String = cppyy.gbl.G4String

cppyy.include("G4ParticleGun.hh")
G4ParticleGun = cppyy.gbl.G4ParticleGun

cppyy.include('QGSP_BERT.hh')
QGSP_BERT = cppyy.gbl.QGSP_BERT

cppyy.include('QGSP_BERT_HP.hh')
QGSP_BERT_HP = cppyy.gbl.QGSP_BERT_HP

cppyy.include("G4VUserPrimaryGeneratorAction.hh")
G4VUserPrimaryGeneratorAction = cppyy.gbl.G4VUserPrimaryGeneratorAction

cppyy.include('G4RunManager.hh')
G4RunManager = cppyy.gbl.G4RunManager

cppyy.include('G4LogicalVolume.hh')
G4LogialVolume = cppyy.gbl.G4LogicalVolume

cppyy.include('G4Material.hh')
G4Material = cppyy.gbl.G4Material

cppyy.include('G4VPhysicalVolume.hh')
G4VPhysicalVolume = cppyy.gbl.G4VPhysicalVolume

cppyy.include('G4PVPlacement.hh')
G4PVPlacement = cppyy.gbl.G4PVPlacement

cppyy.include('G4NistManager.hh')
global gNistManager
gNistManager = cppyy.gbl.G4NistManager.Instance()

cppyy.include('G4VUserDetectorConstruction.hh')
G4VUserDetectorConstruction = cppyy.gbl.G4VUserDetectorConstruction


cppyy.include("G4ThreeVector.hh")
G4ThreeVector = cppyy.gbl.G4ThreeVector

cppyy.include("G4RotationMatrix.hh")
G4RotationMatrix = cppyy.gbl.G4RotationMatrix

cppyy.include("G4UserEventAction.hh")
G4UserEventAction = cppyy.gbl.G4UserEventAction

cppyy.include("G4UserSteppingAction.hh")
G4UserSteppingAction = cppyy.gbl.G4UserSteppingAction

cppyy.include("G4UserRunAction.hh")
G4UserRunAction = cppyy.gbl.G4UserRunAction

#cppyy.include("G4ParticleTable.hh")
#cppyy.gbl.G4ParticleTable.GetParticleTable()

cppyy.include("G4ParticleDefinition.hh")
G4ParticleDefinition = cppyy.gbl.G4ParticleDefinition

cppyy.include("G4Neutron.hh")
cppyy.include("G4Proton.hh")
cppyy.include("G4Electron.hh")
cppyy.include("G4MuonMinus.hh")
cppyy.include("G4MuonPlus.hh")

from cppyy.gbl import G4Neutron, G4Proton, G4Electron, G4MuonMinus, G4MuonPlus

NULL = cppyy.nullptr

cppyy.include("G4RunManagerFactory.hh")
G4RunManagerFactory = cppyy.gbl.G4RunManagerFactory

cppyy.include("G4VSensitiveDetector.hh")
G4VSensitiveDetector = cppyy.gbl.G4VSensitiveDetector


cppyy.include("G4TrackStatus.hh")
G4TrackStatus = cppyy.gbl.G4TrackStatus
G4UImanager = cppyy.gbl.G4UImanager
G4VisExecutive = cppyy.gbl.G4VisExecutive
G4UIExecutive = cppyy.gbl.G4UIExecutive



def handle_raytrace(gRunManager):
    gRunManager.Initialize()
    ui = G4UIExecutive(1,["test"])

    visManager = G4VisExecutive()
    visManager.Initialize()

    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile("macros/raytracer.mac")

    ui.SessionStart()



def handle_interactive(gRunManager):
    gRunManager.Initialize()
    ui = G4UIExecutive(1,["test"])

    visManager = G4VisExecutive()
    visManager.Initialize()

    UImanager = G4UImanager.GetUIpointer()
    UImanager.ApplyCommand("/control/execute init_vis.mac")

    ui.SessionStart()


def handle_beam(gRunManager, events):
    gRunManager.Initialize()
    gRunManager.BeamOn(events)



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



class World(G4VUserDetectorConstruction):
    def __init__(self, world_obj):
        super().__init__()
        self.physical = world_obj
        
    def Construct(self):
        return self.physical
    

def GetMaterial(name):
    return gNistManager.FindOrBuildMaterial(name)

cppyy.include("G4SystemOfUnits.hh")

from cppyy.gbl import cm, mm, m, eV, MeV, GeV, kg, g



cppyy.include("G4Element.hh")
from cppyy.gbl import G4Element









# Material Helpers
def material_from_elements(name : str,
                            density : float,
                            elements : list[str, G4Element],
                            fractions : list[int]):
    
    if (gNistManager.FindOrBuildMaterial(name)): 
        return gNistManager.FindOrBuildMaterial(name)
        
    mat = G4Material(name, density, len(elements))
    
    for e,f in zip(elements, fractions):
        if (isinstance(e, str)):
            
            e = gNistManager.FindOrBuildElement(e)
        if (e):
            mat.AddElement(e, f)

    return mat


def material_from_materials(name : str,
                            density : float,
                            materials : list[str, G4Material],
                            fractions : list[int]):
    if (gNistManager.FindOrBuildMaterial(name)): 
        return gNistManager.FindOrBuildMaterial(name)
        
    mat = G4Material(name, density, len(materials))

    for i, (m, f) in enumerate(zip(materials, fractions)):
        if (isinstance(m, str)):
            m = gNistManager.FindOrBuildMaterial(m)
        if (m):
            mat.AddMaterial(m, f)
        else:
            raise Exception(f"Failed to load material {i}")

    return mat

def material_from_store(name : str):
    if gNistManager.FindOrBuildMaterial(name):
        return gNistManager.FindOrBuildMaterial(name)
    else: 
        return None

cppyy.include("G4MaterialPropertiesTable.hh")
from cppyy.gbl import G4MaterialPropertiesTable

import numpy as np

def update_table_properties(table, properties):

    constants = ["SCINTILLATIONTIMECONSTANT1", "SCINTILLATIONYIELD", "RESOLUTIONSCALE", "MIEHG_FORWARD_RATIO", "MIEHG_FORWARD", 
"MIEHG_BACKWARD" ]
    for key in constants:
        if key in properties:
            table.AddConstProperty(key, properties[key])
            
    dynamics = ["RINDEX", "ABSLENGTH", "SCINTILLATIONCOMPONENT1", "ABSLENGTH", "RAYLEIGH", "MIEHG" ]
    for key in dynamics:

        if key+"_X" in properties and key+"_Y" in properties:

            xv = properties[key+"_X"]
            yv = properties[key+"_Y"]
            
            table.AddProperty(key, 
                            np.array(xv),
                            np.array(yv), 
                            len(xv))



def build_vis(col=[1.0,0.0,0.0,0.5], visible=True, drawstyle="wireframe"):
    
    vis = G4VisAttributes()
    gVisAttributes.append(vis)
    
    vis.SetVisibility(visible)
    if drawstyle == "solid":
        vis.SetForceSolid(1)
        vis.SetForceWireframe(0)
    else:
        vis.SetForceSolid(0)
        vis.SetForceWireframe(1)
    if len(col) <= 3:
        col.append(1.0)
        
    vis.SetColor(G4Color(col[0],col[1],col[2], col[3]))

    return vis


material_vis_mapping = {}
def set_material_vis(name, col=[1.0,0.0,0.0,0.5], visible=True, drawstyle="wireframe"):
    vv = build_vis(vol, visible, drawstyle)
    material_vis_mapping[name] = vv
    
tables = []

def set_material_properties(material, data : dict):  

    tab = material.GetMaterialPropertiesTable()
    update_found = False
    if tab == None:
        update_found = True
        tab = G4MaterialPropertiesTable()
        tables.append(tab)
                
    properties = {}
    data_found = False
    for p in data:
        if p == p.upper() and data[p]:
            properties[p] = data[p]
            data_found = True

    for key in properties:
        if "_X" in key:
            xv = properties[key]
            yv = properties[key.replace("_X","_Y")]

            vals = sorted(zip(xv, yv))
            xv, yv = zip(*vals)
            properties[key] = xv
            properties[key.replace("_X","_Y")] = yv

                        
    if data_found:
        update_table_properties(tab, properties)

    if update_found:
        material.SetMaterialPropertiesTable(tab)

    
    

global material_store
material_store = {}

def build_material(name: str, 
             density: float = None, 
             elements: list[str, G4Element] = None, 
             materials: list[str, G4Material] = None, 
             fractions : list[float] = None,
             col = None,
             visible = None,
             drawstyle = None,
             SCINTILLATIONTIMECONSTANT1 : float = None,
             SCINTILLATIONTIMECONSTANT2 : float = None,
             SCINTILLATIONYIELD : float = None,
             RESOLUTIONSCALE : float = None,
             ABSLENGTH_X : list[float] = None,
             ABSLENGTH_Y : list[float] = None,
             RINDEX_X : list[float] = None,
             RINDEX_Y : list[float] = None,
             SCINTILLATIONCOMPONENT1_X : list[float] = None,
             SCINTILLATIONCOMPONENT1_Y : list[float] = None,
             SCINTILLATIONCOMPONENT2_X : list[float] = None,
             SCINTILLATIONCOMPONENT2_Y : list[float] = None,
             WLSTIMECONSTANT : float = None,
             WLSCOMPONENT_X : list[float] = None, 
             WLSCOMPONENT_Y : list[float] = None,
             RAYLEIGH_X : list[float] = None, 
             RAYLEIGH_Y : list[float] = None,
             MIEHG_X : list[float] = None, 
             MIEHG_Y : list[float] = None,
             MIEHG_FORWARD_RATIO : float = None,
             MIEHG_FORWARD : float = None,
             MIEHG_BACKWARD : float = None,
             WLSABSLENGTH_X: list[float] = None,
             WLSABSLENGTH_Y: list[float] = None):

    material = None
    if elements and not materials:
        material = material_from_elements(name, density, elements, fractions) 
    elif not elements and materials:
        material = material_from_materials(name, density, materials, fractions)
    else:
        if name in material_store and material_store[name]: material = material_store[name]
        else: material = material_from_store(name)

    if not material: return None

    material_store[name] = material
    set_material_properties(material, locals())

    if col or drawstyle or visible:
        set_material_vis(name, col, visible, drawstyle)
        
    return material





# @beartype
def position(x : (float, int) = 0.0,
             y : (float, int) = 0.0,
             z : (float, int) = 0.0):
    return [float(x),float(y),float(z)]

# @beartype
def rotation(xy : (float, int) = 0.0,
             xz : (float, int) = 0.0,
             yz : (float, int) = 0.0):
    return [float(xy),float(xz),float(yz)]




cppyy.include("G4Box.hh")
cppyy.include("G4Sphere.hh")
cppyy.include("G4Tubs.hh")
cppyy.include("G4VSolid.hh")


from cppyy.gbl import G4VSolid


def G4Box(name, 
          x : float = 1.0*m, 
          y : float = 1.0*m, 
          z : float = 1.0*m):
    return cppyy.gbl.G4Box(name, 
                           x, 
                           y, 
                           z)
    
def G4Sphere(name, 
             rmin : float = 0.0, 
             rmax : float = 1.0*m, 
             phimin : float = 0.0, 
             phimax : float = twopi, 
             thetamin : float = 0.0, 
             thetamax : float = twopi):
    return cppyy.gbl.G4Sphere(name, 
                              rmin, 
                              rmax, 
                              phimin, 
                              phimax, 
                              thetamin, 
                              thetamax)

def G4Tubs(name, 
           rmin : float = 0.0, 
           rmax : float = 1.0*m, 
           zmax : float = 1.0*m, 
           phimin : float = 0.0, 
           phimax : float = twopi):
    return cppyy.gbl.G4Tubs(name, 
                            rmin, 
                            rmax, 
                            zmax, 
                            phimin, 
                            phimax)


global gSolidList
gSolidList = {}
def build_solid(name  : str,
                solid : str,
                x: float = 1,
                y: float = 1,
                z: float = 1,
                rmin : float = 0, 
                rmax : float = 1, 
                phimin : float = 0, 
                phimax : float = twopi, 
                thetamin : float = 0, 
                thetamax : float = twopi):
    """
        box(name, x, y, z)
        sphere(name, rmin, rmax, phimin, phimax, thetamin, thetamax)
        tubs(name, rmin, rmax, zmax/2, phimin, phimax)
    """
    
    if "box" in solid.lower(): 
        obj = G4Box(name, x, y, z)
        
    if "sphere" in solid.lower(): 
        obj = G4Sphere(name, rmin, rmax, 
                       phimin, phimax, thetamin, thetamax)
        
    if "tubs" in solid.lower(): 
        obj = G4Tubs(name, rmin,
                     rmax, z, phimin, phimax)

    gSolidList[name] = obj
    return obj


cppyy.include("G4VPhysicalVolume.hh")
cppyy.include("G4LogicalVolume.hh")
cppyy.include("G4VisAttributes.hh")


cppyy.include("G4Color.hh")

from cppyy.gbl import G4VPhysicalVolume
from cppyy.gbl import G4LogicalVolume
from cppyy.gbl import G4VisAttributes
from cppyy.gbl import G4Color





gVisAttributes = []
def vis(detector, col, visible=True, drawstyle="wireframe"):
    
    vis = G4VisAttributes()
    gVisAttributes.append(vis)
    
    vis.SetVisibility(visible)
    if drawstyle == "solid":
        vis.SetForceSolid(1)
        vis.SetForceWireframe(0)
    else:
        vis.SetForceSolid(0)
        vis.SetForceWireframe(1)
    if len(col) <= 3:
        col.append(1.0)
        
    vis.SetColor(G4Color(col[0],col[1],col[2], col[3]))

    if isinstance(detector, G4VPhysicalVolume):
        detector.GetLogicalVolume().SetVisAttributes(vis)
    else:
        detector.SetVisAttributes(vis)
    

global gLogicalList 
gLogicalList = []

def build_logical(name : str,
          solid : (str, G4VSolid) = None,
          material: (str, G4Material) = None,
          x: float = 1,
          y: float = 1,
          z: float = 1,
          rmin : float = 0, 
          rmax : float = 1, 
          phimin : float = 0, 
          phimax : float = twopi, 
          thetamin : float = 0, 
          thetamax : float = twopi,
          color: list[float,int] = [1.0,0.0,0.0,1.0],
          visible: bool = True,
          drawstyle: str = "wireframe"):

    if isinstance(solid, str):
        solid = build_solid(name, solid, x, y, z, rmin, rmax, phimin, phimax, thetamin, thetamax)

    if isinstance(material, str):
        material = build_material(material)

    log = G4LogicalVolume(solid, material, name)
    gLogicalList.append(log)

    # Move to overriding drawstyles.        
    vis(log, color, visible, drawstyle)
    gSolidList[name + "_logical"] = log
    
    return log

global gComponentList
gComponentList = []

def build_component(name : str,
              solid : (str, G4VSolid) = None,
              material: (str, G4Material) = None,
              logical: (str, G4LogicalVolume) = None,
              mother: (str, G4LogicalVolume) = None,
              pos: list[float] = position(),
              rot: list[float] = rotation(),
              x: float = 1*m,
              y: float = 1*m,
              z: float = 1*m,
              rmin : float = 0.0, 
              rmax : float = 1*m, 
              phimin : float = 0.0, 
              phimax : float = twopi, 
              thetamin : float = 0.0, 
              thetamax : float = twopi,
              color: list[float,int] = [1.0,0.0,0.0,1.0],
              visible: bool = True,
              drawstyle: str = "wireframe"):
    """
    Examples:
    component('block', solid='box', x=5, y=5, z=5, material="G4_AIR")

    component('block', solid=box_solid_obj, material="G4_AIR")

    component('block', logical=box, pos=[0.0,5.0,0.0], mother=world)
    """

    if solid and material and logical:
        raise Exception("Define solid/material or logical, not both")

    if not logical:
        logical = build_logical(name, solid, material, 
                                x, y, z, rmin, rmax, phimin, 
                                phimax, thetamin, thetamax, color, visible, drawstyle)
        
    rotation_matrix = G4RotationMatrix()
    if rot[0] != 0.0: rotation_matrix.rotateX(rot[0])
    if rot[1] != 0.0: rotation_matrix.rotateY(rot[1])
    if rot[2] != 0.0: rotation_matrix.rotateZ(rot[2])
    global gComponentList
    gComponentList.append(rotation_matrix)

    local_pos = G4ThreeVector(pos[0], pos[1], pos[2])
    gComponentList.append(local_pos)
    
    if isinstance(mother, G4PVPlacement):
        mother = mother.GetLogicalVolume()
    
    if not mother:
        rotation_matrix = 0 
        mother = 0

      # return g4.G4PVPlacement(
      #       None,
      #       local_pos,
      #       logical,
      #       name,
      #       mother,  
      #       False, 
      #       0)

    plac = G4PVPlacement(
            rotation_matrix,
            local_pos,
            logical,
            name,
            mother,  
            False, 
            0)
    
    gComponentList.append(plac)
    return plac



print("GEANT4 : Imported all definitions.")



