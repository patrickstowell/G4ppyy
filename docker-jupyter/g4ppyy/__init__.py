import cppyy
from subprocess import Popen, PIPE
import os


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
    

print("GEANT4 : Loading modules")
twopi = 2*3.14159 
deg = 3.14159/180.0

#cppyy.include('/data/g4definitions.hh')
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


def handle_interactive(gRunManager):
    gRunManager.Initialize()
    ui = G4UIExecutive(1,["test"])

    visManager = G4VisExecutive()
    visManager.Initialize()

    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(os.path.dirname(__file__) + "/interactive_vis.mac")

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
            1)
    
    gComponentList.append(plac)
    return plac




import k3d
import numpy as np
from k3d import matplotlib_color_maps



import cppyy
cppyy.include("G4ASCIITree.hh")
cppyy.include("G4VSceneHandler.hh")
from cppyy.gbl import G4ASCIITree

cppyy.include("G4VGraphicsSystem.hh")
cppyy.include("G4VSceneHandler.hh")
cppyy.include("globals.hh")
cppyy.include("G4Polyline.hh")
cppyy.include("G4Circle.hh")
cppyy.include("G4VMarker.hh")
cppyy.include("G4Visible.hh")




cppyy.cppdef("""
class G4NURBS;

class BaseSceneHandler : public G4VSceneHandler {
public: 
    BaseSceneHandler(G4VGraphicsSystem &system, G4int id, const G4String &name="") : G4VSceneHandler(system,id,name) {
    }

    G4Transform3D* GetObjectTransformation(){
        return &fObjectTransformation;
    }

    virtual void AddPrimitivePolyhedron(const G4Polyhedron& obj){}
    virtual void AddPrimitive (const G4Polyhedron& obj){
        AddPrimitivePolyhedron(obj);
    };         

    virtual void AddPrimitivePolyline(const G4Polyline& obj){}
    virtual void AddPrimitive (const G4Polyline& obj){
        AddPrimitivePolyline(obj);
    };

    virtual void AddPrimitiveText (const G4Text& obj){};
    virtual void AddPrimitive (const G4Text& obj){
        AddPrimitiveText(obj);
    };

    virtual void AddPrimitiveCircle(const G4Circle& obj){}
    virtual void AddPrimitive (const G4Circle& obj){
        AddPrimitiveCircle(obj);
    };      

    virtual void AddPrimitiveSquare(const G4Square& obj){}
    virtual void AddPrimitive (const G4Square& obj){
        AddPrimitiveSquare(obj);
    };     
   
    virtual void AddPrimitiveNURBS (const G4NURBS& obj){};
    virtual void AddPrimitive (const G4NURBS& obj){
        AddPrimitiveNURBS(obj);
    };      
};""")

cppyy.cppdef("""
std::vector<std::vector<std::vector<double>>> ObtainPolyhedronVertexFacets(const G4Polyhedron& obj){

std::vector< std::vector<double> > normals_return;
std::vector< std::vector<double> > vertex_return;

G4bool notLastFace;
do {
    G4Point3D vertex[4];
    G4int edgeFlag[4];
    G4Normal3D normals[4];
    G4int nEdges;
    notLastFace = obj.GetNextFacet(nEdges, vertex, edgeFlag, normals);
    
    for(G4int edgeCount = 0; edgeCount < nEdges; ++edgeCount) {
        std::vector<double> normals_subvect;
        normals_subvect.push_back(normals[edgeCount].x());
        normals_subvect.push_back(normals[edgeCount].y());
        normals_subvect.push_back(normals[edgeCount].z());
        normals_return.push_back(normals_subvect);
        
        std::vector<double> vertex_subvect;
        vertex_subvect.push_back(vertex[edgeCount].x());
        vertex_subvect.push_back(vertex[edgeCount].y());
        vertex_subvect.push_back(vertex[edgeCount].z());
        vertex_return.push_back(vertex_subvect);
    }

    if (nEdges == 3) {
        G4int edgeCount = 3;
        normals[edgeCount] = normals[0];
        vertex[edgeCount] = vertex[0];

        std::vector<double> normals_subvect;
        normals_subvect.push_back(normals[edgeCount].x());
        normals_subvect.push_back(normals[edgeCount].y());
        normals_subvect.push_back(normals[edgeCount].z());
        normals_return.push_back(normals_subvect);
        
        std::vector<double> vertex_subvect;
        vertex_subvect.push_back(vertex[edgeCount].x());
        vertex_subvect.push_back(vertex[edgeCount].y());
        vertex_subvect.push_back(vertex[edgeCount].z());
        vertex_return.push_back(vertex_subvect);
    }
} while (notLastFace);  

std::vector<std::vector<std::vector<double>>> compiled;
compiled.push_back(normals_return);
compiled.push_back(vertex_return);

return compiled;
}
""")

