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
iterLabels['0'] = ['initialStepClusters',
                   'initialStepSeedLayers',
                   'initialStepSeeds',
                   'initialStepTrackCandidates',
                   'initialStepTracks',
                   'initialStepSelector',
                   'initialStep']
iterLabels['1'] = ['lowPtTripletStepClusters',
                   'lowPtTripletStepSeedLayers',
                   'lowPtTripletStepSeeds',
                   'lowPtTripletStepTrackCandidates',
                   'lowPtTripletStepTracks',
                   'lowPtTripletStepSelector']
iterLabels['2'] = ['pixelPairStepClusters',
                   'pixelPairStepSeedLayers',
                   'pixelPairStepSeeds',
                   'pixelPairStepTrackCandidates',
                   'pixelPairStepTracks',
                   'pixelPairStepSelector']
iterLabels['3'] = ['detachedTripletStepClusters',
                   'detachedTripletStepSeedLayers',
                   'detachedTripletStepSeeds',
                   'detachedTripletStepTrackCandidates',
                   'detachedTripletStepTracks',
                   'detachedTripletStepSelector',
                   'detachedTripletStep']
iterLabels['4'] = ['mixedTripletStepClusters',
                   'mixedTripletStepSeedLayersA',
                   'mixedTripletStepSeedLayersB',
                   'mixedTripletStepSeedsA',
                   'mixedTripletStepSeedsB',
                   'mixedTripletStepSeeds',
                   'mixedTripletStepTrackCandidates',
                   'mixedTripletStepTracks',
                   'mixedTripletStepSelector',
                   'mixedTripletStep']
iterLabels['5'] = ['pixelLessStepClusters',
                   'pixelLessStepSeedClusters',
                   'pixelLessStepSeedLayers',
                   'pixelLessStepSeeds',
                   'pixelLessStepTrackCandidates',
                   'pixelLessStepTracks',
                   'pixelLessStepSelector',
                   'pixelLessStep']
iterLabels['6'] = ['tobTecStepClusters',
                   'tobTecStepSeedClusters',
                   'tobTecStepSeedLayersTripl',
                   'tobTecStepSeedLayersPair',
                   'tobTecStepSeedsTripl',
                   'tobTecStepSeedsPair',
                   'tobTecStepSeed',
                   'tobTecStepTrackCandidates',
                   'tobTecStepTracks',
                   'tobTecStepSelector']

iterLabels31 = copy.deepcopy(iterLabels)
iterLabels31['3'] = iterLabels['1']
iterLabels31['1'] = iterLabels['3']

def checkEnvs():
    localrt = os.getenv("LOCALRT")
    if not localrt:
        print "Error, CMSSW environment not set."
    return

