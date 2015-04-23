* Use as a baseline wfl 25207.
* Generated 9000 SingleMuPt10 events and 1K NeutrinoGun events

  cmsDriver.py SingleNuE10_cfi.py  --conditions auto:run2_mc -n 1000 \
  --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier \
  GEN-SIM --beamspot NominalCollision2015 --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --no_exec

* Generate the SingleMuPt10 simulated events

  cmsDriver.py SingleMuPt10_pythia8_cfi  --conditions auto:run2_mc -n \
  9000 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM \
  --datatier GEN-SIM --beamspot NominalCollision2015 --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --no_exec


* Add the PU at digi step, using the neutrino-gun sample produced
  previously as PU sample and the SingleMuPt10 simulated events as
  signal.

  cmsDriver.py step2  --conditions auto:run2_mc --pileup_input \
  file:./SingleNuE10_cfi_py_GEN_SIM.root -n 9000 --eventcontent \
  FEVTDEBUGHLT --filein file:./SingleMuPt10_pythia8_cfi_GEN_SIM.root \
  -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@frozen25ns,RAW2DIGI,L1Reco --datatier \
  GEN-SIM-DIGI-RAW-HLTDEBUG --pileup AVE_40_BX_25ns --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --no_exec
  
* Run again the DIGI step on the SingleMuPt10 simulated events, but
  this time without adding the PU (so that dynamic inefficiency are
  turned off).

  cmsDriver.py step2  --conditions auto:run2_mc -n 9000 --eventcontent \
  FEVTDEBUGHLT --filein file:./SingleMuPt10_pythia8_cfi_GEN_SIM.root \
  -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@frozen25ns,RAW2DIGI,L1Reco --datatier \
  GEN-SIM-DIGI-RAW-HLTDEBUG --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --no_exec --python_filename=step2_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_NOPU.py
  
* Now run the full RECO,VALIDATION,DQM,EI on both samples

  for the PU case:
  
  cmsDriver.py step3  --conditions auto:run2_mc --pileup_input \
  file:./SingleNuE10_cfi_py_GEN_SIM.root -n 9000 --eventcontent \
  RECOSIM,DQM -s RAW2DIGI,L1Reco,RECO,EI,VALIDATION,DQM --datatier \
  GEN-SIM-RECO,DQMIO --pileup AVE_40_BX_25ns --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --filein file:./step2_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_PU.root \
  --no_exec

  for the NON-PU case:
  
  cmsDriver.py step3  --conditions auto:run2_mc \
  --filein file:./step2_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco.root \
  -n 9000 --eventcontent RECOSIM,DQM -s \
  RAW2DIGI,L1Reco,RECO,EI,VALIDATION,DQM \
  --datatier GEN-SIM-RECO,DQMIO --customise \
  SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --magField 38T_PostLS1 --python_filename=step3_RAW2DIGI_L1Reco_RECO_EI_VALIDATION_DQM_NOPU.py \
  --no_exec

* Now run the Harvesting:
  
  for the PU case:

  cmsDriver.py step4  --conditions auto:run2_mc \
  -s HARVESTING:validationHarvesting+dqmHarvesting --filetype DQM \
  --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1  \
  --mc  --magField 38T_PostLS1 -n -1 \
  --filein file:step3_RAW2DIGI_L1Reco_RECO_EI_VALIDATION_DQM_PU_inDQM.root \
  --no_exec --python_filename step4_HARVESTING_PU.py

  for the NOPU case:

  cmsDriver.py step4  --conditions auto:run2_mc \
  -s HARVESTING:validationHarvesting+dqmHarvesting --filetype DQM \
  --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1  \
  --mc  --magField 38T_PostLS1 -n -1 \
  --filein file:step3_RAW2DIGI_L1Reco_RECO_EI_VALIDATION_DQM_inDQM.root \
  --no_exec --python_filename step4_HARVESTING_NOPU.py


* Now produce MINIAOD out of it

  for the PU case:

  cmsDriver.py step5  --conditions auto:run2_mc -n 9000 \
  --eventcontent MINIAODSIM --runUnscheduled  \
  --filein file:step3_RAW2DIGI_L1Reco_RECO_EI_VALIDATION_DQM_PU.root \
  -s PAT --datatier MINIAODSIM \
  --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --mc --no_exec --python_filename=step5_PAT_PU.py

  for the NOPU case:

  cmsDriver.py step5  --conditions auto:run2_mc -n 9000 \
  --eventcontent MINIAODSIM --runUnscheduled  \
  --filein file:step3_RAW2DIGI_L1Reco_RECO_EI_VALIDATION_DQM.root \
  -s PAT --datatier MINIAODSIM \
  --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 \
  --mc --no_exec --python_filename=step5_PAT_NOPU.py \
  --fileout file:step5_PAT_NOPU.root

* Reco all steps also with SingleMuPt100