cppyy.cppdef("""
std::vector<std::vector<double>> GetPolylinePoints(const G4Polyline& line){
     G4int nPoints = line.size ();
     std::vector<std::vector<double>> data;
     if (nPoints <= 0) return data;
     
    for (G4int iPoint = 0; iPoint < nPoints; iPoint++) {
        G4double x, y, z;
        x = line[iPoint].x(); 
        y = line[iPoint].y();
        z = line[iPoint].z();
        data.push_back({x,y,z});
    };
    return data;
};
""")

cppyy.cppdef("""
std::vector<std::vector<int>> ObtainFacets(const G4Polyhedron& obj){
    std::vector<std::vector<int>> data;

    G4int iFace;
    G4int n; 
    G4int iNodes[100];
    G4int edgeFlags[100];
    G4int iFaces[100];
    
    for (iFace = 0; iFace < obj.GetNoFacets(); iFace++) {
        obj.GetFacet(iFace+1, n, iNodes, edgeFlags, iFaces);
        std::vector<int> temp;
        if (n == 4){
            temp.push_back(iFaces[0] - 1);
            temp.push_back(edgeFlags[0]-1);
            temp.push_back(iNodes[0] - 1);
            temp.push_back(iNodes[1] - 1);
            temp.push_back(iNodes[2] - 1);
            temp.push_back(iNodes[3] - 1);        
        } else {
            temp.push_back(iFaces[0] - 1);
            temp.push_back(edgeFlags[0]-1);
            temp.push_back(iNodes[0] - 1);
            temp.push_back(iNodes[1] - 1);
            temp.push_back(iNodes[2] - 1);
            temp.push_back(iNodes[0] - 1); 
        }
        data.push_back(temp);
    }    
    return data;
};""")

def rgb_to_hex(r, g, b):
        """Converts RGB values (0-255) to a hex color code.
    
        Args:
            r (int): Red value (0-255).
            g (int): Green value (0-255).
            b (int): Blue value (0-255).
    
        Returns:
            str: Hex color code (e.g., '#FF0000').
        """
    
        # Ensure RGB values are within the valid range
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)
    
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
    
        # Convert each RGB value to its hexadecimal representation
        hex_r = hex(r)[2:].upper()
        hex_g = hex(g)[2:].upper()
        hex_b = hex(b)[2:].upper()
    
        # Pad each hexadecimal value with a leading zero if necessary
        hex_r = hex_r.zfill(2)
        hex_g = hex_g.zfill(2)
        hex_b = hex_b.zfill(2)
    
        # Combine the hexadecimal values into a single hex color code    
        hex_color =  int(hex_r + hex_g + hex_b,16)
        return hex_color


import plotly.graph_objects as go
global gfig
gfig = k3d.plot()

global k3d_polyline_vertices
k3d_polyline_vertices = []
global k3d_polyline_indices
k3d_polyline_indices = []
global k3d_polyline_colors
k3d_polyline_colors = []
global k3d_polyline_colors2
k3d_polyline_colors2 = []
global k3d_polyline_origins
k3d_polyline_origins = []

global k3d_polyline_vectors
k3d_polyline_vectors = []

global k3d_circle_vertices
k3d_circle_vertices = []
global k3d_circle_sizes
k3d_circle_sizes = []
global k3d_circle_colors
k3d_circle_colors = []


