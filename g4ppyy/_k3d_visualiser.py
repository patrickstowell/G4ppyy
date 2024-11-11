
import k3d
import numpy as np
from k3d import matplotlib_color_maps
# import plotly.graph_objects as go
from ._lazy_loader import cppyy
from . import _lazy_loader as _lzl
from . import _base_visualiser
import matplotlib.pyplot as plt

_lzl.include("G4VSceneHandler.hh")
_lzl.include("G4VGraphicsSystem.hh")
_lzl.include("G4VSceneHandler.hh")
_lzl.include("globals.hh")
_lzl.include("G4Polyline.hh")
_lzl.include("G4Circle.hh")
_lzl.include("G4VMarker.hh")
_lzl.include("G4Visible.hh")
_lzl.include("G4VisAttributes.hh")
_lzl.G4VisAttributes

from ._lazy_loader import G4ThreeVector
from . import _lazy_loader

_lazy_loader.include("G4VisExecutive.icc")
_lazy_loader.include("G4VisExecutive.hh")
_lazy_loader.G4VisExecutive


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


class K3DJupyterSceneHandler(cppyy.gbl.BaseSceneHandler):
    def __init__(self, system, id, name):
        super().__init__(system, id, name)
        self.global_data = []
        self.current_transform = None
        self.nlines = 0
        
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

    def Finish(self):
        self.AddPolyLinesAtEnd()

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
        
      

class K3DJupyterViewer(cppyy.gbl.G4VViewer):
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
    
class K3DJupyterGraphicsSystem(cppyy.gbl.BaseGS):
    def __init__(self):
        super().__init__()
        
    def CreateSceneHandler(self,name):
        self.name = name
        self.handler = K3DJupyterSceneHandler(self, 0, name)
        return self.handler

    def CreateViewer(self, scenehandler, name):
        self.scenehandler = scenehandler
        self.viewer = K3DJupyterViewer(scenehandler, 0, name)
        return self.viewer
        
    def IsUISessionCompatible(self):
        return True

cppyy.include('G4VisExecutive.hh')
cppyy.include('G4VisExecutive.icc')

class PyCRUSTVisExecutive(cppyy.gbl.G4VisExecutive):
    def RegisterGraphicsSystems(self):
        self.val = K3DJupyterGraphicsSystem()
        self.RegisterGraphicsSystem(self.val);
        self.gs = self.val

class K3DJupyterVisExecutive(cppyy.gbl.G4VisExecutive):
    def RegisterGraphicsSystems(self):
        self.val = K3DJupyterGraphicsSystem()
        self.RegisterGraphicsSystem(self.val)
        self.gs = self.val

    # def Start(self):
    #     print("Python-side Vis Activated.")

    # def FinishPlot(self):
    #     self.gs.viewer.scene.Finish() 
