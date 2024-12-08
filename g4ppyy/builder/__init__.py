from .. import _lazy_loader as _lzl

from .. import register
register.all()

from ..SI import *

gNistManager = _lzl.gNistManager

G4Material = _lzl.G4Material
G4Element = _lzl.G4Element
G4VUserDetectorConstruction = _lzl.G4VUserDetectorConstruction
G4VSolid = _lzl.G4VSolid
G4LogicalVolume = _lzl.G4LogicalVolume
G4Color = _lzl.G4Color
G4Box = _lzl.G4Box
G4Tubs = _lzl.G4Tubs
G4Sphere = _lzl.G4Sphere
G4VisAttributes = _lzl.G4VisAttributes
G4VPhysicalVolume = _lzl.G4VPhysicalVolume
G4VSolid = _lzl.G4VSolid
G4RotationMatrix = _lzl.G4RotationMatrix
G4ThreeVector = _lzl.G4ThreeVector
G4PVPlacement = _lzl.G4PVPlacement
G4MaterialPropertiesTable = _lzl.G4MaterialPropertiesTable


# ------------------
# MATERIALS
# ------------------
def GetMaterial(name):
    return gNistManager.FindOrBuildMaterial(name)

# Material Helpers
def material_from_elements(name : str,
                            density : float,
                            elements : list[str, _lzl.G4Element],
                            fractions : list[int]):
    
    if (gNistManager.FindOrBuildMaterial(name)): 
        return gNistManager.FindOrBuildMaterial(name)
        
    mat = _lzl.G4Material(name, density, len(elements))
    
    for e,f in zip(elements, fractions):
        if (isinstance(e, str)):
            
            e = gNistManager.FindOrBuildElement(e)
        if (e):
            mat.AddElement(e, f)

    return mat


def material_from_materials(name : str,
                            density : float,
                            materials : list[str, _lzl.G4Material],
                            fractions : list[int]):
    if (gNistManager.FindOrBuildMaterial(name)): 
        return gNistManager.FindOrBuildMaterial(name)
        
    mat = _lzl.G4Material(name, density, len(materials))

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

import numpy as np

def update_table_properties(table, properties):

    constants = ["SCINTILLATIONTIMECONSTANT1", "SCINTILLATIONTIMECONSTANT2","SCINTILLATIONYIELD", "WLSTIMECONSTANT",  "RESOLUTIONSCALE", "MIEHG_FORWARD_RATIO", "MIEHG_FORWARD", 
"MIEHG_BACKWARD" ]
    for key in constants:
        if key in properties:
            table.AddConstProperty(key, properties[key])
            
    dynamics = ["RINDEX", "ABSLENGTH", "SCINTILLATIONCOMPONENT1", "SCINTILLATIONCOMPONENT2", "WLSCOMPONENT", "ABSLENGTH", "WLSABSLENGTH", "RAYLEIGH", "MIEHG" ]
    for key in dynamics:

        if key+"_X" in properties and key+"_Y" in properties:

            xv = properties[key+"_X"]
            yv = properties[key+"_Y"]

            yv = [x for _, x in sorted(zip(yv, xv))]
            xv = [x for _, x in sorted(zip(xv, xv))]

            table.AddProperty(key, 
                            np.array(xv),
                            np.array(yv), 
                            len(xv))



def build_vis(col=[1.0,0.0,0.0,0.5], visible=True, drawstyle="wireframe"):
    
    vis = _lzl.G4VisAttributes()
    gVisAttributes.append(vis)
    
    vis.SetVisibility(visible)
    if drawstyle == "solid":
        vis.SetForceSolid(1)
        vis.SetForceWireframe(0)
    elif drawstyle == 'wireframe':
        vis.SetForceSolid(0)
        vis.SetForceWireframe(1)
    else:
        raise RunTimeError(f"Unknown Drawstyle : {drawstyle}")
        
    if len(col) <= 3:
        col.append(1.0)
        
    vis.SetColor(_lzl.G4Color(col[0],col[1],col[2], col[3]))

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
        tab = _lzl.G4MaterialPropertiesTable()
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
             elements: list[str, _lzl.G4Element] = None, 
             materials: list[str, _lzl.G4Material] = None, 
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

