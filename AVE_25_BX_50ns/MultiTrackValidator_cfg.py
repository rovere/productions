import FWCore.ParameterSet.Config as cms

import commands

JOB_LABEL = "PU25_BX50"

# Do not forget trailing '/'.
EOS_REPO = '/store/group/phys_tracking/samples_710pre7/DIGI/AVE_%s/TTbar/' % JOB_LABEL
# Grab it after some lookups throu type -a eoscms/eos
EOS_COMMAND = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select'

process = cms.Process("MULTITRACKVALIDATOR")

# message logger
process.MessageLogger = cms.Service("MessageLogger",
     default = cms.untracked.PSet( limit = cms.untracked.int32(10) )
)

# source
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
readFiles.extend( ['/store/group/phys_tracking/samples_710pre8/RECO/AVE_%s/TTbar/step3_%sNODUP_RAW2DIGI_L1Reco_RECO_DQM.root' %(JOB_LABEL,JOB_LABEL)] );
#readFiles.extend( ['file:./step3_%sNODUP_RAW2DIGI_L1Reco_RECO_DQM.root' % JOB_LABEL] );

# Grab files dynamically from the specified eos directory
input_files = commands.getoutput('%s ls %s' % (EOS_COMMAND, EOS_REPO))
input_files = input_files.split('\n')
input_files = map(lambda x: '%s%s' %(EOS_REPO, x), input_files)
secFiles.extend(input_files)

source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)

process.source = source
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

### conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

### standard includes
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

### validation-specific includes
#process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociation.quickTrackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
process.load("Validation.RecoTrack.cuts_cff")
process.load("Validation.RecoTrack.MultiTrackValidator_cff")
process.load("DQMServices.Components.EDMtoMEConverter_cff")
process.load("Validation.Configuration.postValidation_cff")
process.quickTrackAssociatorByHits.SimToRecoDenominator = cms.string('reco')

########### configuration MultiTrackValidator ########
process.multiTrackValidator.outputFile = 'multitrackvalidator_%s.root' % JOB_LABEL
process.multiTrackValidator.associators = ['quickTrackAssociatorByHits']
process.multiTrackValidator.skipHistoFit=cms.untracked.bool(False)
process.multiTrackValidator.label = ['cutsRecoTracks']
process.multiTrackValidator.useLogPt=cms.untracked.bool(True)
process.multiTrackValidator.minpT = cms.double(0.1)
process.multiTrackValidator.maxpT = cms.double(3000.0)
process.multiTrackValidator.nintpT = cms.int32(40)
process.multiTrackValidator.UseAssociators = cms.bool(True)
process.multiTrackValidator.runStandalone = cms.bool(True)

### TP+Efficiency Cuts Configuration ###
process.multiTrackValidator.minHitTP = cms.int32(0)
process.multiTrackValidator.ptMinTP = cms.double(0.5)
process.multiTrackValidator.lipTP = cms.double(30.0)
process.multiTrackValidator.tipTP = cms.double(60.0)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.minHit = cms.int32(0)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.ptMin = cms.double(0.5)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.lip   = cms.double(30.0)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.tip   = cms.double(60.0)
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsEta  = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsPhi  = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsPt   = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsVTXR = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsVTXZ = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()

# Numerator: cuts on Reco Tracks ... ?
process.load("Validation.RecoTrack.cuts_cff")
process.cutsRecoTracks.quality = cms.vstring('highPurity')
#process.cutsRecoTracks.quality = cms.vstring('')
#process.cutsRecoTracks.ptMin    = cms.double(0.4)
#process.cutsRecoTracks.lip = cms.double(35.0)
#process.cutsRecoTracks.tip = cms.double(70.0)
#process.cutsRecoTracks.minHit   = cms.int32(10)

#process.cutsRecoTracks.minRapidity  = cms.int32(-1.0)
#process.cutsRecoTracks.maxRapidity  = cms.int32(1.0)

process.quickTrackAssociatorByHits.useClusterTPAssociation = cms.bool(True)
process.load("SimTracker.TrackerHitAssociation.clusterTpAssociationProducer_cfi")


# Add on the fly harvesting to have also eff/fake and all the rest
# computed on the fly. Being it based on the main DQM GenericClient,
# it will run at endJob.

process.load("Validation.RecoTrack.PostProcessorTracker_cfi")
process.postProcessorTrack.outputFileName = cms.untracked.string("multitrackValidator_%s_postProcess.root" % JOB_LABEL)

process.validation = cms.Sequence(
    process.tpClusterProducer *
    process.multiTrackValidator *
    process.postProcessorTrack
    )

# paths
process.p = cms.Path(
    process.cutsRecoTracks
    * process.validation
    )
process.schedule = cms.Schedule(
    process.p
    )