def makeFrame(name, title, xtitle, ytitle, xll, yll, xur, yur):
    c = TCanvas(name, name, 1024, 768)
    x = array("f", [xll, xur])
    y = array("f", [yll, yur])
    g = TGraphErrors(len(x), x, y)
    g.SetMarkerSize(0)
    g.SetTitle(title)
    g.GetXaxis().SetTitle(xtitle)
    g.GetYaxis().SetTitle(ytitle)
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
                        print_labels_for_points
                        ):
    gr = []
    pu_text = []
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
            for step in steps:
                iy[int(step)].append(measurements[i].iterative_time_[step]/1000./measurements[i].processed_events_) # 1000 for ms
    if kind != 'IterativeTime_vs_PU' and kind != 'IterativeTime_vs_LUMI':
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

        if print_labels_for_points[0]:
            for l in range(0, len(x)):
                pu_text.append(TText(x[l], y[l]*print_labels_for_points[1] + print_labels_for_points[2], "%d" % int(measurements[l].pileup_)))
                pu_text[-1].SetTextFont(23)
                pu_text[-1].SetTextSize(20)
                pu_text[-1].SetTextAlign(22)
                pu_text[-1].Draw()
        if not legend:
            legend = TLegend(0.1, 0.65, 0.4, 0.9)
            legend.SetFillColor(0)
            legend.SetHeader("PileUp Scenarios")
        legend.AddEntry(gr[-1], label, legend_kind)
        legend.Draw()
    elif kind == 'IterativeTime_vs_PU' or kind == 'IterativeTime_vs_LUMI':
        if not legend:
            legend = TLegend(0.1, 0.45, 0.3, 0.9)
            legend.SetFillColor(0)
            legend.SetHeader("PileUp Scenarios")
        for i in range(len(steps)):
            gr.append(TGraphErrors(len(x), x, iy[i], ex, ey))
            gr[-1].SetMarkerStyle(marker_style+i)
            gr[-1].SetMarkerColor(iterColor[i])
            gr[-1].SetMarkerSize(1.2)
            gr[-1].SetFillColor(iterColor[i])
            gr[-1].SetLineColor(iterColor[i])
            gr[-1].SetLineStyle(line_type)
            gr[-1].SetLineWidth(2)
            gr[-1].SetFillStyle(fill_pattern)
            gr[-1].Draw("CP")
            legend.AddEntry(gr[-1], "%s Iter%d" % (label, i), legend_kind)
        if print_labels_for_points[0]:
            for l in range(0, len(x)):
                pu_text.append(TText(x[l], iy[-1][l]*print_labels_for_points[1] + print_labels_for_points[2], "%d" % int(measurements[l].pileup_)))
                pu_text[-1].SetTextFont(23)
                pu_text[-1].SetTextSize(16)
                pu_text[-1].SetTextAlign(22)
                pu_text[-1].Draw()
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
    RECO_MODULES_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/process RECO/Paths/reconstruction_step_module_total'
    RECO_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/process RECO/Paths/reconstruction_step_total'
    EVENT_TIME_HISTO = '/DQMData/Run 1/DQM/Run summary/TimerService/event'
#    TRACKS_HISTO = '/DQMData/Run 1/TrackingTime/Run summary/Algo/Algo_For_HP'
    def __init__(self, file, verbose=0):
        self.verbose_ = verbose
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
        h = self.ROOT_file_.Get(Measure.RECO_TIME_HISTO)
        self.reco_total_time_ = h.GetMean()
        self.reco_total_time_rms_ = h.GetRMS()
        h = self.ROOT_file_.Get(Measure.EVENT_TIME_HISTO)
        self.processed_events_ = h.GetEntries()
        self.event_time_ = h.GetMean()
        self.event_time_rms_ = h.GetRMS()
        h = self.ROOT_file_.Get(Measure.RECO_MODULES_TIME_HISTO)
        steps = sorted(iterLabels.keys())
        for step in steps:
            self.iterative_time_[step] = 0.
            labels = iterLabels[step]
            for l in labels:
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
    (c, g) = makeFrame("RecoTimePU",
                       "Reco Time - %s" % release_label,
                       "PileUp",
                       "Time/Event [s]",
                       20,
                       0,
                       150,
                       200)
    (g0, legend, t) = makeGenericTimePlot('TotalEventTime_vs_PU',
                                          measurements,
                                          "%d ns - FullEvent" % measurements[0].bunch_spacing_,
                                          kAzure+5,
                                          23,
                                          1,
                                          NoFill,
                                          None,
                                          'lp',
                                          (False, 0, 0))
    (g1, legend, t) = makeGenericTimePlot('TotalRecoTime_vs_PU',
                                          measurements,
                                          "%d ns - Reco Only" % measurements[0].bunch_spacing_,
                                          kAzure,
                                          21,
                                          1,
                                          fillStyle[0],
                                          legend,
                                          'f',
                                          (False, 0, 0))
    (g2, legend, t) = makeGenericTimePlot('TotalIterativeTime_vs_PU',
                                          measurements,
                                          "%d ns - IterativeTime Only" % measurements[0].bunch_spacing_,
                                          kAzure-5,
                                          20,
                                          1,
                                          NoFill,
                                          legend,
                                          'lp',
                                          (False, 0, 0))
    c.SaveAs("RecoTimePU_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
                                                  release_label))

