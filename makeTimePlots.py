#!/bin/env python

import sys
import re
import copy
import os
import math
from array import array

RXPU = re.compile(r"AVE_(\d+)_BX_(\d+)ns.*")
PUBX = re.compile(r".*PU(\d+)_BX(\d+).root$")
CLUSTER_CHARGE = re.compile(r".*ClusterChargeCut.*root$")
ERR_BAD_FILE = 1

iterLabels = {}
iterLabels['0_initialStep'] = ['initialStepClusters',
                               'initialStepSeedLayers',
                               'initialStepSeeds',
                               'initialStepTrackCandidates',
                               'initialStepTracks',
                               'initialStepSelector',
                               'initialStep']
iterLabels['1_lowPt'] = ['lowPtTripletStepClusters',
                         'lowPtTripletStepSeedLayers',
                         'lowPtTripletStepSeeds',
                         'lowPtTripletStepTrackCandidates',
                         'lowPtTripletStepTracks',
                         'lowPtTripletStepSelector']
iterLabels['2_pixelPair'] = ['pixelPairStepClusters',
                             'pixelPairStepSeedLayers',
                             'pixelPairStepSeeds',
                             'pixelPairStepTrackCandidates',
                             'pixelPairStepTracks',
                             'pixelPairStepSelector']
iterLabels['3_detachedTriplet'] = ['detachedTripletStepClusters',
                                   'detachedTripletStepSeedLayers',
                                   'detachedTripletStepSeeds',
                                   'detachedTripletStepTrackCandidates',
                                   'detachedTripletStepTracks',
                                   'detachedTripletStepSelector',
                                   'detachedTripletStep']
iterLabels['4_mixedTriplet'] = ['mixedTripletStepClusters',
                                'mixedTripletStepSeedLayersA',
                                'mixedTripletStepSeedLayersB',
                                'mixedTripletStepSeedsA',
                                'mixedTripletStepSeedsB',
                                'mixedTripletStepSeeds',
                                'mixedTripletStepTrackCandidates',
                                'mixedTripletStepTracks',
                                'mixedTripletStepSelector',
                                'mixedTripletStep']
iterLabels['5_pixelLess'] = ['pixelLessStepClusters',
                             'pixelLessStepSeedClusters',
                             'pixelLessStepSeedLayers',
                             'pixelLessStepSeeds',
                             'pixelLessStepTrackCandidates',
                             'pixelLessStepTracks',
                             'pixelLessStepSelector',
                             'pixelLessStep']
iterLabels['6_tobtec'] = ['tobTecStepClusters',
                          'tobTecStepSeedClusters',
                          'tobTecStepSeedLayersTripl',
                          'tobTecStepSeedLayersPair',
                          'tobTecStepSeedsTripl',
                          'tobTecStepSeedsPair',
                          'tobTecStepSeeds',
                          'tobTecStepTrackCandidates',
                          'tobTecStepTracks',
                          'tobTecStepSelector']
iterLabels['earlyGeneralTracks'] = ['earlyGeneralTracks']
iterLabels['muonSeededStep'] = ['earlyMuons',
                                'muonSeededSeedsInOut',
                                'muonSeededSeedsInOut',
                                'muonSeededTracksInOut',
                                'muonSeededSeedsOutIn',
                                'muonSeededTrackCandidatesOutIn',
                                'muonSeededTracksOutIn',
                                'muonSeededTracksInOutSelector',
                                'muonSeededTracksOutInSelector']
iterLabels['generalTracksSequence'] = ['duplicateTrackCandidates',
                                       'mergedDuplicateTracks',
                                       'duplicateTrackSelector',
                                       'generalTracks']
iterLabels['ConvStep'] = ['convClusters',
                          'convLayerPairs',
                          'photonConvTrajSeedFromSingleLeg',
                          'convTrackCandidates',
                          'convStepTracks',
                          'convStepSelector',
                          'conversionStepTracks']
