# Auto generated configuration file
# using:
# Revision: 1.20
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: step3_25PU --step RAW2DIGI,L1Reco,RECO,DQM --conditions auto:startup --eventcontent RECO,DQM --datatier RECO,DQM --filein file:step2_40PU_DIGI_L1_DIGI2RAW_HLT_PU.root -n -1 --no_exec
import FWCore.ParameterSet.Config as cms
import commands

JOB_LABEL = "PU50_BX50"

# Do not forget trailing '/'.
EOS_REPO = '/store/caf/user/cerati/7_1_0_pre7/DIGI-NO-PIX-DYN-INEF/AVE_%s/TTbar/' % JOB_LABEL
# Grab it after some lookups throu type -a eoscms/eos
EOS_COMMAND = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select'

process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(200)
)

# Input source

# Grab files dynamically from the specified eos directory
input_files = commands.getoutput('%s ls %s' % (EOS_COMMAND, EOS_REPO))
input_files = input_files.split('\n')
input_files = map(lambda x: '%s%s' %(EOS_REPO, x), input_files)

process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
#    fileNames = cms.untracked.vstring('file:./step3_25PU_RAW2DIGI_L1Reco_RECO_DQM.root')
    fileNames = cms.untracked.vstring(input_files)
                            )

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('step3_%s nevts:-1' % JOB_LABEL),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('step3_%sNODUP_RAW2DIGI_L1Reco_RECO_DQM.root' % JOB_LABEL),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('RECO')
    )
)

process.DQMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.DQMEventContent.outputCommands,
    fileName = cms.untracked.string('step3_%sNODUP_RAW2DIGI_L1Reco_RECO_DQM_inDQM.root' % JOB_LABEL),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('DQM')
    )
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.dqmoffline_step = cms.Path(process.DQMOffline)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

process.load('DQMServices.Components.DQMFileSaver_cfi')
process.dqmSaver.workflow = cms.untracked.string('/MyTiming/Release710pre7/%s' % JOB_LABEL)
process.DQMFile = cms.EndPath(process.dqmSaver)
process.DQMStore.enableMultiThread = cms.untracked.bool(True)
process.dqmSaver.enableMultiThread = cms.untracked.bool(True)
process.FastTimerService.dqmTimeRange = cms.untracked.double(200000)
process.FastTimerService.dqmTimeResolution = cms.untracked.double(100)
process.FastTimerService.dqmPathTimeRange = cms.untracked.double(200000)
process.FastTimerService.dqmPathTimeResolution = cms.untracked.double(100)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,
                                process.L1Reco_step,
                                process.reconstruction_step,
                                process.dqmoffline_step,
                                process.DQMFile,
                                process.endjob_step,
                                process.RECOoutput_step,
                                process.DQMoutput_step)

