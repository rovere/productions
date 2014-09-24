#!/usr/bin/env python

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
iterLabels['7_jetCore'] = ['iter0TrackRefsForJets',
                   'caloTowerForTrk',
                   'ak4CaloJetsForTrk',
                   'jetsForCoreTracking',
                   'firstStepPrimaryVertices',
                   'firstStepGoodPrimaryVertices',
                   'jetCoreRegionalStepSeedLayers',
                   'jetCoreRegionalStepSeeds',
                   'jetCoreRegionalStepTrackCandidates',
                   'jetCoreRegionalStepTracks',
                   'jetCoreRegionalStepSelector']
# iterLabels['earlyGeneralTracks'] = ['earlyGeneralTracks']
# iterLabels['muonSeededStep'] = ['earlyMuons',
#                                 'muonSeededSeedsInOut',
#                                 'muonSeededSeedsInOut',
#                                 'muonSeededTracksInOut',
#                                 'muonSeededSeedsOutIn',
#                                 'muonSeededTrackCandidatesOutIn',
#                                 'muonSeededTracksOutIn',
#                                 'muonSeededTracksInOutSelector',
#                                 'muonSeededTracksOutInSelector']
# iterLabels['generalTracksSequence'] = ['duplicateTrackCandidates',
#                                        'mergedDuplicateTracks',
#                                        'duplicateTrackSelector',
#                                        'generalTracks']
# iterLabels['ConvStep'] = ['convClusters',
#                           'convLayerPairs',
#                           'photonConvTrajSeedFromSingleLeg',
#                           'convTrackCandidates',
#                           'convStepTracks',
#                           'convStepSelector',
#                           'conversionStepTracks']
# iterLabels['electronSeedsSeq'] = ['initialStepSeedClusterMask',
#                                   'pixelPairStepSeedClusterMask',
#                                   'mixedTripletStepSeedClusterMask',
#                                   'pixelLessStepSeedClusterMask',
#                                   'tripletElectronSeedLayers',
#                                   'tripletElectronSeeds',
#                                   'tripletElectronClusterMask',
#                                   'pixelPairElectronSeedLayers',
#                                   'pixelPairElectronSeeds',
#                                   'stripPairElectronSeedLayers',
#                                   'stripPairElectronSeeds',
#                                   'newCombinedSeeds']
# iterLabels['doAlldEdXEstimators'] = ['dedxTruncated40',
#                                      'dedxHarmonic2',
#                                      'dedxDiscrimASmi']

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
    #g.SetTitle(title)
    g.SetTitle('')
    g.GetXaxis().SetTitle(xtitle)
    g.GetYaxis().SetTitle(ytitle)
    setTextProperties(g.GetXaxis(), title=True)
    setTextProperties(g.GetYaxis(), title=True)
    setTextProperties(g.GetXaxis(), label=True)
    setTextProperties(g.GetYaxis(), label=True)
    g.Draw("AP")
    c.Update()
    return c, g  # keep it alive....

def makeTimePlotVsStep(kind,
                       measurements):
    steps = sorted(iterLabels.keys())
    histos = []
    for i in range(0, len(measurements)):
        h=TH1F(measurements[i].release_,measurements[i].release_,9,0,9)
        h.SetLineWidth(2)
        if i == 0: 
            h.SetLineColor(kBlack)
            h.SetMarkerColor(kBlack)
            h.SetMarkerStyle(21)
        elif i == 1: 
            h.SetLineColor(kRed)
            h.SetMarkerColor(kRed)
            h.SetMarkerStyle(22)
        elif i == 2: 
            h.SetLineColor(kAzure)
            h.SetMarkerColor(kAzure)
            h.SetMarkerStyle(23)
        print len(measurements[i].iterative_time_)
        print measurements[i].iterative_time_
        istep = 0
        for step in steps:
            print step
            print measurements[i].iterative_time_[step]
            h.SetBinContent(istep+1,measurements[i].iterative_time_[step]/ measurements[i].processed_events_ /1000./6.05)
            istep+=1
        h.SetBinContent(istep+1,measurements[i].iterative_total_time_/ measurements[i].processed_events_ /1000./6.05)
        histos.append(h)
    return histos

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
            y.append(measurements[i].reco_total_time_/1000./6.05)
            ey.append(measurements[i].reco_total_time_rms_/1000./6.05)
    elif kind == 'TotalIterativeTime_vs_PU':
        for i in range(0, len(measurements)):
            x.append(measurements[i].pileup_)
            ex.append(0.)
            y.append(measurements[i].iterative_total_time_/1000./measurements[i].processed_events_ / 6.05) # 1000 for ms
            ey.append(0.)
    elif kind == 'TotalEventTime_vs_PU':
        for i in range(0, len(measurements)):
            x.append(measurements[i].pileup_)
            ex.append(0.)
            y.append(measurements[i].event_time_/1000./6.05)
