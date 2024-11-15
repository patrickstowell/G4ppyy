### G4ppyy : Automated Python Bindings for GEANT4 based on CPPYY.

This package is a wrapper module around the powerful CPPYY backend enabling automated python bindings for GEANT4.
The module is setup to use geant4-config to determine the location of libraries and header files, and automatically
load them as requested by the end user through a lazy loading interface. Several additional Jupyter tools are provided
to support C++ compilation magic in cells on the fy using CPPYY, and 3D visualisation using K3D or matplotlib.


#### Importing GEANT4 through G4PPYY
G4ppyy acts as a wrapper around GEANT4, so this should simply be imported at the start of a python script or notebook.
Note that this can take a few seconds to fully load. 

```
import g4ppyy as g4

**************************************************************

[G4PPYY] : Geant4 Python wrapper for CPPYY
[G4PPYY] : Authors: P. Stowell (p.stowell@sheffield.ac.uk)
[G4PPYY] :          R. Foster 
[G4PPYY] : Loading G4 Modules.
[G4PPYY] : G4PREFIX : /app/geant4-v11.2.2/install
[G4PPYY] : G4VERSION : 11.2.2
[G4PPYY] : Module loading complete.
[G4PPYY] : Jupyter Instance : g4_k3d g4_compile
[G4PPYY] : Imported all definitions.

**************************************************************
 Geant4 version Name: geant4-11-02-patch-02 [MT]   (21-June-2024)
                       Copyright : Geant4 Collaboration
                      References : NIM A 506 (2003), 250-303
                                 : IEEE-TNS 53 (2006), 270-278
                                 : NIM A 835 (2016), 186-225
                             WWW : http://geant4.org/
**************************************************************

```

By default only a handful of classes are fully initialized at the start.
These can be seen by tab completing the g4 module namespace as below.


```
g4.[TAB]

g4.
```

However if the user requests an additional class they know is inside GEANT4 these should

#### Overloading Classes
Classes can be overriden on the python side and passed into the G4 run manager to develop interfaces on the fly without a full recompilation.

```
class neutron_tracker(g4.G4VSensitiveDetector):                
    def ProcessHits(self, aStep, ROhist):
        
        pdg = (aStep.GetTrack().GetParticleDefinition().GetPDGEncoding())
        if not (pdg == 2112): return 0

        eid = int(gRunManager.GetCurrentEvent().GetEventID())

        self.neutron_event["eid"].append( eid )
        
        pos = aStep.GetPreStepPoint().GetPosition() 
        dirs = aStep.GetTrack().GetMomentumDirection() 
        ek = aStep.GetPreStepPoint().GetTotalEnergy()
        ...
```




#### Visualisation

##### K3D Graphics System

By default G4ppyy will attempt to use the built in K3D graphics system to draw the plots if running in Jupyter.
For more information on how to enable k3d in jupyter see : https://github.com/K3D-tools/K3D-jupyter

<img width="812" alt="image" src="https://github.com/user-attachments/assets/9a6c7cf3-231e-4c69-8d07-b41885ac7267">



