import FWCore.ParameterSet.Config as cms

job_label = "PU25BX50"

process = cms.Process("MULTITRACKVALIDATOR")

# message logger
process.MessageLogger = cms.Service("MessageLogger",
     default = cms.untracked.PSet( limit = cms.untracked.int32(10) )
)

# source
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( ['file:./step3_%sNODUP_RAW2DIGI_L1Reco_RECO_DQM.root' % job_label] );


secFiles.extend( ['/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_10_1_lE9.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_11_1_9at.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_12_1_Eqg.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_13_1_rGd.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_14_1_lWN.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_15_1_oKP.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_16_1_QzE.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_17_1_QYY.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_18_1_BRT.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_19_1_NQr.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_1_1_JHw.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_20_1_BxW.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_21_1_dQZ.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_22_1_FG4.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_23_1_sBy.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_24_1_P1i.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_25_1_p0i.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_26_1_ojK.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_27_1_CGC.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_28_1_jVc.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_29_1_c2F.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_2_1_JHP.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_30_1_fS1.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_31_1_anK.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_32_1_LiK.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_33_1_0jO.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_34_1_eBH.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_35_1_Lh3.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_36_1_Djx.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_37_1_hWt.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_38_1_0G9.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_39_1_bRi.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_3_1_OF6.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_40_1_3py.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_41_1_E9Z.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_42_1_9my.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_43_1_yRG.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_44_1_Ppn.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_45_1_7nE.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_46_1_JVV.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_47_1_6oW.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_48_1_o10.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_49_1_RCB.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_4_1_tLM.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_50_1_Epy.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_5_1_M8r.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_6_1_dMe.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_7_1_Lx0.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_8_1_lXy.root',
                  '/store/caf/user/rovere/6_2_0_pre7/DIGI/AVE_PU25_BX50/TTbar/DIGI_PU25_BX50_DIGI_L1_DIGI2RAW_HLT_PU_9_1_jXm.root'
                  ] );

process.source = source
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

### conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

### standard includes
process.load('Configuration/StandardSequences/Services_cff')
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
process.multiTrackValidator.outputFile = 'multitrackvalidator_%s.root' % job_label
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
process.multiTrackValidator.ptMinTP = cms.double(0.4)
process.multiTrackValidator.lipTP = cms.double(35.0)
process.multiTrackValidator.tipTP = cms.double(70.0)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.ptMin = cms.double(0.4)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.lip   = cms.double(35.0)
process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.tip   = cms.double(70.0)
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsEta  = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsPhi  = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsPt   = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsVTXR = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()
process.multiTrackValidator.histoProducerAlgoBlock.TpSelectorForEfficiencyVsVTXZ = process.multiTrackValidator.histoProducerAlgoBlock.generalTpSelector.clone()

# Numerator: cuts on Reco Tracks ... ?
process.load("Validation.RecoTrack.cuts_cff")
process.cutsRecoTracks.quality = cms.vstring('','highPurity')
#process.cutsRecoTracks.quality = cms.vstring('')
# process.cutsRecoTracks.ptMin    = cms.double(0.4)
# process.cutsRecoTracks.lip = cms.double(35.0)
# process.cutsRecoTracks.tip = cms.double(70.0)
#process.cutsRecoTracks.minHit   = cms.int32(10)

#process.cutsRecoTracks.minRapidity  = cms.int32(-1.0)
#process.cutsRecoTracks.maxRapidity  = cms.int32(1.0)

process.quickTrackAssociatorByHits.useClusterTPAssociation = cms.bool(True)
#process.load("SimTracker.TrackerHitAssociation.clusterTpAssociationProducer_cfi")

process.validation = cms.Sequence(
#    process.tpClusterProducer *
    process.multiTrackValidator
)

# paths
process.p = cms.Path(
      process.cutsRecoTracks
    * process.validation
)
process.schedule = cms.Schedule(
      process.p
)


