from . import _lazy_loader as _lzl
from . import SI as SI

_lzl.include("G4VUserPrimaryGeneratorAction.hh")
_lzl.include("G4VSensitiveDetector.hh")
_lzl.include("G4VUserDetectorConstruction.hh")

def materials():
    for key in ["G4Material",
                "G4Element",
                "G4NistManager"]:
        _lzl.lazy_register(key)

    gNistManager = _lzl.G4NistManager.Instance()
    _lzl.assign("gNistManager", gNistManager)


def managers():
    for key in ["G4RunManager", "G4VUserPrimaryGeneratorAction"]:
        _lzl.lazy_register(key)



def physics():
    for key in ["QGSP_BERT_HP",
                "QGSP_BERT",
                "G4OpticalPhysics",
                "G4NistManager"]:
        _lzl.lazy_register(key)


def geometry():

    for key in ["G4VPhysicalVolume",
                "G4LogicalVolume",
                "G4VisAttributes",
                "G4Color",
                "G4VSolid",
                "G4Box",
                "G4Sphere",
                "G4Tubs",
                "G4VSensitiveDetector"]:
        _lzl.include(key + ".hh")
        _lzl.lazy_register(key)

def all():
    managers()
    physics()
    geometry()
    materials()