#            ey.append(measurements[i].event_time_rms_/1000.)
            ey.append(0.)
    elif kind == 'TotalRecoTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].reco_total_time_/1000./6.05)
            ey.append(measurements[i].reco_total_time_rms_/1000./6.05)
    elif kind == 'TotalIterativeTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].iterative_total_time_/1000./measurements[i].processed_events_ / 6.05) # 1000 for ms
            ey.append(0.)
    elif kind == 'TotalEventTime_vs_LUMI':
        for i in range(0, len(measurements)):
            x.append(measurements[i].luminosity_)
            ex.append(0.)
            y.append(measurements[i].event_time_/1000./6.05) # 1000 for ms
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
                iy[counter].append(measurements[i].iterative_time_[step]/1000./measurements[i].processed_events_/6.05) # 1000 for ms
                counter += 1
    if kind != 'IterativeTime_vs_PU' and kind != 'IterativeTime_vs_LUMI':
        if not legend:
            if kind == 'TotalRecoTime_vs_LUMI': legend = TLegend(0.15, 0.78, 0.89, 0.88)
            else: legend = TLegend(0.15, 0.68, 0.55, 0.85)
            legend.SetFillColor(0)
            legend.SetBorderSize(0)
            #legend.SetHeader("PileUp Scenarios")
            if kind == 'TotalRecoTime_vs_LUMI': legend.SetNColumns(2)
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
        gr[-1].Draw("CPX")#CP3
        for l in range(0, len(measurements)):
            if measurements[l].print_labels_:
                if int(measurements[l].pileup_)==140: pu_text.append(TText(x[l]-0.2, y[l]*print_labels_for_points[0] + print_labels_for_points[1]/6.05, "PU%d" % int(measurements[l].pileup_)))
                if int(measurements[l].pileup_)==40: pu_text.append(TText(x[l]-0.2, y[l]*3*print_labels_for_points[0] + print_labels_for_points[1]/6.05, "PU%d" % int(measurements[l].pileup_)))
                else: pu_text.append(TText(x[l]-0.4, y[l]*2.5*print_labels_for_points[0] + print_labels_for_points[1]/6.05, "PU%d" % int(measurements[l].pileup_)))
                setTextProperties(pu_text[-1])
#                pu_text[-1].SetTextFont(23)
#                pu_text[-1].SetTextSize(20)
#                pu_text[-1].SetTextAlign(22)
        legend.AddEntry(gr[-1], label, legend_kind)
        setTextProperties(legend)
        legend.Draw()
    elif kind == 'IterativeTime_vs_PU' or kind == 'IterativeTime_vs_LUMI':
        if not legend:
            legend = TLegend(0.15, 0.5, 0.55, 0.85)
            legend.SetFillColor(0)
            legend.SetBorderSize(0)
            #legend.SetHeader("PileUp Scenarios")
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
                pu_text.append(TText(x[l]-0.2, iy[i][l]*print_labels_for_points[0] + print_labels_for_points[1]/6.05, "PU%d" % int(measurements[l].pileup_)))
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
        self.ROOT_file_ = TFile(self.file_)
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

