from . import _lazy_loader as _lzl

_lzl.include("G4VSceneHandler.hh")
_lzl.include("G4VGraphicsSystem.hh")
_lzl.include("G4VSceneHandler.hh")
_lzl.include("globals.hh")
_lzl.include("G4Polyline.hh")
_lzl.include("G4Circle.hh")
_lzl.include("G4VMarker.hh")
_lzl.include("G4Visible.hh")
_lzl.include('G4UImanager.hh')
_lzl.include('G4UIterminal.hh')
_lzl.include('G4VisExecutive.hh')
_lzl.include('G4VisExecutive.icc')
_lzl.include('G4UIExecutive.hh')
_lzl.include("G4ParticleTable.hh")
_lzl.include("G4VisAttributes.hh")
_lzl.G4VisAttributes

# try:

_lzl.cppyy.cppdef("""
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

_lzl.cppyy.cppdef("""
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

_lzl.cppyy.cppdef("""
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

_lzl.cppyy.cppdef("""
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