class JupyterSceneHandler(cppyy.gbl.BaseSceneHandler):
    def __init__(self, system, id, name):
        super().__init__(system, id, name)
        self.global_data = []
        self.current_transform = None
        self.nlines = 0
        
        
        # self.fig = go.Figure(data=self.global_data)
        # self.fig.update_layout( autosize=False, width=800, height=800, ) 
        # self.fig.show()
        # self.fig = k3d.plot()
        # global gfig
        # gfig = self.fig

    # def BeginModelling(self):
        # print("Begin modelling")

    # def EndModelling(self):
        # print("End Modelling")
        
    # def BeginPrimitives(self, objectTransformation):
    #     super().BeginPrimitives(objectTransformation)
    #     print("Begin primitives", objectTransformation)
    #     self.current_transform = objectTransformation

    # def EndPrimitives(self):
    #     super().BeginPrimitives()
    #     print("End primitives")
    #     self.current_transform = None
    #     # self.fig = go.Figure(data=self.global_data)
        # self.fig.update_layout( autosize=False, width=800, height=800, ) 
        # self.fig.show()
        # self.fig.display()

    
    def AddPrimitivePolyline(self, obj):
        self.current_transform = self.GetObjectTransformation()
        self.nlines += 1


        global k3d_polyline_vertices
        global k3d_polyline_indices
        global k3d_polyline_colors

        global k3d_polyline_origins
        global k3d_polyline_vectors

        
        # Limit k3D Drawer
        if len(k3d_polyline_indices) > 10000: return


        vis = obj.GetVisAttributes()
        color = vis.GetColor()
        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
        cval = rgb_to_hex(r,g,b)
        # print("VISATTDFEGS", vis.GetAttDefs())
        
        
        vertices = cppyy.gbl.GetPolylinePoints(obj)

        for v in vertices:
            p = G4ThreeVector(v[0], v[1], v[2])
            p = self.current_transform.getRotation()*p + self.current_transform.getTranslation()
            id1 = len(k3d_polyline_vertices)
            k3d_polyline_vertices.append( [float(p.x()), float(p.y()), float(p.z())] )
            id2 = len(k3d_polyline_vertices)
            k3d_polyline_colors.append(cval)
            
            if len(k3d_polyline_vertices) >= 2:
                k3d_polyline_indices.append([id1-1,id2-1])
                
                k3d_polyline_origins.append([(k3d_polyline_vertices[id1-1][0] + k3d_polyline_vertices[id2-1][0])/2,
                                            (k3d_polyline_vertices[id1-1][1] + k3d_polyline_vertices[id2-1][1])/2,
                                            (k3d_polyline_vertices[id1-1][2] + k3d_polyline_vertices[id2-1][2])/2])
    
                k3d_polyline_vectors.append([(k3d_polyline_vertices[id2-1][0] - k3d_polyline_vertices[id1-1][0])/4,
                                            (k3d_polyline_vertices[id2-1][1] - k3d_polyline_vertices[id1-1][1])/4,
                                            (k3d_polyline_vertices[id2-1][2] - k3d_polyline_vertices[id1-1][2])/4])
                k3d_polyline_colors2.append(cval)
                

        # if len(k3d_polyline_vertices) % 100 == 0:
            # print("ADDING POLYLINE", len(k3d_polyline_vertices))
        
        
    def AddPolyLinesAtEnd(self):
        global k3d_polyline_vertices
        global k3d_polyline_indices
        polyline_k3d_vertices_np = np.array(k3d_polyline_vertices).astype(np.float32)
        polyline_k3d_indices_np = np.array(k3d_polyline_indices).astype(np.uint32)
        polyline_k3d_colors_np = np.array(k3d_polyline_colors).astype(np.uint32)

        global k3d_polyline_origins
        global k3d_polyline_vectors
        global k3d_polyline_colors2
        

        polyline_k3d_origins_np = np.array(k3d_polyline_origins).astype(np.float32)
        polyline_k3d_vectors_np = np.array(k3d_polyline_vectors).astype(np.float32)
        polyline_k3d_colors2_np = np.array(k3d_polyline_colors2).astype(np.uint32)
        
        global gfig
        gfig += k3d.lines(vertices=polyline_k3d_vertices_np, 
                          indices=polyline_k3d_indices_np, 
                          indices_type='segment',
                          shader='simple',
                          width=0.5,
                          colors=polyline_k3d_colors_np) 

        # gfig += k3d.vectors(polyline_k3d_origins_np, polyline_k3d_vectors_np,
        #                   line_width=2.0)
        global k3d_circle_vertices
        global k3d_circle_sizes
        global k3d_circle_colors
        
        gfig += k3d.points(positions=np.array(k3d_circle_vertices).astype(np.float32),
                        point_sizes=k3d_circle_sizes,
                        shader='flat', colors=k3d_circle_colors)

        #, color=0xc6884b, shader='mesh', width=0.025)
        # gfig += k3d.line(k3d_vertices, color=0xc6884b, shader='mesh', width=2)

    
    def AddPrimitiveCircle(self, obj):
        self.current_transform = self.GetObjectTransformation()
        self.nlines += 1

        global k3d_circle_vertices
        global k3d_circle_sizes
        global k3d_circle_colors
        
        # Limit k3D Drawer
        if len(k3d_circle_vertices) > 10000: return
        size = obj.GetScreenSize()*2

        vis = obj.GetVisAttributes()
        color = vis.GetColor()
        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
        cval = rgb_to_hex(r,g,b)

        
        p = obj.GetPosition()
        # G4ThreeVector(0.0,0.0,0.0)
        # p = p + self.current_transform.getTranslation()

        k3d_circle_vertices.append( [float(p.x()), float(p.y()), float(p.z())] )
        k3d_circle_sizes.append(size)
        k3d_circle_colors.append(cval)
        
        return

    
    def AddPrimitivePolyhedron(self, obj):
        self.current_transform = self.GetObjectTransformation()
        

        vertices = []
        for i in range(obj.GetNoVertices()):
            p3d = obj.GetVertex(i+1)
            vertices.append( [p3d[0], p3d[1], p3d[2]] )

        facets = cppyy.gbl.ObtainFacets(obj)

        normals = []
        for i in range(obj.GetNoFacets()):
            f3d = obj.GetUnitNormal(i+1)
            normals.append( (f3d[0], f3d[1], f3d[2]) )

        k3d_vertices = []
        for v in vertices:
            p = G4ThreeVector(v[0], v[1], v[2])
            p = self.current_transform.getRotation()*p + self.current_transform.getTranslation()
            k3d_vertices.append( [float(p.x()), float(p.y()), float(p.z())] )

        k3d_normals = []
        for n in normals:
            p = G4ThreeVector(n[0], n[1], n[2])
            p = self.current_transform.getRotation()*p 
            k3d_normals.append( [float(p.x()), float(p.y()), float(p.z())] )

        k3d_indices = []
        for f in facets:
            ff = [f[2], f[3], f[4], f[5]]
            k3d_indices.append( [ff[0], ff[1], ff[2]] )
            k3d_indices.append( [ff[0], ff[1], ff[3]] )
            k3d_indices.append( [ff[0], ff[2], ff[1]] )
            k3d_indices.append( [ff[0], ff[2], ff[3]] )
            k3d_indices.append( [ff[0], ff[3], ff[2]] )
            k3d_indices.append( [ff[0], ff[3], ff[3]] )

            k3d_indices.append( [ff[1], ff[0], ff[2]] )
            k3d_indices.append( [ff[1], ff[0], ff[3]] )
            k3d_indices.append( [ff[1], ff[2], ff[0]] )
            k3d_indices.append( [ff[1], ff[2], ff[3]] )
            k3d_indices.append( [ff[1], ff[3], ff[0]] )
            k3d_indices.append( [ff[1], ff[3], ff[3]] )

            k3d_indices.append( [ff[2], ff[0], ff[1]] )
            k3d_indices.append( [ff[2], ff[0], ff[3]] )
            k3d_indices.append( [ff[2], ff[1], ff[0]] )
            k3d_indices.append( [ff[2], ff[1], ff[3]] )
            k3d_indices.append( [ff[2], ff[3], ff[0]] )
            k3d_indices.append( [ff[2], ff[3], ff[1]] )
            
            
            
            
            
        k3d_vertices = np.array(k3d_vertices).astype(np.float32)
        k3d_normals = np.array(k3d_normals).astype(np.float32)
        k3d_indices = np.array(k3d_indices).astype(np.uint32)

        global gfig
        vis = obj.GetVisAttributes()
        
        color = vis.GetColor()
        style = vis.GetForcedDrawingStyle()
        visbl = vis.IsVisible()

        opacity = color.GetAlpha()
        if not visbl: opacity = 0.0

        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
       
        iswireframe = False
        if vis.GetForcedDrawingStyle() == G4VisAttributes.wireframe:
            iswireframe = True
            
        gfig += k3d.mesh(np.array(k3d_vertices), 
                         np.array(k3d_indices), 
                         np.array(k3d_normals), 
                         name="Object",
                         opacity=opacity,
                         wireframe=iswireframe,
                         color=rgb_to_hex(r,g,b))
        
      
