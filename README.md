PREAMBLE
========

**Run only from lxplus* machines, since we need the local batch queue available.**


Source CRAB ENVs
----------------

```
source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh

source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh
voms-proxy-init
```

Submit CRAB JOB
---------------
```
crab -create -cfg crab_TTbar.cfg
crab -submit -c crab_*_*
crab -status -c crab_*_*
crab -resubmit -c crab_*_* 1,2...
```


General Procedure
=================

Caveat
------

Few branches will be provided with all the explained process already
done.

Procedure
---------

1. The first step is to produce the GEN-SIM samples for the process
you want to study (these files will be used as configuration files for
the CRAB JOB (see next point)):

  1. `cmsDriver.py TTbar_Tauola_13TeV_cfi.py --conditions auto:startup -n 1000 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --no_exec` for signal
  1. `cmsDriver.py MinBias_13TeV_cfi.py --conditions auto:startup -n 1000 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --no_exec` for PU

1. Create a proper CRAB config [1]: this file will use the proper
python configuration file, split the job according the instructions
and save the output on the caf storage element. Remember to tuned the
output directory to the reflect the same release used to produce the
GEN-SIM sample.

1. DIGI+PU step.
  1. `cmsDriver.py DIGI_PU25_BX50 --datatier GEN-SIM-RAW --conditions auto:startup -s DIGI,L1,DIGI2RAW,HLT:@relval --eventcontent FEVTDEBUG -n 500 --filein /eos/something --pileup AVE_25_BX_50ns --pileup_input /eos/somthingelse —no_exec`.
  1. You must edit the produced python file and change:
    1. Use as input files for the mixing module the ones produced at
    the previous point, for the MinBias[2].
    1. Change the PU, including OOT, parameters to reflect your
    needs. In particular, pay attention to this example[3].
1. Prepare another CRAB cfg to submit the DIGI+PU step[4].

1. use this anchillary scripts[5] to customize the input files.

1. Remember to produce the file TTbar_fullList.txt with the list of
   signs files produced in the previous step. Example of a possible
   simple command to do that:
   ```touch TTbar_fullList.txt && eospath='/store/caf/user/rovere/7_0_0/GEN-SIM/TTbar/' && for f in `eoscms ls ${eospath}`; do echo ${eospath}${f} >>TTbar_fullList.txt; done```

1. Also add another file to customize, in case it is needed, the rss
   requirements of the jb rss[6].

1. Run now the full RECO(+DQM for timing only) sequence:
  1. `step3_25PU --step RAW2DIGI,L1Reco,RECO,DQM --conditions auto:startup --eventcontent RECO,DQM --datatier RECO,DQM --filein file:step2_40PU_DIGI_L1_DIGI2RAW_HLT_PU.root -n -1 —no_exec`
  1. change the input files and use the ones produced at the previous point.
  1. use this[7] customization





# References

[1]
```
[CRAB]
jobtype                  = cmssw
scheduler                = caf
use_server               = 0

[CMSSW]
datasetpath              = none
pset                     = MinBias_13TeV_cfi_py_GEN_SIM.py
get_edm_output           = 1
total_number_of_events   = 500
events_per_job           = 10

[USER]
thresholdLevel           = 100
eMail                    = marco.rovere@cern.ch
return_data              = 0
copy_data                = 1
storage_element          = T2_CH_CERN
#storage_path             = /srm/v2/server?SFN=/eos/cms
user_remote_dir          = 6_2_3_patch1/GEN-SIM/MinBias

[LSF]
queue                    = 1nh

[CAF]
queue                    = cmscaf1nh
```

[2]
```
process.mix.input.fileNames = cms.untracked.vstring(['/store/caf/user/rovere/6_2_3_patch1/GEN-SIM/MinBias/MinBias_13TeV_cfi_py_GEN_SIM_10_1_rhB.root',
                                                     …, …, …])
```

[3]
```
process.mix.input.nbPileupEvents.averageNumber = cms.double(25.000000)
process.mix.bunchspace = cms.int32(50)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
```


[4] crab_localDIGI.cfg
```
[CRAB]
jobtype                  = cmssw
scheduler                = caf
use_server               = 0

[CMSSW]
datasetpath              = none
pset                     = DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU.py
get_edm_output           = 1
total_number_of_events   = 500
events_per_job           = 10

[USER]
additional_input_files   = TTbar_fullList.txt,set_inputFiles.py
script_exe               = set_inputFiles.sh
thresholdLevel           = 100
eMail                    = marco.rovere@cern.ch
return_data              = 0
copy_data                = 1
storage_element          = T2_CH_CERN
#storage_path             = /srm/v2/server?SFN=/eos/cms
user_remote_dir          = 6_2_3_patch1/DIGI/AVE_PU25_BX50/TTbar

[LSF]
queue                    = 1nh

[CAF]
queue                    = cmscaf1nh
```


[5] set_inputFiles.py
```
import FWCore.ParameterSet.Config as cms
import pickle
import sys

cfg = pickle.load(open('pset.py.pkl', 'rb'))
cfg.source.fileNames = cms.untracked.vstring('%s' % sys.argv[1])
cfg.maxEvents.input = cms.untracked.int32(-1)


pickle.dump(cfg, open('pset2.py.pkl', 'wb'))
```


[6] set_inputFiles.sh
```
#!/bin/bash

filename=$(cat TTbar_fullList.txt | sed -n $1,$1p)
echo "Using $filename as input"
python set_inputFiles.py $filename
mv pset{2,}.py.pkl
#sed -i -e 's#@INPUTFILES@#$filename#' pset.py
cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml -p pset.py
```

[7]
```
process.load('DQMServices.Components.DQMFileSaver_cfi')
process.dqmSaver.workflow = cms.untracked.string('/MyTimingNODUP/Release623p1/%s' % job_label)
process.DQMFile = cms.EndPath(process.dqmSaver)
process.FastTimerService.dqmTimeRange = cms.untracked.double(200000)
process.FastTimerService.dqmTimeResolution = cms.untracked.double(100)
process.FastTimerService.dqmPathTimeRange = cms.untracked.double(200000)
process.FastTimerService.dqmPathTimeResolution = cms.untracked.double(100)
process.load('TrackingTests.DemoTrackAnalyzer.demoTrackAnalyzer_cfi')
```

[rss]
cat rssLimit
```
5000000
```