def totalEventTime_vs_LUMI(measurements,
                           release_label,
                           fillStyle,
                           NoFill):
    (cl, gl) = makeFrame("RecoTimeLUMI",
                         "Reco Time - %s" % release_label,
                         "Luminosity [10^{34} cm^{-2} s^{-1}]",
                         "Time/Event [s]",
                         0.5,
                         0,
                         5.0,
                         200)
    (g7a, legendl, p) = makeGenericTimePlot('TotalEventTime_vs_LUMI',
                                            measurements,
                                            "%d ns - Full Event" % measurements[0].bunch_spacing_,
                                            kAzure+5,
                                            23,
                                            1,
                                            NoFill,
                                            None,
                                            'lp',
                                            (True, 1., 12))
    (g7, legendl, p) = makeGenericTimePlot('TotalRecoTime_vs_LUMI',
                                           measurements,
                                           "%d ns - Reco Only" % measurements[0].bunch_spacing_,
                                           kAzure,
                                           21,
                                           1,
                                           fillStyle[0],
                                           legendl,
                                           'f',
                                           (True, 1., 12))
    (g8, legendl, t) = makeGenericTimePlot('TotalIterativeTime_vs_LUMI',
                                           measurements,
                                           "%d ns - IterativeTime" % measurements[0].bunch_spacing_,
                                           kAzure-5,
                                           20,
                                           1,
                                           1,
                                           legendl,
                                           'lp',
                                           (False, 0, 0))
    cl.SaveAs("RecoTimeLUMI_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
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
                         150,
                         200)
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
    ci.SaveAs("IterativeTimePU_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
                                                        release_label))

    # Iterative Steps Details LUMI
    (cil, gil) = makeFrame("IterativeTimeLUMI",
                           "Iterative Time - %s" % release_label,
                           "Luminosity [10^{34} cm^{-2} s^{-1}]",
                           "Time/Event [s]",
                           0.5,
                           0,
                           5.0,
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
    cil.SaveAs("IterativeTimeLUMI_%d_BX_%s_Nehalem.png" % (measurements[0].bunch_spacing_,
                                                           release_label))

def main():
    if not checkEnvs():
        pass
    measurements_25bx = []
    measurements_50bx = []

#    measurements_50bx.append(Measure('AVE_25_BX_50ns/DQM_V0001_R000000001__MyTiming__Release700__PU25_BX50.root', 1))
#    measurements_50bx.append(Measure('AVE_50_BX_50ns/DQM_V0001_R000000001__MyTiming__Release700__PU50_BX50.root', 1))
    measurements_25bx.append(Measure('AVE_25_BX_25ns/DQM_V0001_R000000001__MyTiming__Release710pre7__PU25_BX25.root' ,1))
    measurements_25bx.append(Measure('AVE_40_BX_25ns/DQM_V0001_R000000001__MyTiming__Release710pre7__PU40_BX25.root' ,1))
    measurements_25bx.append(Measure('AVE_70_BX_25ns/DQM_V0001_R000000001__MyTiming__Release710pre7__PU70_BX25.root' ,1))
    measurements_25bx.append(Measure('AVE_140_BX_25ns/DQM_V0001_R000000001__MyTiming__Release710pre7__PU140_BX25.root' ,1))
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
#    totalEventTime_vs_PU(measurements_50bx, "710pre4", fillStyle, NoFill)
#    totalEventTime_vs_LUMI(measurements_50bx, "710pre4", fillStyle, NoFill)
#    iterativeTime(measurements_50bx, "710pre4", fillStyle, NoFill)

    # 25 ns
    totalEventTime_vs_PU(measurements_25bx, "710pre7", fillStyle, NoFill)
    totalEventTime_vs_LUMI(measurements_25bx, "710pre7", fillStyle, NoFill)
    iterativeTime(measurements_25bx, "710pre7", fillStyle, NoFill)

    for m in measurements_50bx:
        m.dump()
    for m in measurements_25bx:
        m.dump()

    waitKey()

if __name__ == "__main__":
    from ROOT import *
    main()
