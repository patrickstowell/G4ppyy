#!/usr/bin/env python
# coding: utf-8

# In[1]:
import g4ppyy as g4
from g4ppyy import cm, m, mm, eV, MeV
from g4ppyy import G4ThreeVector, G4RotationMatrix
import random

gRunManager = g4.G4RunManager();

# In[2]:

class custom_generator(g4.G4VUserPrimaryGeneratorAction):
    "Moderated Cf252 Generator"
    def __init__(self):
        super().__init__()
        self.particle = g4.G4Neutron.Definition()
        self.particleGun = g4.G4ParticleGun()
        self.particleGun.SetParticleDefinition(self.particle)
        self.particleGun.SetParticleMomentumDirection(g4.G4ThreeVector(1, 0, 0))
        self.particleGun.SetNumberOfParticles(1)  
        self.particleGun.SetParticleTime(0)

    def GeneratePrimaries(self, anEvent):
        energy = 1.0 #beam_energy
        self.particleGun.SetParticlePosition(g4.G4ThreeVector(-11*cm,-1*cm + 2*cm*random.random(),-1*cm + 2*cm*random.random()))
        self.particleGun.SetParticleEnergy(energy)  
        self.particleGun.GeneratePrimaryVertex(anEvent)


# In [3]: NEUTRON DETECTOR
# Make a ND array to store information
neutron_event = {
    "eid": [],
    "edep": []
}
class neutron_tracker(g4.G4VSensitiveDetector):
    def ProcessHits(self, aStep, ROhist):
        
        pdg = (aStep.GetTrack().GetParticleDefinition().GetPDGEncoding())
        if not (pdg == 2112): return 0
        print("NEUTRON FOUND!")

        eid = int(gRunManager.GetCurrentEvent().GetEventID())

        neutron_event["eid"].append( eid )
        
        pos = aStep.GetPreStepPoint().GetPosition() 
        dirs = aStep.GetTrack().GetMomentumDirection() 
        ek = aStep.GetPreStepPoint().GetTotalEnergy() 

        neutron_event["edep"].append(aStep.GetTotalEnergyDeposit())

        aStep.GetTrack().SetTrackStatus(g4.G4TrackStatus.fStopAndKill)

        return 1

det = neutron_tracker("neutron_det")


# In[3]:

def build_world():
  mat = g4.gNistManager.FindOrBuildMaterial("G4_WATER")
  plac = g4.build_component("world", solid="box", x=5*m, y=5*m, z=5*m, material=mat)
  hdpe_outer = g4.build_component("shell", solid="tubs", rmax=22*cm, z=1.2*m/2, mother=plac, material="G4_POLYETHYLENE", color=[0.0,0.0,1.0,0.8], drawstyle="solid")
  water_inner = g4.build_component("water", solid="tubs", rmax=18*cm, z=1.2*m/2, mother=hdpe_outer, material="G4_WATER", color=[0.5,0.5,1.0,0.1], drawstyle="solid")
  hdpe_endcap1 = g4.build_component("cap1", solid="tubs", rmax=18*cm, z=1*cm, mother=water_inner, material="G4_POLYETHYLENE", color=[1.0,0.2,1.0,0.8], drawstyle="solid", pos=[0.0, 0.0, +1.2*m/2 - 1*cm])
  hdpe_endcap2 = g4.build_component("cap2", solid="tubs", rmax=18*cm, z=1*cm, mother=water_inner, material="G4_POLYETHYLENE", color=[1.0,0.2,1.0,0.8], drawstyle="solid", pos=[0.0, 0.0, -1.2*m/2 + 1*cm])

  # Assign our detector
  hdpe_outer.GetLogicalVolume().SetSensitiveDetector(det)

  return g4.World(plac)



# In [4]:
# Add Physics List
physics = g4.QGSP_BERT()
gRunManager.SetUserInitialization(physics)

# Add a World
detector = build_world()
gRunManager.SetUserInitialization(detector)

# Add a Generator
gen = custom_generator()
gRunManager.SetUserAction(gen)

# Add standard GEANT4 Actions
g4.add_default_actions(gRunManager)


# In[5]:
gRunManager.Initialize()


# In[6]:
g4.handle_beam(gRunManager, 1000)
