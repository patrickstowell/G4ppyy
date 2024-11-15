import cppyy.ll
cppyy.ll.set_signals_as_exception(True)
import sys
import numba
import cppyy.numba_ext

import g4ppyy as g4
from g4ppyy import new

g4.include("G4RunManagerFactory.hh")
g4.include("G4VUserActionInitialization.hh")

def g4_uniform_rand():
    return g4.CLHEP.HepRandom.getTheEngine().flat()

class CustomWorld(g4.G4VUserDetectorConstruction):
    
    def __init__(self):
       super().__init__()
       self.scoring_volume = None
    
    def Construct(self):
        print("Construct start")
        env_sizeXY = 20 * g4.cm
        env_sizeZ = 30 * g4.cm
        env_mat = new(g4.gNistManager.FindOrBuildMaterial("G4_WATER"))

        check_overlaps = True

        world_sizeXY = 1.2 * env_sizeXY
        world_sizeZ = 1.2 * env_sizeZ
        world_mat = new( g4.gNistManager.FindOrBuildMaterial("G4_AIR") )

        solid_world = new(g4.G4Box("World",
                               0.5*world_sizeXY,
                               0.5*world_sizeXY,
                               0.5*world_sizeZ))
        logic_world = new(g4.G4LogicalVolume(solid_world,
                                         world_mat,
                                         "World"))
        self.phys_world = new(g4.G4PVPlacement(g4.cppyy.nullptr,
                                      g4.G4ThreeVector(),
                                      logic_world,
                                      "World",
                                      g4.cppyy.nullptr,
                                      False,
                                      0,
                                      check_overlaps))
        print("Built world")

        solid_env = new(g4.G4Box("Envelope",
                             0.5*env_sizeXY,
                             0.5*env_sizeXY,
                             0.5*env_sizeZ))
        logic_env = new(g4.G4LogicalVolume(solid_env,
                                       env_mat,
                                       "Envelope"))
        phys_env = new(g4.G4PVPlacement(g4.cppyy.nullptr,
                         g4.G4ThreeVector(),
                         logic_env,
                         "Envelope",
                         logic_world,
                         False,
                         0,
                         check_overlaps))
        print("Built envelope")

        shape1_mat = new(g4.gNistManager.FindOrBuildMaterial("G4_A-150_TISSUE"))
        pos1 = g4.G4ThreeVector(0.0, 2.0*g4.cm, -7.0*g4.cm)

        shape1_rmina = 0.0 * g4.cm
        shape1_rmaxa = 2.0 * g4.cm
        shape1_rminb = 0.0 * g4.cm
        shape1_rmaxb = 4.0 * g4.cm
        shape1_hz = 3.0 * g4.cm
        shape1_phimin = 0.0 * g4.deg
        shape1_phimax = 360.0 * g4.deg
        solid_shape1 = new(g4.G4Cons("Shape1",
                                 shape1_rmina,
                                 shape1_rmaxa,
                                 shape1_rminb,
                                 shape1_rmaxb,
                                 shape1_hz,
                                 shape1_phimin,
                                 shape1_phimax))
        logic_shape1 = new(g4.G4LogicalVolume(solid_shape1, 
                                          shape1_mat, 
                                          "Shape1"))
        phys_shape1 = new(g4.G4PVPlacement(g4.cppyy.nullptr, 
                         pos1, 
                         logic_shape1,
                         "Shape1", 
                         logic_env, 
                         False, 
                         0, 
                         check_overlaps))
        print("Built shape1")
        
        self.shape2_mat = g4.gNistManager.FindOrBuildMaterial("G4_BONE_COMPACT_ICRU")
        pos2 = g4.G4ThreeVector(0, -1*g4.cm, 7.0*g4.cm)

        shape2_dxa = 12.0 * g4.cm
        shape2_dxb = 12.0 * g4.cm
        shape2_dya = 10.0 * g4.cm
        shape2_dyb = 16.0 * g4.cm
        shape2_dz = 6.0 * g4.cm

        self.solid_shape2 = g4.G4Trd("Shape2",
                                0.5 * shape2_dxa, 
                                0.5 * shape2_dxb,
                                0.5 * shape2_dya, 
                                0.5 * shape2_dyb,
                                0.5 * shape2_dz)
        self.logic_shape2 = g4.G4LogicalVolume(self.solid_shape2,
                                          self.shape2_mat,
                                          "Shape2")
        self.phys_shape2 = g4.G4PVPlacement(g4.cppyy.nullptr,
                         pos2,
                         self.logic_shape2,
                         "Shape2",
                         logic_env,
                         False,
                         0,
                         check_overlaps)
        
        self.scoring_volume = self.logic_shape2
        print("Built shape2")

        print("Construct end")
        return self.phys_world
    
    def get_scoring_volume(self):
        return self.scoring_volume

from g4ppyy import G4ParticleGun, G4ParticleTable, G4ThreeVector, MeV


