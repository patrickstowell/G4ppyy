from . import _lazy_loader as _lzl
from . import _si_units as SI

def materials():
    for key in ["G4Material",
                "G4Element",
                "G4NistManager"]:
        _lzl.lazy_register(key)

        gNistManager = _lzl.G4NistManager.Instance()
        _lzl.assign("gNistManager", gNistManager)

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
                "G4Tubs"]:
        _lzl.lazy_register(key)

    # Handle Python-CPPYY Overrides
    def G4Box(name,
        x : float = 1.0*SI.m,
        y : float = 1.0*SI.m,
        z : float = 1.0*SI.m):
        return _lzl.cppyy.G4Box(name,
                                x,
                                y,
                                z)
    _lzl.G4Box = G4Box

    def G4Sphere(name,
                rmin : float = 0.0,
                rmax : float = 1.0*SI.m,
                phimin : float = 0.0,
                phimax : float = SI.twopi,
                thetamin : float = 0.0,
                thetamax : float = SI.twopi):
        return _lzl.cppyy.G4Sphere(name,
                                rmin,
                                rmax,
                                phimin,
                                phimax,
                                thetamin,
                                thetamax)
    _lzl.G4Sphere = G4Sphere

    def G4Tubs(name,
        rmin : float = 0.0,
        rmax : float = 1.0*SI.m,
        zmax : float = 1.0*SI.m,
        phimin : float = 0.0,
        phimax : float = SI.twopi):
        return _lzl.cppyy.G4Tubs(name,
                                rmin,
                                rmax,
                                zmax,
                                phimin,
                                phimax)

    _lzl.G4Tubs = G4Tubs

def all():
    physics()
    geometry()
    materials()