iterLabels['electronSeedsSeq'] = ['initialStepSeedClusterMask',
                                  'pixelPairStepSeedClusterMask',
                                  'mixedTripletStepSeedClusterMask',
                                  'pixelLessStepSeedClusterMask',
                                  'tripletElectronSeedLayers',
                                  'tripletElectronSeeds',
                                  'tripletElectronClusterMask',
                                  'pixelPairElectronSeedLayers',
                                  'pixelPairElectronSeeds',
                                  'stripPairElectronSeedLayers',
                                  'stripPairElectronSeeds',
                                  'newCombinedSeeds']
iterLabels['doAlldEdXEstimators'] = ['dedxTruncated40',
                                     'dedxHarmonic2',
                                     'dedxDiscrimASmi']

#iterLabels31 = copy.deepcopy(iterLabels)
#iterLabels31['3'] = iterLabels['1']
#iterLabels31['1'] = iterLabels['3']

def checkEnvs():
    localrt = os.getenv("LOCALRT")
    if not localrt:
        print "Error, CMSSW environment not set."
    return

def makeFrame(name, title, xtitle, ytitle, xll, yll, xur, yur):
    c = TCanvas(name, name, 1024, 1024)
    x = array("f", [xll, xur])
    y = array("f", [yll, yur])
    g = TGraphErrors(len(x), x, y)
    g.SetMarkerSize(0)
    g.SetTitle(title)
    g.GetXaxis().SetTitle(xtitle)
    g.GetYaxis().SetTitle(ytitle)
    setTextProperties(g.GetXaxis(), title=True)
    setTextProperties(g.GetYaxis(), title=True)
    setTextProperties(g.GetXaxis(), label=True)
    setTextProperties(g.GetYaxis(), label=True)
    g.Draw("AP")
    c.Update()
    return c, g  # keep it alive....

def makeGenericTimePlot(kind,
                        measurements,
                        label,
                        color,
                        marker_style,
                        line_type,
                        fill_pattern,
                        legend,
                        legend_kind,
                        print_labels_for_points,
                        pu_labels=[]
                        ):
    print '\n\nStarting rendering of %s of kind %s' %(label, kind)
    gr = []
    pu_text = pu_labels if pu_labels else []
    x = array("f")
    y = array("f")
    iy = []
    iterColor = [kAzure+10, # 0
                 kViolet+10, # 1
                 kPink+10, # 2
                 kOrange+10, # 3
                 kSpring, # 4
                 kViolet, # 5
                 kRed, # 6
                 kBlack+3 # 7
                 ]
    steps = sorted(iterLabels.keys())
    for step in steps:
        iy.append(array("f"))
    ex = array("f")
    ey = array("f")
    if kind == 'TotalRecoTime_vs_PU':
        for i in range(0, len(measurements)):
            x.append(measurements[i].pileup_)
            ex.append(0.)
            y.append(measurements[i].reco_total_time_/1000.)
            ey.append(measurements[i].reco_total_time_rms_/1000.)
    elif kind == 'TotalIterativeTime_vs_PU':
        for i in range(0, len(measurements)):
            x.append(measurements[i].pileup_)
            ex.append(0.)
            y.append(measurements[i].iterative_total_time_/1000./measurements[i].processed_events_) # 1000 for ms
            ey.append(0.)
    elif kind == 'TotalEventTime_vs_PU':
        for i in range(0, len(measurements)):
            x.append(measurements[i].pileup_)
            ex.append(0.)
            y.append(measurements[i].event_time_/1000.)