class CustomGenerator(g4.G4VUserPrimaryGeneratorAction):

    def __init__(self):
        print("Custom generator")
        super().__init__()
        
        n_particle = 1
        self.particle_gun = G4ParticleGun(n_particle)

        particle_table = G4ParticleTable.GetParticleTable()
        particle = particle_table.FindParticle("gamma")
        self.particle_gun.SetParticleDefinition(particle)
        self.particle_gun.SetParticleMomentumDirection(G4ThreeVector(0.,0.,1.))
        self.particle_gun.SetParticleEnergy(6.0 * MeV)

        self.envelope_box = None

    def GeneratePrimaries(self, event):
        env_sizeXY = 0
        env_sizeZ = 0

        if not self.envelope_box:
            env_lv = g4.G4LogicalVolumeStore.GetInstance().GetVolume("Envelope")
            self.envelope_box = env_lv.GetSolid()
        
        if self.envelope_box:
            env_sizeXY = self.envelope_box.GetXHalfLength() * 2.0
            env_sizeZ = self.envelope_box.GetZHalfLength() * 2.0
        else:
            raise RuntimeError("Could not find envelope box")
        
        size = 0.8
        x0 = size * env_sizeXY * (g4_uniform_rand() - 0.5)
        y0 = size * env_sizeXY * (g4_uniform_rand() - 0.5)
        z0 = -0.5 * env_sizeZ
        
        self.particle_gun.SetParticlePosition(G4ThreeVector(x0,y0,z0))

        self.particle_gun.GeneratePrimaryVertex(event)

class CustomAccumulableManager(g4.G4AccumulableManager):
    
    def __init__(self):
        super().__init__()



from g4ppyy import G4Accumulable, G4double, G4AccumulableManager

class CustomRunAction(g4.G4UserRunAction):
    
    def __init__(self):
        super().__init__()
        self.edep = G4Accumulable[G4double](0)
        self.edep2 = G4Accumulable[G4double](0)
        self.accumulableManager = G4AccumulableManager.Instance()
        self.accumulableManager.RegisterAccumulable(self.edep)
        self.accumulableManager.RegisterAccumulable(self.edep2)
    
    def BeginOfRunAction(self, g4run):
        g4.G4RunManager.GetRunManager().SetRandomNumberStore(False)
        self.accumulableManager.Reset()
        pass
    
    def EndOfRunAction(self, g4run):
        self.accumulableManager.Merge()
        edep = self.edep.GetValue()
        edep2 = self.edep2.GetValue()
        print(f"edep: {edep}")
        print(f"edep2 {edep2}")
    
    def addEdep(self, edep):
        self.edep += edep
        self.edep2 += edep * edep
        
class CustomEventAction(g4.G4UserEventAction):
    
    def __init__(self, run_action):
        super().__init__()
        self.edep = 0
        self.run_action = run_action
    
    def BeginOfEventAction(self, event):
        self.edep = 0
    
    def EndOfEventAction(self, event):
        self.run_action.addEdep(self.edep)
        pass

    def addEdep(self, edep):
        self.edep += edep
        

class CustomSteppingAction(g4.G4UserSteppingAction):
    
    def __init__(self, event_action):
        super().__init__()
        self.event_action = event_action
        self.scoring_volume = None
    
    def UserSteppingAction(self, step):
        if not self.scoring_volume:
            det_con = g4.G4RunManager.GetRunManager().GetUserDetectorConstruction()
            self.scoring_volume = det_con.get_scoring_volume()
            
        volume = step.GetPreStepPoint().GetTouchableHandle().GetVolume().GetLogicalVolume()
        if volume != self.scoring_volume:
            return
        
        edep_step = step.GetTotalEnergyDeposit()
        self.event_action.addEdep(edep_step)

class CustomAction(g4.G4VUserActionInitialization):
    
    def __init__(self):
       super().__init__()
    
    def BuildForMaster(self):
        run_action = CustomRunAction()
        self.SetUserAction(run_action)
        # pass
    
    def Build(self):
        print("Custom action")
        self.gen = CustomGenerator()
        self.SetUserAction(self.gen)
        
        self.run_action = CustomRunAction()
        self.SetUserAction(self.run_action)
        
        self.event_action = CustomEventAction(self.run_action)
        self.SetUserAction(self.event_action)
        
        self.step_action = CustomSteppingAction(self.event_action)
        self.SetUserAction(self.step_action)

        

def main(argc, argv):

    run_manager = g4.G4RunManagerFactory.CreateRunManager(g4.G4RunManagerType.Serial)
    custom_world = new(CustomWorld())
    run_manager.SetVerboseLevel(1)
    run_manager.SetUserInitialization(custom_world)
    physics_list = g4.QBBC()
    physics_list.SetVerboseLevel(-1)
    run_manager.SetUserInitialization(physics_list)
    custom_action = CustomAction()
    run_manager.SetUserInitialization(custom_action)

    run_manager.Initialize()
    run_manager.BeamOn(100000)

    print("FINISHED")

if __name__ == "__main__":
    argc = len(sys.argv)
    main(argc, sys.argv)
