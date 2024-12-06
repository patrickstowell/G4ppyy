
import k3d
import numpy as np
# import plotly.graph_objects as go
from ._lazy_loader import cppyy
from . import _lazy_loader as _lzl
from . import _base_visualiser
import matplotlib.pyplot as plt
from ._base_visualiser import rgb_to_hex

cppyy.include('G4VisExecutive.hh')
cppyy.include('G4VisExecutive.icc')
_lzl.include("G4VisExecutive.icc")
_lzl.include("G4VisExecutive.hh")
_lzl.include("G4String.hh")
_lzl.G4VisExecutive
_lzl.G4String

_lzl.include("G4VSceneHandler.hh")
_lzl.include("G4VGraphicsSystem.hh")
_lzl.include("G4VSceneHandler.hh")
_lzl.include("globals.hh")
_lzl.include("G4Polyline.hh")
_lzl.include("G4Circle.hh")
_lzl.include("G4VMarker.hh")
_lzl.include("G4Visible.hh")
_lzl.include("G4VisAttributes.hh")

G4VMarker = _lzl.G4VMarker
G4Visible = _lzl.G4VisAttributes
G4VisAttributes = _lzl.G4VisAttributes
G4VisExecutive = _lzl.G4VisExecutive
G4String = _lzl.G4String

from ._lazy_loader import G4ThreeVector
from . import _lazy_loader

_lazy_loader.include("G4VisExecutive.icc")
_lazy_loader.include("G4VisExecutive.hh")
_lazy_loader.G4VisExecutive


global gfig
gfig = k3d.plot()



class MPLJupyterSceneHandler(cppyy.gbl.BaseSceneHandler):
    def __init__(self, system, id, name):
        super().__init__(system, id, name)
        self.global_data = []
        self.current_transform = None
        self.nPolyhedron = 0

        self.nlines = 0
        self.line_option = "lines"
        self.max_lines = 50000

        self.ncircles = 0
        self.max_circles = 50000

        self.nvectors = 0
        self.max_vectors = 10000

        self.circle_vertices = np.zeros((self.max_circles,3)).astype(np.float32)
        self.circle_sizes = np.zeros(self.max_circles).astype(np.uint32)
        self.circle_colors = np.zeros(self.max_circles).astype(np.uint32)

        self.polyline_vertices = np.zeros((self.max_lines,3)).astype(np.float32)
        self.polyline_indices = [] #np.zeros((self.max_lines,2)).astype(np.uint32)
        self.polyline_colors = np.zeros(self.max_lines).astype(np.uint32)

        self.polyline_vector_colors = np.zeros(self.max_vectors).astype(np.uint32)
        self.polyline_origins = np.zeros((self.max_vectors,3)).astype(np.float32)
        self.polyline_vectors = np.zeros((self.max_vectors,3)).astype(np.float32)

        self.fig, self.axs = plt.subplots(1, 3, figsize=(9*2, 3*2))

    

    def AddPrimitivePolyline(self, obj):
        self.current_transform = self.GetObjectTransformation()

        # Limit k3D Drawer
        vis = obj.GetVisAttributes()
        color = vis.GetColor()
        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
        cval = rgb_to_hex(r,g,b)
                
        vertices = cppyy.gbl.GetPolylinePoints(obj)
        newcount = 0

        for v in vertices:
            newcount += 1
            p = _lzl.G4ThreeVector(v[0], v[1], v[2])
            p = self.current_transform.getRotation()*p + self.current_transform.getTranslation()
            
            self.polyline_vertices[self.nlines % self.max_lines] = ( [float(p.x()), float(p.y()), float(p.z())] )
            self.polyline_colors[self.nlines % self.max_lines] = cval

            if newcount >= 2:
                self.polyline_indices.append( [self.nlines % self.max_lines, self.nlines+1 % self.max_lines] )

            self.nlines += 1

                
    def AddPolyLinesAtEnd(self):
        pass
     
        # global gfig
        # if self.line_option == "lines":
        #     mlines = np.max([self.nlines, self.max_lines])
        #     print(len(self.polyline_colors), len(self.polyline_indices), len(self.polyline_vertices))
        #     gfig += k3d.lines(vertices=np.array(self.polyline_vertices[0:mlines,:]).astype(np.float32), 
        #                     indices=np.array(self.polyline_indices).astype(np.uint32), 
        #                     indices_type='segment',
        #                     shader='simple',
        #                     width=0.5,
        #                     colors=np.array(self.polyline_colors[0:mlines]).astype(np.uint32)) 

        # else:
        #     # polyline_vector_colors
        #     gfig += k3d.vectors(np.array(self.polyline_origins[0:self.nvectors]).astype(np.float32), 
        #                         np.array(self.polyline_vectors[0:self.nvectors]).astype(np.uint32),
        #                         line_width=2.0)

       

    def AddPrimitiveCircle(self, obj):
        pass
        # self.current_transform = self.GetObjectTransformation()

        # size = obj.GetScreenSize()*2

        # vis = obj.GetVisAttributes()
        # color = vis.GetColor()
        # r = float(color.GetRed())
        # b = float(color.GetBlue())
        # g = float(color.GetGreen())
        # cval = rgb_to_hex(r,g,b)

        # p = obj.GetPosition()

        
        return

    
    def AddPrimitivePolyhedron(self, obj):
        self.current_transform = self.GetObjectTransformation()

        def get_components(obj, transform):

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

            return k3d_vertices, k3d_normals, k3d_indices
        
        vertices, normals, indices = get_components(obj, self.current_transform)

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
       
        iswireframe = True
        if vis.GetForcedDrawingStyle() == G4VisAttributes.wireframe:
            iswireframe = False

        if self.nPolyhedron > 0:

            for i in range(len(indices)):
                self.axs[0].plot( [vertices[indices[i][0]][0],vertices[indices[i][1]][0],
                                   vertices[indices[i][2]][0],vertices[indices[i][0]][0]],
                                  [vertices[indices[i][0]][1],vertices[indices[i][1]][1],
                                   vertices[indices[i][2]][1],vertices[indices[i][0]][1]],
                                  color=(r, g, b))

            for i in range(len(indices)):
                self.axs[1].plot( [vertices[indices[i][0]][0],vertices[indices[i][1]][0],
                                   vertices[indices[i][2]][0],vertices[indices[i][0]][0]],
                                  [vertices[indices[i][0]][2],vertices[indices[i][1]][2],
                                   vertices[indices[i][2]][2],vertices[indices[i][0]][2]],
                                  color=(r, g, b))

            for i in range(len(indices)):
                self.axs[2].plot( [vertices[indices[i][0]][1],vertices[indices[i][1]][1],
                                   vertices[indices[i][2]][1],vertices[indices[i][0]][1]],
                                  [vertices[indices[i][0]][2],vertices[indices[i][1]][2],
                                   vertices[indices[i][2]][2],vertices[indices[i][0]][2]],
                                  color=(r, g, b))


        minv = np.min([np.min(vertices[:,0]),np.min(vertices[:,1]), np.min(vertices[:,2])])
        maxv = np.max([np.max(vertices[:,0]),np.max(vertices[:,1]), np.max(vertices[:,2])])
        
        self.axs[0].set_xlabel('x [mm]')
        self.axs[0].set_ylabel('y [mm]')
        self.axs[0].set_xlim([-maxv, maxv])
        self.axs[0].set_ylim([-maxv, maxv])
        
        self.axs[0].grid(True)

        self.axs[1].set_xlabel('x [mm]')
        self.axs[1].set_ylabel('z [mm]')
        self.axs[1].set_xlim([-maxv, maxv])
        self.axs[1].set_ylim([-maxv, maxv])
        
        
        self.axs[1].grid(True)

        self.axs[2].set_xlabel('y [mm]')
        self.axs[2].set_ylabel('z [mm]')
        self.axs[2].set_xlim([-maxv, maxv])
        self.axs[2].set_ylim([-maxv, maxv])
        
        
        self.axs[2].grid(True)

            
            # gfig += k3d.mesh(np.array(vertices), 
            #                  np.array(indices), 
            #                  np.array(normals), 
            #                  name="Object",
            #                  visible=False, #self.nPolyhedron > 0,
            #                  opacity=opacity,
            #                  wireframe=iswireframe,
            #                  color=rgb_to_hex(r,g,b))
        self.nPolyhedron += 1
        
    def Finish(self):
        # print("FINISHING MPL")
        # self.AddPolyLinesAtEnd()
        # global gfig
        # gfig.display()
        plt.show()
        
      