#            ey.append(measurements[i].event_time_rms_/1000.)
            ey.append(0.)
    elif kind == 'TotalRecoTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].reco_total_time_/1000.)
            ey.append(measurements[i].reco_total_time_rms_/1000.)
    elif kind == 'TotalIterativeTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].iterative_total_time_/1000./measurements[i].processed_events_) # 1000 for ms
            ey.append(0.)
    elif kind == 'TotalEventTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].event_time_/1000.) # 1000 for ms
            ey.append(0.)
    elif kind == 'IterativeTime_vs_PU' or kind == 'IterativeTime_vs_LUMI':
        for i in range(0, len(measurements)):
            if kind == 'IterativeTime_vs_PU':
                x.append(measurements[i].pileup_)
            else:
                x.append(measurements[i].luminosity_)
            ex.append(0.)
            ey.append(0.)
            counter = 0
            for step in steps:
                iy[counter].append(measurements[i].iterative_time_[step]/1000./measurements[i].processed_events_) # 1000 for ms
                counter += 1
    if kind != 'IterativeTime_vs_PU' and kind != 'IterativeTime_vs_LUMI':
        if not legend:
            legend = TLegend(0.13, 0.65, 0.7, 0.9)
            legend.SetFillColor(0)
            legend.SetHeader("PileUp Scenarios")
        print kind
        print x, y
        gr.append(TGraphErrors(len(x), x, y, ex, ey))
        gr[-1].SetMarkerStyle(marker_style)
        gr[-1].SetMarkerColor(color)
        gr[-1].SetMarkerSize(1.5)
        gr[-1].SetFillColor(color)
        gr[-1].SetLineColor(color)
        gr[-1].SetLineStyle(line_type)
        gr[-1].SetLineWidth(2)
        gr[-1].SetFillStyle(fill_pattern)
        gr[-1].Draw("CP3")

        for l in range(0, len(x)):
            if measurements[l].print_labels_:
                pu_text.append(TText(x[l], y[l]*print_labels_for_points[0] + print_labels_for_points[1], "%d" % int(measurements[l].pileup_)))
                setTextProperties(pu_text[-1])
#                pu_text[-1].SetTextFont(23)
#                pu_text[-1].SetTextSize(20)
#                pu_text[-1].SetTextAlign(22)
        legend.AddEntry(gr[-1], label, legend_kind)
        setTextProperties(legend)
        legend.Draw()
    elif kind == 'IterativeTime_vs_PU' or kind == 'IterativeTime_vs_LUMI':
        if not legend:
            legend = TLegend(0.13, 0.45, 0.7, 0.9)
            legend.SetFillColor(0)
            legend.SetHeader("PileUp Scenarios")
        for i in range(len(steps)):
            gr.append(TGraphErrors(len(x), x, iy[i], ex, ey))
            gr[-1].SetMarkerStyle(marker_style+i)
            gr[-1].SetMarkerColor(iterColor[i%len(iterColor)])
            gr[-1].SetMarkerSize(1.2)
            gr[-1].SetFillColor(iterColor[i%len(iterColor)])
            gr[-1].SetLineColor(iterColor[i%len(iterColor)])
            gr[-1].SetLineStyle(line_type)
            gr[-1].SetLineWidth(2)
            gr[-1].SetFillStyle(fill_pattern)
            gr[-1].Draw("CP")
            legend.AddEntry(gr[-1], "%s Iter_%s" % (label, steps[i]), legend_kind)
        for l in range(0, len(x)):
            if measurements[l].print_labels_:
                pu_text.append(TText(x[l], iy[-1][l]*print_labels_for_points[0] + print_labels_for_points[1], "%d" % int(measurements[l].pileup_)))
                setTextProperties(pu_text[-1])
#                pu_text[-1].SetTextFont(23)
#                pu_text[-1].SetTextSize(16)
#                pu_text[-1].SetTextAlign(22)
        setTextProperties(legend)
        legend.Draw()
    return gr,legend,pu_text

def waitKey(quit=False):
    c = raw_input("Quit? ")
    if c not in ['y', 'yes', 'Y']:
        if quit:
            sys.exit()

class Measure:
    SCALE = 1.0 * pow(10, 34);
    MINBIAS_XS = 78. * pow(10, -3) * pow(10, -24);
    FREV  = 11245;  # Hz
    NBB50 = 1380;   # bunches@50ns
    NBB25 = 2508;   # bunches@25ns
    RECO_MODULES_TIME_HISTO_OLD = '/DQMData/Run 1/DQM/Run summary/TimerService/Paths/reconstruction_step_module_total'
    RECO_TIME_HISTO_OLD = '/DQMData/Run 1/DQM/Run summary/TimerService/Paths/reconstruction_step_total'
    RECO_MODULES_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/process RECO/Paths/reconstruction_step_module_total'
    RECO_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/process RECO/Paths/reconstruction_step_total'
    EVENT_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/event'
