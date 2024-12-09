"""
G4PPYY.k3d_visualiser : Geant4 K3D Visualiser Interface
=============

Vis tools for the K3D Graphics System

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

# System Level Imports
import numpy as np

import k3d
from k3d import matplotlib_color_maps

from . import _lazy_loader as _g4

G4ThreeVector = _g4.G4ThreeVector

# Explicit Requirements
_g4.include('G4VisExecutive.hh')
_g4.include('G4VisExecutive.icc')
_g4.include("G4VisExecutive.icc")
_g4.include("G4VisExecutive.hh")
_g4.include("G4String.hh")
_g4.include("G4VSceneHandler.hh")
_g4.include("G4VGraphicsSystem.hh")
_g4.include("G4VSceneHandler.hh")
_g4.include("globals.hh")
_g4.include("G4Polyline.hh")
_g4.include("G4Circle.hh")
_g4.include("G4VMarker.hh")
_g4.include("G4Visible.hh")
_g4.include("G4VisAttributes.hh")
_g4.include("G4VisExecutive.icc")
_g4.include("G4VisExecutive.hh")
_g4.include("G4VSceneHandler.hh")
_g4.include("G4VGraphicsSystem.hh")
_g4.include("G4VSceneHandler.hh")
_g4.include("globals.hh")
_g4.include("G4Polyline.hh")
_g4.include("G4Circle.hh")
_g4.include("G4VMarker.hh")
_g4.include("G4Visible.hh")
_g4.include('G4UImanager.hh')
_g4.include('G4UIterminal.hh')
_g4.include('G4VisExecutive.hh')
_g4.include('G4VisExecutive.icc')
_g4.include('G4UIExecutive.hh')
_g4.include("G4ParticleTable.hh")
_g4.include("G4VisAttributes.hh")

# Locals to make it easier
G4VMarker = _g4.G4VMarker
G4Visible = _g4.G4VisAttributes
G4VisAttributes = _g4.G4VisAttributes
G4VisExecutive = _g4.G4VisExecutive
G4String = _g4.G4String

scaling = 1.0/1000.0

from . import _base_visualiser
rgb_to_hex = _base_visualiser.rgb_to_hex

# global self.plot
# self.plot = k3d.plot()

# Scene Handler for K3D System, Main Draw Calls are here
class K3DJupyterSceneHandler(_g4.BaseSceneHandler):
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

        self.plot = None
        self.plot_drawn = False
        self.plot_objects = []
        self.CreatePlot()

    def CreatePlot(self):
        if not self.plot:
            self.plot = k3d.plot()

        while len(self.plot_objects) > 0:
            del self.plot_objects[0]
            del self.plot.objects[0]
            del self.plot.object_ids[0]


        self.plot_objects = []
        self.nPolyhedron = 0

    def AddPrimitivePolyline(self, obj):
        self.current_transform = self.GetObjectTransformation()

        # Limit k3D Drawer
        vis = obj.GetVisAttributes()
        color = vis.GetColor()
        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
        cval = rgb_to_hex(r,g,b)
                
        vertices = _g4.GetPolylinePoints(obj)
        newcount = 0

        for v in vertices:
            newcount += 1
            p = _g4.G4ThreeVector(v[0], v[1], v[2])
            p = self.current_transform.getRotation()*p + self.current_transform.getTranslation()
            
            self.polyline_vertices[self.nlines % self.max_lines] = ( [float(p.x()), float(p.y()), float(p.z())] )
            self.polyline_colors[self.nlines % self.max_lines] = cval

            if newcount >= 2:
                self.polyline_indices.append( [self.nlines % self.max_lines, self.nlines+1 % self.max_lines] )

            self.nlines += 1
   
  
    def AddPrimitiveCircle(self, obj):
        self.current_transform = self.GetObjectTransformation()

        size = obj.GetScreenSize()*2

        vis = obj.GetVisAttributes()
        color = vis.GetColor()
        r = float(color.GetRed())
        b = float(color.GetBlue())
        g = float(color.GetGreen())
        cval = rgb_to_hex(r,g,b)

        p = obj.GetPosition()

        # self.circle_vertices[self.ncircles % self.max_circles] = ( [float(p.x()), float(p.y()), float(p.z())] )
        # self.circle_sizes[self.ncircles % self.max_circles] = (size)
        # self.circle_colors[self.ncircles % self.max_circles] = (cval)

        # self.ncircles += 1
        
        return

                  
    def AddPolyLinesAtEnd(self):
     
        mlines = np.max([self.nlines, self.max_lines])
        print(len(self.polyline_colors), len(self.polyline_indices), len(self.polyline_vertices))
        
        self.plot_objects += [k3d.lines(vertices=scaling*np.array(self.polyline_vertices[0:mlines,:]).astype(np.float32), 
                        indices=np.array(self.polyline_indices).astype(np.uint32), 
                        indices_type='segment',
                        shader='simple',
                        width=0.5,
                        colors=np.array(self.polyline_colors[0:mlines]).astype(np.float32))]

        # polyline_vector_colors
        # self.plot_objects += [k3d.vectors(np.array(self.polyline_origins[0:self.nvectors]).astype(np.float32), 
        #                     np.array(self.polyline_vectors[0:self.nvectors]).astype(np.uint32),
        #                     line_width=2.0)]

        # self.plot += k3d.points(positions=np.array(self.circle_vertices[0:self.ncircles % self.max_circles]).astype(np.float32),
        #                 point_sizes=self.circle_sizes[0:self.ncircles % self.max_circles].astype(np.float32),
        #                 shader='flat') 
        
        #, colors=self.circle_colors.astype(np.float32))
        #, color=0xc6884b, shader='mesh', width=0.025)
        # self.plot += k3d.line(k3d_vertices, color=0xc6884b, shader='mesh', width=2)


    def AddPrimitivePolyhedron(self, obj):
        self.current_transform = self.GetObjectTransformation()

        def get_components(obj, transform):

            vertices = []
            for i in range(obj.GetNoVertices()):
                p3d = obj.GetVertex(i+1)
                vertices.append( [p3d[0], p3d[1], p3d[2]] )

            facets = _g4.ObtainFacets(obj)

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

        # global self.plot
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
            self.plot_objects += [k3d.mesh(scaling*np.array(vertices), 
                             np.array(indices), 
                             np.array(normals), 
                             name="Object",
                             visible=False, #self.nPolyhedron > 0,
                             opacity=opacity,
                             wireframe=iswireframe,
                             color=rgb_to_hex(r,g,b))]
        self.nPolyhedron += 1
        
    def Finish(self):

        if not self.plot_drawn:
            self.plot_drawn = True
            self.plot.display()

        while len(self.plot.objects) > 0:
            del self.plot.objects[0]
            del self.plot.object_ids[0]


        self.AddPolyLinesAtEnd()
        
        # global self.plot
        for obj in self.plot_objects:
            self.plot += obj

        


        
      
#################################
# SCENE HANDLER AND EXECUTIVES
#################################

# The Base Scene Handler needs a name that can be set on construction
# We make the original cppdef with the base names
_g4.cppyy.cppdef("""
class BaseK3DJupyter : public G4VGraphicsSystem {
public: 
    BaseK3DJupyter() : G4VGraphicsSystem("K3DJupyter","K3DJupyter",G4VGraphicsSystem::threeD) {
        fName = "K3DJupyter";
        fNicknames = {"K3DJupyter"};
        fDescription = "K3DJupyter Visualisation System";
        fFunctionality = G4VGraphicsSystem::threeD;
    }
    virtual G4VSceneHandler* CreateSceneHandler (const G4String& name) { return NULL; };
    virtual G4VViewer* CreateViewer (G4VSceneHandler& scenehandler, const G4String& name) { return NULL; };
};""")



class K3DJupyterViewer(_g4.G4VViewer):
    def __init__(self, scene, id, name):
        super().__init__(scene, id, name)
        self.name = "K3DJUPYTER"
        self.scene = scene

    def SetView(self):
        return

    def ClearView(self):
        return

    def DrawView(self):
        self.scene.CreatePlot()
        self.scene.global_data = []   
        self.ProcessView()
        self.scene.Finish()
        return

    def FinishView(self):
        # self.scene.Finish()
        pass
    

class K3DJupyterGraphicsSystem(_g4.BaseK3DJupyter):
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


# class K3DJupyterVisExecutive(_g4.G4VisExecutive):
#     """_summary_

#     Args:
#         _lzl (_type_): _description_
#     """
#     def RegisterGraphicsSystems(self):
#         self.val = K3DJupyterGraphicsSystem()
#         self.RegisterGraphicsSystem(self.val)
#         self.gs = self.val

#     def Start(self):
#         print("Python-side Vis Activated.")

#     def Finish(self):
#         self.gs.viewer.scene.Finish() 


# try:
#     from IPython.core.magic import register_cell_magic

#     @register_cell_magic
#     def g4_k3d(filename, cell):
#         """Creates a single cell with a jupyter k3d draw inside

#         Args:
#             filename (str): filename data
#             cell (str): cell data
#         """
#         _run.create_visualization(None)
#         _run.draw_visualization(None)
# except:
#     pass