#################################
# SCENE HANDLER AND EXECUTIVES
#################################
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

_lzl.cppyy.cppdef("""
class BaseMPLJupyter : public G4VGraphicsSystem {
public: 
    BaseMPLJupyter() : G4VGraphicsSystem("K3DJupyter","K3DJupyter",G4VGraphicsSystem::threeD) {
        fName = "MPLJupyter";
        fNicknames = {"MPLJupyter"};
        fDescription = "MPLJupyter Visualisation System";
        fFunctionality = G4VGraphicsSystem::threeD;
    }
    virtual G4VSceneHandler* CreateSceneHandler (const G4String& name) { return NULL; };
    virtual G4VViewer* CreateViewer (G4VSceneHandler& scenehandler, const G4String& name) { return NULL; };
};""")

class MPLJupyterViewer(cppyy.gbl.G4VViewer):
    def __init__(self, scene, id, name):
        super().__init__(scene, id, name)
        self.name = "K3DJUPYTER"
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
        self.scene.Finish()
    

class MPLJupyterGraphicsSystem(cppyy.gbl.BaseMPLJupyter):
    def __init__(self):
        super().__init__()
        
    def CreateSceneHandler(self,name):
        self.name = name
        self.handler = MPLJupyterSceneHandler(self, 0, name)
        return self.handler

    def CreateViewer(self, scenehandler, name):
        self.scenehandler = scenehandler
        self.viewer = MPLJupyterViewer(scenehandler, 0, name)
        return self.viewer
        
    def IsUISessionCompatible(self):
        return True


class MPLJupyterVisExecutive(_lzl.G4VisExecutive):
    def RegisterGraphicsSystems(self):
        self.val = MPLJupyterGraphicsSystem()
        self.RegisterGraphicsSystem(self.val)
        self.gs = self.val

    def Start(self):
        print("Python-side Vis Activated.")

    def Finish(self):
        self.gs.viewer.scene.Finish() 