#    TRACKS_HISTO = '/DQMData/Run 1/TrackingTime/Run summary/Algo/Algo_For_HP'
    def __init__(self, file, release, print_labels, oldPath=0, verbose=0):
        self.oldPath_ = oldPath
        self.verbose_ = verbose
        self.release_ = release
        self.print_labels_ = print_labels
        self.file_ = file
        self.ROOT_file_ = None
        self.processed_events_ = 0. # Fetched as entries in EVENT_TIME_HISTO
        self.event_time_ = 0. # in ms
        self.event_time_rms_ = 0. # in ms
        self.reco_total_time_ = 0. # in ms
        self.reco_total_time_rms_ = 0. # in ms
        self.iterative_total_time_ = 0. # in ms
        self.iterative_time_ = {} # in ms
        self.pileup_ = 0.
        self.bunch_spacing_ = 0.
        self.luminosity_ = 0.
        self.cluster_charge_cut_ = 0.
        if self.oldPath_:
            self.RECO_MODULES_TIME_HISTO = self.RECO_MODULES_TIME_HISTO_OLD
            self.RECO_TIME_HISTO = self.RECO_TIME_HISTO_OLD
        # Now call decoding functions`
        self.fillInfoFromFile_()
        self.fillTimeInfoFromFile_()


    def fillInfoFromFile_(self):
        m = re.match(PUBX, self.file_)
        if m:
            pileup_to_luminosity_factor = 1. / Measure.MINBIAS_XS * Measure.FREV / Measure.SCALE
            self.pileup_ = float(m.group(1))
            self.bunch_spacing_ = float(m.group(2))
            if self.bunch_spacing_ == 50:
                self.luminosity_ = Measure.NBB50 * self.pileup_ * pileup_to_luminosity_factor
            elif self.bunch_spacing_ == 25:
                self.luminosity_ = Measure.NBB25 * self.pileup_ * pileup_to_luminosity_factor
            else:
                print "Error, unsopported bunch spacing %f . Quitting.\n" % self.bunch_spacing_
        else:
            print "Error decoding info from %s. Quitting.\n" % self.file_
            sys.exit(ERR_BAD_FILE)
        m = re.match(CLUSTER_CHARGE, self.file_)
        if m:
            self.cluster_charge_cut_ = 1.

    def fillTimeInfoFromFile_(self):
        self.ROOT_file_ = TFile.Open(self.file_)
        h = self.ROOT_file_.Get(self.RECO_TIME_HISTO)
        self.reco_total_time_ = h.GetMean()
        self.reco_total_time_rms_ = h.GetRMS()
        h = self.ROOT_file_.Get(self.EVENT_TIME_HISTO)
        self.processed_events_ = h.GetEntries()
        self.event_time_ = h.GetMean()
        self.event_time_rms_ = h.GetRMS()
        h = self.ROOT_file_.Get(self.RECO_MODULES_TIME_HISTO)
        steps = sorted(iterLabels.keys())
        for step in steps:
            self.iterative_time_[step] = 0.
            for l in iterLabels[step]:
                if self.verbose_ > 0 :
                    print "Adding step %s for iter%s" % (l, step)
                self.iterative_total_time_ += h.GetBinContent(h.GetXaxis().FindBin(l))
                self.iterative_time_[step] += h.GetBinContent(h.GetXaxis().FindBin(l))
            if self.verbose_ > 0:
                print "iter%s Tot[s]: %f " % (step,
                                              self.iterative_time_[step] / self.processed_events_ / 1000.)
    def dump(self):
        print "Displaying info from %s" % self.file_
        print "Processed Events: %d" % self.processed_events_
        print "EventTime[s]: %f RMS: %f" % (self.event_time_/1000.,
                                            self.event_time_rms_/1000.)
        print "RecoTime[s]: %f RMS: %f" % (self.reco_total_time_/1000.,
                                           self.reco_total_time_rms_/1000.)
        print "IterativeTime[s]: %f" % (self.iterative_total_time_/self.processed_events_/1000.)
        print "PileUP: %d, Lumi: %f" % (self.pileup_, self.luminosity_)