import matplotlib.pyplot as plt

class JupyterViewer(cppyy.gbl.G4VViewer):
    def __init__(self, scene, id, name):
        super().__init__(scene, id, name)
        self.name = "JUPYTER"
        self.scene = scene

    def SetView(self):
        return

    def ClearView(self):
        return

    def DrawView(self):
        self.scene.global_data = []   
        self.ProcessView()
        return

    def FinishView(self):
        print("FINISH VIEW")
        self.scene.AddPolyLinesAtEnd()
    
        



cppyy.cppdef("""
class BaseGS : public G4VGraphicsSystem {
public: 
    BaseGS() : G4VGraphicsSystem("Jupyter","Jupyter",G4VGraphicsSystem::threeD) {
        fName = "Jupyter";
        fNicknames = {"Jupyter"};
      fDescription = "Jupyter";
      fFunctionality = G4VGraphicsSystem::threeD;
    }
    virtual G4VSceneHandler* CreateSceneHandler (const G4String& name) { return NULL; };
    virtual G4VViewer* CreateViewer (G4VSceneHandler& scenehandler, const G4String& name) { return NULL; };
};""")

class JupyterGraphicsSystem(cppyy.gbl.BaseGS):
    def __init__(self):
        super().__init__()
        
    def CreateSceneHandler(self,name):
        self.name = name
        self.handler = JupyterSceneHandler(self, 0, name)
        return self.handler

    def CreateViewer(self, scenehandler, name):
        self.scenehandler = scenehandler
        self.viewer = JupyterViewer(scenehandler, 0, name)
        return self.viewer
        
    def IsUISessionCompatible(self):
        return True


class PyCRUSTVisExecutive(G4VisExecutive):
    def RegisterGraphicsSystems(self):
        self.val = JupyterGraphicsSystem()
        self.RegisterGraphicsSystem(self.val);
        self.gs = self.val


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
    UImanager.ExecuteMacroFile(os.path.dirname(__file__) + "/jupyter_vis.mac")

global detector_hooks
detector_hooks = []

def register_detector_hooks(det):
    global detector_hooks
    detector_hooks.append(det)

def register_processor_hooks(det):
    register_detector_hooks(det)

def register_tracking_hooks(det):
    register_detector_hooks(det)
        
def draw_visualization(gRunManager):
    global gfig
    visManager.gs.viewer.scene.AddPolyLinesAtEnd()
    gfig.display()

    global detector_hooks
    for obj in detector_hooks:
        start_action = getattr(obj, "VisualizationAction", None)
        if callable(start_action):
            start_action()

import os 
def supress_startup():
    UImanager = G4UImanager.GetUIpointer()
    UImanager.ExecuteMacroFile(os.path.dirname(__file__) + "/jupyter_quiet.mac")

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




print("GEANT4 : Imported all definitions.")



