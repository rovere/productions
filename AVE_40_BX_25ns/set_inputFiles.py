import FWCore.ParameterSet.Config as cms
import pickle
import sys

cfg = pickle.load(open('pset.py.pkl', 'rb'))
cfg.source.fileNames = cms.untracked.vstring('%s' % sys.argv[1])
cfg.maxEvents.input = cms.untracked.int32(-1)


pickle.dump(cfg, open('pset2.py.pkl', 'wb'))