def totalEventTime_vs_PU(measurements,
                         release_label,
                         fillStyle,
                         NoFill):
    baseColor = [kAzure, kOrange, kSpring, kRed]
    if len(measurements) > len(baseColor):
        print "Warning, too many files to overlay"
        return
    (c, g) = makeFrame("RecoTimePU",
                       "Reco Time - %s" % release_label,
                       "PileUp",
                       "Time/Event [s]",
                       20,
                       0,
                       150,
                       200)
    keep_alive = []
    legend = 0
    pu_labels = None
    col_idx = 0
    for measurement in measurements:
        color = baseColor[col_idx]
        col_idx += 1
#         (g0, legend, t) = makeGenericTimePlot('TotalEventTime_vs_PU',
#                                               measurement,
#                                               "%d ns - FullEvent %s" % (measurement[0].bunch_spacing_,
#                                                                         measurement[0].release_),
#                                               color+5,
#                                               23,
#                                               1,
#                                               NoFill,
#                                               legend if legend else None,
#                                               'lp',
#                                               (False, 0, 0))
#        keep_alive.append(g0)
        (g1, legend, pu_labels) = makeGenericTimePlot('TotalRecoTime_vs_PU',
                                                      measurement,
                                                      "%d ns - Reco Only %s" % (measurement[0].bunch_spacing_,
                                                                                measurement[0].release_),
                                                      color,
                                                      21,
                                                      1,
                                                      fillStyle[0],
                                                      legend if legend else None,
                                                      'f',
                                                      (1., 12),
                                                      pu_labels if pu_labels else None)
        keep_alive.append(g1)
        (g2, legend, t) = makeGenericTimePlot('TotalIterativeTime_vs_PU',
                                              measurement,
                                              "%d ns - IterativeTime Only %s" % (measurement[0].bunch_spacing_,
                                                                                 measurement[0].release_),
                                              color-5,
                                              20,
                                              1,
                                              NoFill,
                                              legend,
                                              'lp',
                                              (1., 12),
                                              None)
        keep_alive.append(g2)
#         for t in pu_labels:
#             t.Draw()
        c.RedrawAxis()
        c.SaveAs("RecoTimePU_%d_BX_%s_Nehalem.png" % (measurement[0].bunch_spacing_,
                                                      release_label))

def totalEventTime_vs_LUMI(measurements,
                           release_label,
                           fillStyle,
                           NoFill):
    baseColor = [kAzure, kOrange, kSpring, kRed]
    if len(measurements) > len(baseColor):
        print "Warning, too many files to overlay"
        return
    (cl, gl) = makeFrame("RecoTimeLUMI",
                         "Reco Time - %s" % release_label,
                         "Luminosity [10^{34} cm^{-2} s^{-1}]",
                         "Time/Event [s]",
                         0.5,
                         0,
                         5.5,
                         380)
    keep_alive = []
    legendl = 0
    pu_labels = None
    col_idx = 0
    for measurement in measurements:
        color = baseColor[col_idx]
        col_idx += 1
#         (g7a, legendl, p) = makeGenericTimePlot('TotalEventTime_vs_LUMI',
#                                                 measurements,
#                                                 "%d ns - Full Event" % measurements[0].bunch_spacing_,
#                                                 kAzure+5,
#                                                 23,
#                                                 1,
#                                                 NoFill,
#                                                 None,
#                                                 'lp',
#                                                 (True, 1., 12))
        (g7, legendl, pu_labels) = makeGenericTimePlot('TotalRecoTime_vs_LUMI',
                                                       measurement,
                                                       "%d ns - Reco Only %s" % (measurement[0].bunch_spacing_,
                                                                                 measurement[0].release_),
                                                       color,
                                                       21,
                                                       1,
                                                       fillStyle[0],
                                                       legendl if legendl else None,
                                                       'f',
                                                       (1., 12),
                                                       pu_labels if pu_labels else None)
        keep_alive.append(g7)
        (g8, legendl, p) = makeGenericTimePlot('TotalIterativeTime_vs_LUMI',
                                               measurement,
                                               "%d ns - IterativeTime %s" % (measurement[0].bunch_spacing_,
                                                                             measurement[0].release_),
                                               color-5,
                                               20,
                                               1,
                                               1,
                                               legendl if legendl else None,
                                               'lp',
                                               (0., 0),
                                               None)
        keep_alive.append(g8)
        for t in pu_labels:
            t = setTextProperties(t)
            t.Draw()
        cl.RedrawAxis()
        cl.SaveAs("RecoTimeLUMI_%d_BX_%s_Nehalem.png" % (measurement[0].bunch_spacing_,
                                                         release_label))
