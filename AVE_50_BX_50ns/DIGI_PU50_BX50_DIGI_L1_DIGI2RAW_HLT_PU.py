# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: DIGI_PU50_BX50 --datatier GEN-SIM-RAW --conditions auto:startup -s DIGI,L1,DIGI2RAW,HLT:@relval --eventcontent FEVTDEBUG -n 500 --filein /eos/something --pileup AVE_50_BX_50ns --pileup_input /eos/somthingelse --no_exec
import FWCore.ParameterSet.Config as cms
import commands
# Do not forget trailing '/'.
EOS_REPO = '/store/caf/user/rovere/7_0_0/GEN-SIM/MinBias/'
# Grab it after some lookups throu type -a eoscms/eos
EOS_COMMAND = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select'

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_2013_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('@INPUTFILES@')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('DIGI_PU50_BX50 nevts:500'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    fileName = cms.untracked.string('DIGI_PU50_BX50_DIGI_L1_DIGI2RAW_HLT_PU.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    )
)

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(50.000000)
process.mix.bunchspace = cms.int32(50)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
# Grab files dynamically from the specified eos directory
mix_files = commands.getoutput('%s ls %s' % (EOS_COMMAND, EOS_REPO))
mix_files = mix_files.split('\n')
mix_files = map(lambda x: '%s%s' %(EOS_REPO, x), mix_files)
process.mix.input.fileNames = cms.untracked.vstring(mix_files)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.FEVTDEBUGoutput_step])

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

#### TURN OFF PIXEL DYNAMIC INEFFICIENCY ####
#with this option you can turn on/off the whole efficiency simulation (when 'false' you'll have 100% efficiency);
#it is true by default
process.mix.digitizers.pixel.AddPixelInefficiencyFromPython = cms.bool(True)
#these are the variables you have to alter to get the efficiency simulation
#without dynamic inefficiency
process.mix.digitizers.pixel.thePixelColEfficiency_BPix1 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelColEfficiency_BPix2 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelColEfficiency_BPix3 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelEfficiency_BPix1 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelEfficiency_BPix2 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelEfficiency_BPix3 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelChipEfficiency_BPix1 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelChipEfficiency_BPix2 = cms.double(0.999)
process.mix.digitizers.pixel.thePixelChipEfficiency_BPix3 = cms.double(0.999)
process.mix.digitizers.pixel.theLadderEfficiency_BPix1 = cms.vdouble(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0)
process.mix.digitizers.pixel.theModuleEfficiency_BPix1 = cms.vdouble(1.0,1.0,1.0,1.0)
process.mix.digitizers.pixel.thePUEfficiency_BPix1 = cms.vdouble(1.0)
process.mix.digitizers.pixel.theLadderEfficiency_BPix2 = cms.vdouble(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0)
process.mix.digitizers.pixel.theModuleEfficiency_BPix2 = cms.vdouble(1.0,1.0,1.0,1.0)
process.mix.digitizers.pixel.thePUEfficiency_BPix2 = cms.vdouble(1.0)
process.mix.digitizers.pixel.theLadderEfficiency_BPix3 = cms.vdouble(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,
                                                                     1.0,1.0,1.0,1.0)
process.mix.digitizers.pixel.theModuleEfficiency_BPix3 = cms.vdouble(1.0,1.0,1.0,1.0)
process.mix.digitizers.pixel.thePUEfficiency_BPix3 = cms.vdouble(1.0)

# End of customisation functions
