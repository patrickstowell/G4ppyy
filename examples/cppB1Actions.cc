//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
//
/// \file cppB1Actions.cc
/// \brief Implementation of User Actions for g4ppyy Example B1

#include "G4Event.hh"
#include "G4LogicalVolume.hh"
#include "G4UserEventAction.hh"
#include "G4AccumulableManager.hh"
#include "G4RunManager.hh"
#include "G4Step.hh"
#include "G4Run.hh"
#include "G4UserRunAction.hh"
#include "G4Accumulable.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"

class RunAction : public G4UserRunAction
{
public:
    RunAction();
    ~RunAction() override = default;

    void BeginOfRunAction(const G4Run *) override;
    void EndOfRunAction(const G4Run *) override;

    void AddEdep(G4double edep);

private:
    G4Accumulable<G4double> fEdep = 0.;
    G4Accumulable<G4double> fEdep2 = 0.;
};

RunAction::RunAction()
{
    // add new units for dose
    //
    const G4double milligray = 1.e-3 * gray;
    const G4double microgray = 1.e-6 * gray;
    const G4double nanogray = 1.e-9 * gray;
    const G4double picogray = 1.e-12 * gray;

    new G4UnitDefinition("milligray", "milliGy", "Dose", milligray);
    new G4UnitDefinition("microgray", "microGy", "Dose", microgray);
    new G4UnitDefinition("nanogray", "nanoGy", "Dose", nanogray);
    new G4UnitDefinition("picogray", "picoGy", "Dose", picogray);

    // Register accumulable to the accumulable manager
    G4AccumulableManager *accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->RegisterAccumulable(fEdep);
    accumulableManager->RegisterAccumulable(fEdep2);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::BeginOfRunAction(const G4Run *)
{
    // inform the runManager to save random number seed
    G4RunManager::GetRunManager()->SetRandomNumberStore(false);

    // reset accumulables to their initial values
    G4AccumulableManager *accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Reset();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::EndOfRunAction(const G4Run *run)
{

    // Merge accumulables
    G4AccumulableManager *accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Merge();

    // Compute dose = total energy deposit in a run and its variance
    G4double edep = fEdep.GetValue();
    G4double edep2 = fEdep2.GetValue();

    G4cout << "edep:" << edep << G4endl;
    G4cout << "edep2:" << edep2 << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::AddEdep(G4double edep)
{
    fEdep += edep;
    fEdep2 += edep * edep;
}

class EventAction : public G4UserEventAction
{
public:
    EventAction(RunAction *runAction);
    ~EventAction() override = default;

    void BeginOfEventAction(const G4Event *event) override;
    void EndOfEventAction(const G4Event *event) override;

    void AddEdep(G4double edep) { fEdep += edep; }

private:
    RunAction *fRunAction = nullptr;
    G4double fEdep = 0.;
};

EventAction::EventAction(RunAction *runAction) : fRunAction(runAction) {}

void EventAction::BeginOfEventAction(const G4Event *)
{
    fEdep = 0.;
}

void EventAction::EndOfEventAction(const G4Event *)
{
    fRunAction->AddEdep(fEdep);
}

class SteppingAction : public G4UserSteppingAction
{
public:
    SteppingAction(EventAction *eventAction);
    ~SteppingAction() override = default;

    // method from the base class
    void UserSteppingAction(const G4Step *) override;

    EventAction *fEventAction = nullptr;
    G4LogicalVolume *fScoringVolume = nullptr;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

SteppingAction::SteppingAction(EventAction *eventAction) : fEventAction(eventAction)
{
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void SteppingAction::UserSteppingAction(const G4Step *step)
{
    if (!fScoringVolume)
    {
        G4LogicalVolumeStore *lvStore = G4LogicalVolumeStore::GetInstance();
        fScoringVolume = lvStore->GetVolume("Shape2", false);
    }

    // get volume of the current step
    G4LogicalVolume *volume =
        step->GetPreStepPoint()->GetTouchableHandle()->GetVolume()->GetLogicalVolume();

    // check if we are in scoring volume
    if (volume != fScoringVolume)
        return;

    // collect energy deposited in this step
    G4double edepStep = step->GetTotalEnergyDeposit();
    fEventAction->AddEdep(edepStep);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