def iterativeTime(measurements,
                  release_label,
                  fillStyle,
                  NoFill):
    (ci, gi) = makeFrame("IterativeTimePU",
                         "Iterative Time - %s" % release_label,
                         "PileUP",
                         "Time/Event [s]",
                         10,
                         0,
                         70,
                         20)
    (g13, legendi, pi) = makeGenericTimePlot('IterativeTime_vs_PU',
                                             measurements,
                                             "%d ns" % measurements[0].bunch_spacing_,
                                             kAzure,
                                             21,
                                             1,
                                             fillStyle[0],
                                             None,
                                             'lp',
                                             (False, 0., 0.))
    ci.RedrawAxis()
    ci.SaveAs("IterativeTimePU_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
                                                        release_label))

    # Iterative Steps Details LUMI
    (cil, gil) = makeFrame("IterativeTimeLUMI",
                           "Iterative Time - %s" % release_label,
                           "Luminosity [10^{34} cm^{-2} s^{-1}]",
                           "Time/Event [s]",
                           0.5,
                           0,
                           3.0,
                           50)
    (g17, legendil, pil) = makeGenericTimePlot('IterativeTime_vs_LUMI',
                                               measurements,
                                               "%d ns" % measurements[0].bunch_spacing_,
                                               kAzure,
                                               21,
                                               1,
                                               fillStyle[0],
                                               None,
                                               'lp',
                                               (True, 1.2, 0.))
    cil.RedrawAxis()
    cil.SaveAs("IterativeTimeLUMI_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
                                                           release_label))

def setTextProperties(obj, label=False, title=False):
    textFont = 42
    textSize = 0.027
    titleOffset = 1.25
    labelOffset = 0.002
    if not label and not title:
        obj.SetTextFont(textFont)
        obj.SetTextSize(textSize)
    if label:
        obj.SetLabelOffset(labelOffset)
        obj.SetLabelFont(textFont)
        obj.SetLabelSize(textSize)
    if title:
        gStyle.SetTitleX(0.5)
        gStyle.SetTitleAlign(23)
        obj.SetTitleFont(textFont)
        obj.SetTitleSize(textSize)
        obj.SetTitleOffset(titleOffset)
    return obj

def TDRStyle():
#    gSystem.AddDynamicPath("/afs/cern.ch/user/r/rovere/")
    gSystem.Load("tdrStyle_C")
    setTDRStyle()

def main():
    TDRStyle()
    if not checkEnvs():
        pass
    measurements_25bx = []
    measurements_50bx = []
    measurements_25bx_710pre8 = []
    measurements_50bx_710pre8 = []
    measurements_25bx_53X = []
    measurements_50bx_53X = []

    # Measure accepts the following parameters, in the correct order:
    # 1, full pathname of the DQM file containing the timing information
    # 2. the base release in which the measurements have been performed
    # 3. a boolean specifying if the PU labels have to appear on the _vs_LUMI plots
    # 4. a boolean specifying if the internal directory structure of the FastTimerService is old(1) or new(0)
    # 5. the inevitable verbose flag.
    eosdir_710pre7 = 'root://eoscms.cern.ch//store/group/phys_tracking/samples_710pre7/RECO'
    eosdir_710pre8 = 'root://eoscms.cern.ch//store/group/phys_tracking/samples_710pre8/RECO'
    measurements_50bx.append(Measure('%s/AVE_PU25_BX50/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre7__PU25_BX50.root' % eosdir_710pre7,
                                     '710pre7', 1, 0, 0))
    measurements_50bx.append(Measure('%s/AVE_PU50_BX50/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre7__PU50_BX50.root' % eosdir_710pre7,
                                     '710pre7', 1, 0, 0))
    measurements_50bx_710pre8.append(Measure('%s/AVE_PU25_BX50/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre8__PU25_BX50.root' % eosdir_710pre8,
                                             '710pre8', 1, 0, 0))
    measurements_50bx_710pre8.append(Measure('%s/AVE_PU50_BX50/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre8__PU50_BX50.root' % eosdir_710pre8,
                                             '710pre8', 1, 0, 0))