def drawCMSLabel():
    labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
    labelcms.SetTextAlign(12);
    labelcms.SetTextSize(0.033);
    labelcms.SetFillColor(kWhite);
    labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
    labelcms.SetBorderSize(0);
    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    labelcms.Draw();


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
                       "Time/Event [a.u.]",
                       20,
                       0,
                       70+80*(len(measurements[0])-3),#150,
                       (100+350*(len(measurements[0])-3))/6.05)#450
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
        if 'zoom' not in release_label:
            (g1, legend, pu_labels) = makeGenericTimePlot('TotalRecoTime_vs_PU',
                                                          measurement,
                                                          "Full Reco %s" % measurement[0].release_,
                                                          color,
                                                          21,
                                                          1,
                                                          fillStyle[0],
                                                          legend if legend else None,
                                                          'lp',#'f',
                                                          (1., 12),
                                                          pu_labels if pu_labels else None)
            keep_alive.append(g1)
        (g2, legend, t) = makeGenericTimePlot('TotalIterativeTime_vs_PU',
                                              measurement,
                                              "Track Reco %s" % measurement[0].release_,
                                              color-5,
                                              20,
                                              1,
                                              NoFill,
                                              legend,
                                              'lp',
                                              (0., 0),
                                              None)
        keep_alive.append(g2)