# --------------------
# GEOMETRY
# --------------------

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


# class World(_lzl.G4VUserDetectorConstruction):
#     def __init__(self, world_obj):
#         super().__init__()
#         self.physical = world_obj
        
#     def Construct(self):
#         return self.physical
    
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
        obj = _lzl.G4Box(name, x, y, z)
        
    if "sphere" in solid.lower(): 
        obj = _lzl.G4Sphere(name, rmin, rmax, 
                       phimin, phimax, thetamin, thetamax)
        
    if "tubs" in solid.lower(): 
        obj = _lzl.G4Tubs(name, rmin,
                     rmax, z, phimin, phimax)

    gSolidList[name] = obj
    return obj


gVisAttributes = []
def vis(detector, col, visible=True, drawstyle="wireframe"):
    
    vis = _lzl.G4VisAttributes()
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
        
    vis.SetColor(_lzl.G4Color(col[0],col[1],col[2], col[3]))

    if isinstance(detector, _lzl.G4VPhysicalVolume):
        detector.GetLogicalVolume().SetVisAttributes(vis)
    else:
        detector.SetVisAttributes(vis)
    

global gLogicalList 
gLogicalList = []

def build_logical(name : str,
          solid : (str, _lzl.G4VSolid) = None,
          material: (str, _lzl.G4Material) = None,
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
        
        built_material = build_material(material)

        if not built_material:
          raise ValueError(f"Could not build material: {material}")

        material = built_material
  
    log = _lzl.G4LogicalVolume(solid, material, name)
    gLogicalList.append(log)

    # Move to overriding drawstyles.        
    vis(log, color, visible, drawstyle)
    gSolidList[name + "_logical"] = log
    
    return log

global gComponentList
gComponentList = []

def build_component(name : str,
              solid : (str, _lzl.G4VSolid) = None,
              material: (str, _lzl.G4Material) = None,
              logical: (str, _lzl.G4LogicalVolume) = None,
              mother: (str, _lzl.G4LogicalVolume) = None,
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
    component('block', solid='box', x=5, y=5, z=5, material="_lzl.G4_AIR")

    component('block', solid=box_solid_obj, material="_lzl.G4_AIR")

    component('block', logical=box, pos=[0.0,5.0,0.0], mother=world)
    """
    global gComponentList
    if (name in gComponentList):
        print("ERROR COMPONENT ALREADY IN gComponentList")
        raise RuntimeError("Check your geo construction!")
    
    if solid and material and logical:
        raise Exception("Define solid/material or logical, not both")

    if not logical:
        logical = build_logical(name, solid, material, 
                                x, y, z, rmin, rmax, phimin, 
                                phimax, thetamin, thetamax, color, visible, drawstyle)
        
    rotation_matrix = _lzl.G4RotationMatrix()
    if rot[0] != 0.0: rotation_matrix.rotateX(rot[0])
    if rot[1] != 0.0: rotation_matrix.rotateY(rot[1])
    if rot[2] != 0.0: rotation_matrix.rotateZ(rot[2])

    gComponentList.append(rotation_matrix)

    local_pos = _lzl.G4ThreeVector(pos[0], pos[1], pos[2])
    gComponentList.append(local_pos)
    
    if isinstance(mother, _lzl.G4PVPlacement):
        mother = mother.GetLogicalVolume()
    
    if not mother:
        rotation_matrix = 0 
        mother = 0

      # return _lzl.G4._lzl.G4PVPlacement(
      #       None,
      #       local_pos,
      #       logical,
      #       name,
      #       mother,  
      #       False, 
      #       0)

    plac = _lzl.G4PVPlacement(
            rotation_matrix,
            local_pos,
            logical,
            name,
            mother,  
            False, 
            1)
    
    gComponentList.append(plac)
    return plac