#    measurements_50bx_53X.append(Measure('/afs/cern.ch/user/c/cerati/public/productions/AVE_25_BX_50ns/DQM_V0001_R000000001__MyTiming__Release53X__PU25_BX50.root', '53X', 1, 1, 0))
#    measurements_50bx_53X.append(Measure('/afs/cern.ch/user/c/cerati/public/productions/AVE_50_BX_50ns/DQM_V0001_R000000001__MyTiming__Release53X__PU50_BX50.root', '53X', 1, 1, 0))
    measurements_25bx.append(Measure('%s/AVE_PU25_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre7__PU25_BX25.root' % eosdir_710pre7,
                                     '710pre7', 1, 0, 0))
    measurements_25bx.append(Measure('%s/AVE_PU40_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre7__PU40_BX25.root' % eosdir_710pre7,
                                     '710pre7', 1, 0, 0))
    measurements_25bx.append(Measure('%s/AVE_PU70_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre7__PU70_BX25.root' % eosdir_710pre7,
                                     '710pre7', 1, 0, 0))
    measurements_25bx_710pre8.append(Measure('%s/AVE_PU25_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre8__PU25_BX25.root' % eosdir_710pre8,
                                             '710pre8', 1, 0, 0))
    measurements_25bx_710pre8.append(Measure('%s/AVE_PU40_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre8__PU40_BX25.root' % eosdir_710pre8,
                                             '710pre8', 1, 0, 0))
    measurements_25bx_710pre8.append(Measure('%s/AVE_PU70_BX25/TTbar/DQM_V0001_R000000001__MyTiming__Release710pre8__PU70_BX25.root' % eosdir_710pre8,
                                             '710pre8', 1, 0, 0))
#    measurements_25bx_53X.append(Measure('/afs/cern.ch/user/c/cerati/public/productions/AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU25_BX25.root' , '53X', 1, 1, 0))
#    measurements_25bx_53X.append(Measure('/afs/cern.ch/user/c/cerati/public/productions/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU40_BX25.root' , '53X', 1, 1, 0))
#    measurements_25bx_53X.append(Measure('/afs/cern.ch/user/c/cerati/public/productions/AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU70_BX25.root' , '53X', 1, 1, 0))
#    Explanation of the fill style algo:
#    FillStyle = 3ijk, i(1,9)=space[0.5, 6]mm, j(0,9)=angle[0,90], k(0,9)=angle[90,180]
    fillStyle = [
        3245,
        3254,
        3256,
        3017,
        3018,
        3020,
        3305,
        3325,
        3353,
        3345,
        3354
        ]
    NoFill = 1

    # 50 ns
#    totalEventTime_vs_PU([measurements_50bx, measurements_50bx_53X], "710pre7", fillStyle, NoFill)
#    totalEventTime_vs_LUMI([measurements_50bx, measurements_50bx_53X], "710pre7", fillStyle, NoFill)
#    iterativeTime(measurements_50bx, "710pre7", fillStyle, NoFill)

    # 25 ns
    totalEventTime_vs_PU([measurements_25bx, measurements_25bx_710pre8, measurements_50bx, measurements_50bx_710pre8], "710pre7", fillStyle, NoFill)
    totalEventTime_vs_LUMI([measurements_25bx, measurements_25bx_710pre8, measurements_50bx, measurements_50bx_710pre8], "710pre7", fillStyle, NoFill)
    iterativeTime(measurements_25bx, "710pre7", fillStyle, NoFill)

    for m in measurements_50bx:
        m.dump()
    for m in measurements_25bx:
        m.dump()

    waitKey()

if __name__ == "__main__":
    from ROOT import *
    main()