#         for t in pu_labels:
#             t.Draw()
        c.RedrawAxis()
        labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
        labelcms.SetTextAlign(12);
        labelcms.SetTextSize(0.033);
        labelcms.SetFillColor(kWhite);
        labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
        labelcms.SetBorderSize(0);
        labelcms.SetTextFont(42);
        labelcms.SetLineWidth(2);
        labelcms.Draw();
        c.Update()
        c.SaveAs("RecoTimePU_%d_BX_%s.png" % (measurement[0].bunch_spacing_,
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
                         "Time/Event [a.u.]",
                         0.5,
                         0,
                         2.5+3.0*(len(measurements[0])-3),
                         (100+280*(len(measurements[0])-3))/6.05)#450
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
        if 'zoom' not in release_label:
            (g7, legendl, pu_labels) = makeGenericTimePlot('TotalRecoTime_vs_LUMI',
                                                           measurement,
                                                           "Full Reco %s" % measurement[0].release_,
                                                           color,
                                                           21,
                                                           1,
                                                           fillStyle[0],
                                                           legendl if legendl else None,
                                                           'lp',#'f',
                                                           (1., 12),
                                                           pu_labels if pu_labels else None)

            keep_alive.append(g7)
            (g8, legendl, p) = makeGenericTimePlot('TotalIterativeTime_vs_LUMI',
                                                   measurement,
                                                   "Track Reco %s" % measurement[0].release_,
                                                   color-5,
                                                   20,
                                                   1,
                                                   1,
                                                   legendl if legendl else None,
                                                   'lp',
                                                   (0., 0),
                                                   None)
            keep_alive.append(g8)
        else:
            (g8, legendl, pu_labels) = makeGenericTimePlot('TotalIterativeTime_vs_LUMI',
                                                   measurement,
                                                   "Track Reco %s" % measurement[0].release_,
                                                   color-5,
                                                   20,
                                                   1,
                                                   1,
                                                   legendl if legendl else None,
                                                   'lp',
                                                   (1., 1.),#(0., 0),
                                                   pu_labels if pu_labels else None)
            keep_alive.append(g8)

        if pu_labels:
            for t in pu_labels:
                t = setTextProperties(t)
                t.Draw()
        cl.RedrawAxis()
        labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
        labelcms.SetTextAlign(12);
        labelcms.SetTextSize(0.033);
        labelcms.SetFillColor(kWhite);
        labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
        labelcms.SetBorderSize(0);
        labelcms.SetTextFont(42);
        labelcms.SetLineWidth(2);
        labelcms.Draw();
        cl.Update()
        cl.SaveAs("RecoTimeLUMI_%d_BX_%s.png" % (measurement[0].bunch_spacing_,
                                                         release_label))
def iterativeTime(measurements,
                  release_label,
                  fillStyle,
                  NoFill):
    (ci, gi) = makeFrame("IterativeTimePU",
                         "Iterative Time - %s" % release_label,
                         "PileUP",
                         "Time/Event [a.u.]",
                         10,
                         0,
                         140,
                         60/6.05)
    (g13, legendi, pi) = makeGenericTimePlot('IterativeTime_vs_PU',
                                             measurements,
                                             "",
                                             kAzure,
                                             21,
                                             1,
                                             fillStyle[0],
                                             None,
                                             'lp',
                                             (False, 0., 0.))
    ci.RedrawAxis()
    labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
    labelcms.SetTextAlign(12);
    labelcms.SetTextSize(0.033);
    labelcms.SetFillColor(kWhite);
    labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
    labelcms.SetBorderSize(0);
    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    labelcms.Draw();
    ci.Update()
    ci.SaveAs("IterativeTimePU_%d_BX_%s.png" % (measurements[0].bunch_spacing_,
                                                        release_label))

    # Iterative Steps Details LUMI
    (cil, gil) = makeFrame("IterativeTimeLUMI",
                           "Iterative Time - %s" % release_label,
                           "Luminosity [10^{34} cm^{-2} s^{-1}]",
                           "Time/Event [s]",
                           0.5,
                           0,
                           5.0,
                           60/6.05)
    (g17, legendil, pil) = makeGenericTimePlot('IterativeTime_vs_LUMI',
                                               measurements,
                                               "",
                                               kAzure,
                                               21,
                                               1,
                                               fillStyle[0],
                                               None,
                                               'lp',
                                               (True, 1.2, 0.))
    cil.RedrawAxis()
    labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
    labelcms.SetTextAlign(12);
    labelcms.SetTextSize(0.033);
    labelcms.SetFillColor(kWhite);
    labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
    labelcms.SetBorderSize(0);
    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    labelcms.Draw();
    cil.Update()
    cil.SaveAs("IterativeTimeLUMI_%d_BX_%s.png" % (measurements[0].bunch_spacing_,
                                                           release_label))

def iterativeTimeCompare(measurements,
                         release_label
                         #fillStyle,
                         #NoFill
                         ):
    (ci, gi) = makeFrame("IterativeTimePU",
                         "Iterative Time - %s" % release_label,
                         "IterationStep",
                         "Time/Event [a.u.]",
                         0,
                         0,
                         8.2,
                         20/6.05)
    (histos) = makeTimePlotVsStep('Time_vs_Step',measurements)
    ci.RedrawAxis()
    legend = TLegend(0.15,0.68,0.80,0.85)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetNColumns(1)
    histos[0].GetXaxis().SetBinLabel(1,'initial')
    histos[0].GetXaxis().SetBinLabel(2,'lowPtTriplet')
    histos[0].GetXaxis().SetBinLabel(3,'pixelPair')
    histos[0].GetXaxis().SetBinLabel(4,'detachedTriplet')
    histos[0].GetXaxis().SetBinLabel(5,'mixelTriplet')
    histos[0].GetXaxis().SetBinLabel(6,'pixelLess')
    histos[0].GetXaxis().SetBinLabel(7,'tobTec')
    histos[0].GetXaxis().SetBinLabel(8,'jetCore')
    histos[0].GetXaxis().SetBinLabel(9,'total')
    histos[0].GetYaxis().SetRangeUser(0,20/6.05)
    histos[0].GetXaxis().SetTitle('IterationStep')
    histos[0].GetYaxis().SetTitle('Time/Event [a.u.]')
    histos[0].GetXaxis().LabelsOption('v')
    histos[0].GetXaxis().SetLabelSize(0.04)
    histos[0].GetYaxis().SetLabelSize(0.04)
    histos[0].GetXaxis().SetTitleSize(0.05)
    histos[0].GetYaxis().SetTitleSize(0.05)
    histos[0].GetXaxis().SetTitleOffset(2.0)
    histos[0].GetYaxis().SetTitleOffset(1.2)
    histos[0].Draw()
    for h in histos: 
        h.Draw('SAME,PH')
        legend.AddEntry(h,h.GetTitle(),'LP')
    legend.Draw()
    histos[0].SetTitle('')
    labelcms  = TPaveText(0.14,0.88,0.9,0.93,"NDCBR");
    labelcms.SetTextAlign(12);
    labelcms.SetTextSize(0.033);
    labelcms.SetFillColor(kWhite);
    labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + <PU>=40, BX=25ns");
    labelcms.SetBorderSize(0);
    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    labelcms.Draw();
    gPad.SetBottomMargin(0.2);
    ci.Update()
    ci.SaveAs("IterativeTimeStep_%d_BX_%s.png" % (measurements[0].bunch_spacing_,
                                                        release_label))

def setTextProperties(obj, label=False, title=False):
    textFont = 42
    textSize = 0.04
    titleOffset = 1.25
    labelOffset = 0.002
    #histos[0].GetXaxis().SetLabelSize(0.04)
    #histos[0].GetYaxis().SetLabelSize(0.04)
    #histos[0].GetXaxis().SetTitleSize(0.05)
    #histos[0].GetYaxis().SetTitleSize(0.05)
    #histos[0].GetXaxis().SetTitleOffset(2.0)
    #histos[0].GetYaxis().SetTitleOffset(1.2)
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
    gROOT.ProcessLine(".L tdrStyle.C");
    setTDRStyle();
    gStyle.SetOptStat(0)
    #gSystem.AddDynamicPath("./")
    #gSystem.Load("tdrStyle_C")
    #setTDRStyle()
    pass

def main():
    TDRStyle()
    if not checkEnvs():
        pass
    measurements_53X_25bx = []
    measurements_53X_50bx = []
    measurements_720p4_25bx = []
    measurements_720p4_50bx = []
    measurements_720p4_25bx_NoDynInef = []
    measurements_720p4_50bx_NoDynInef = []
    measurements_720p4_25bx_NoDynInefMax70 = []
    measurements_720p4_25bx_NoDynInef_NoCCC = []

    # Measure accepts the following parameters, in the correct order:
    # 1, full pathname of the DQM file containing the timing information
    # 2. the base release in which the measurements have been performed
    # 3. a boolean specifying if the PU labels have to appear on the _vs_LUMI plots
    # 4. a boolean specifying if the internal directory structure of the FastTimerService is old(1) or new(0)
    # 5. the inevitable verbose flag.

    measurements_53X_50bx.append(Measure('CMSSW53X/productions/AVE_25_BX_50ns/DQM_V0001_R000000001__MyTiming__Release53X__PU25_BX50.root', 'Run1', 0, 1, 0))
    measurements_53X_50bx.append(Measure('CMSSW53X/productions/AVE_50_BX_50ns/DQM_V0001_R000000001__MyTiming__Release53X__PU50_BX50.root', 'Run1', 0, 1, 0))
    measurements_53X_25bx.append(Measure('CMSSW53X/productions/AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU25_BX25.root', 'Run1', 0, 1, 0))
    measurements_53X_25bx.append(Measure('CMSSW53X/productions/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU40_BX25.root', 'Run1', 0, 1, 0))
    measurements_53X_25bx.append(Measure('CMSSW53X/productions/AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release53X__PU70_BX25.root', 'Run1', 0, 1, 0))

    measurements_720p4_50bx.append(Measure('CMSSW720pre4/productions/AVE_25_BX_50ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU25_BX50.root', '720p4 DynInef', 1, 0, 0))
    measurements_720p4_50bx.append(Measure('CMSSW720pre4/productions/AVE_50_BX_50ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU50_BX50.root', '720p4 DynInef', 1, 0, 0))
    measurements_720p4_25bx.append(Measure('CMSSW720pre4/productions/AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU25_BX25.root', '720p4 DynInef', 1, 0, 0))
    measurements_720p4_25bx.append(Measure('CMSSW720pre4/productions/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU40_BX25.root', '720p4 DynInef', 1, 0, 0))
    measurements_720p4_25bx.append(Measure('CMSSW720pre4/productions/AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU70_BX25.root', '720p4 DynInef', 1, 0, 0))
    measurements_720p4_25bx.append(Measure('CMSSW720pre4/productions/AVE_140_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU140_BX25.root', '720p4 DynInef', 1, 0, 0))

    measurements_720p4_50bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_25_BX_50ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU25_BX50.root', 'Current', 1, 0, 0))
    measurements_720p4_50bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_50_BX_50ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU50_BX50.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU25_BX25.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU40_BX25.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU70_BX25.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInef.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_140_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU140_BX25.root', 'Current', 1, 0, 0))

    measurements_720p4_25bx_NoDynInefMax70.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU25_BX25.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInefMax70.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU40_BX25.root', 'Current', 1, 0, 0))
    measurements_720p4_25bx_NoDynInefMax70.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU70_BX25.root', 'Current', 1, 0, 0))

    measurements_720p4_25bx_NoDynInef_NoCCC.append(Measure('DQM_V0001_R000000001__MyTiming__Release720pre4-NoDynInef-NoCCC-NoTripl__PU40_BX25.root','Pair Seeding', 0, 0, 1))
    measurements_720p4_25bx_NoDynInef_NoCCC.append(Measure('DQM_V0001_R000000001__MyTiming__Release720pre4-NoDynInef-NoCCC__PU40_BX25.root','Triplet Seeding', 0, 0, 1))
    measurements_720p4_25bx_NoDynInef_NoCCC.append(Measure('CMSSW720pre4/productions-no-dyn-inef/AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release720pre4__PU40_BX25.root', 'Triplets + Cluster Charge Cut', 0, 0, 1))

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

    # # 50 ns
    # totalEventTime_vs_PU([measurements_720p4_50bx, measurements_720p4_50bx_NoDynInef], "720p4", fillStyle, NoFill)
    # totalEventTime_vs_LUMI([measurements_720p4_50bx, measurements_720p4_50bx_NoDynInef], "720p4", fillStyle, NoFill)
    # iterativeTime(measurements_720p4_50bx, "720p4", fillStyle, NoFill)
    # iterativeTime(measurements_720p4_50bx_NoDynInef, "720p4_NoDynInef", fillStyle, NoFill)

    # # 25 ns
    # totalEventTime_vs_PU([measurements_720p4_25bx, measurements_720p4_25bx_NoDynInef], "720p4", fillStyle, NoFill)
    # totalEventTime_vs_LUMI([measurements_720p4_25bx, measurements_720p4_25bx_NoDynInef], "720p4", fillStyle, NoFill)
    # iterativeTime(measurements_720p4_25bx, "720p4", fillStyle, NoFill)
    iterativeTime(measurements_720p4_25bx_NoDynInef, "720p4_NoDynInef", fillStyle, NoFill)
    # #iterativeTime(measurements_720p4_25bx_NoDynInefMax70, "720p4_NoDynInefMax70", fillStyle, NoFill)

    # totalEventTime_vs_PU([measurements_720p4_25bx, measurements_720p4_50bx], "720p4", fillStyle, NoFill)
    # totalEventTime_vs_LUMI([measurements_720p4_25bx, measurements_720p4_50bx], "720p4", fillStyle, NoFill)
    totalEventTime_vs_PU([measurements_720p4_25bx_NoDynInef, measurements_53X_25bx], "25ns", fillStyle, NoFill)
    totalEventTime_vs_LUMI([measurements_720p4_25bx_NoDynInef, measurements_53X_25bx], "25ns", fillStyle, NoFill)

    totalEventTime_vs_PU([measurements_720p4_25bx_NoDynInefMax70, measurements_53X_25bx], "25ns_zoom", fillStyle, NoFill)
    totalEventTime_vs_LUMI([measurements_720p4_25bx_NoDynInefMax70, measurements_53X_25bx], "25ns_zoom", fillStyle, NoFill)

    # totalEventTime_vs_PU([measurements_720p4_50bx_NoDynInef, measurements_53X_50bx], "50ns", fillStyle, NoFill)
    # totalEventTime_vs_LUMI([measurements_720p4_50bx_NoDynInef, measurements_53X_50bx], "50ns", fillStyle, NoFill)


    # for m in measurements_50bx:
    #     m.dump()
    # for m in measurements_25bx:
    #     m.dump()

    iterativeTimeCompare(measurements_720p4_25bx_NoDynInef_NoCCC, "720p4_NoDynInef_NoCCC")#, fillStyle, NoFill)
    for m in measurements_720p4_25bx_NoDynInef_NoCCC:
        m.dump()

    #waitKey()

if __name__ == "__main__":
    from ROOT import *
    main()
