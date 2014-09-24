from ROOT import *
import re

files = ['DQM_V0001_R000000001__Validation__Release720pre4-NoDynInef__PU140_BX25.root',
         'DQM_V0001_R000000001__Validation__Release720pre4-NoDynInef__PU70_BX25.root',
         'DQM_V0001_R000000001__Validation__Release720pre4-NoDynInef__PU40_BX25.root',
         'DQM_V0001_R000000001__Validation__Release720pre4-NoDynInef__PU25_BX25.root']
color = [kAzure+10, # 
         kViolet+10, # 
         kPink+10, #  
         kSpring] # 
file_titles = ['PU140','PU70','PU40','PU25']

folders = [
    'DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/selectedOfflinePrimaryVertices'#,
    #'DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/selectedPixelVertices'
    #'DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/'#,
]

histo_names = [
    {'name': 'RecoVtx_vs_GenVtx', 'o': 'xmax200', 'xAxis': 'Pileup Interactions', 'yAxis': 'Reco Vertices', 'yMax': '200', 'yMin': '0'},
    {'name': 'MatchedRecoVtx_vs_GenVtx', 'o': 'xmax200', 'xAxis': 'Pileup Interactions', 'yAxis': 'Matched Reco Vertices', 'yMax': '200', 'yMin': '0'},
    # {'name': 'RecoAllAssoc2GenProperties', 'o': '', 'xAxis': 'Kind of Reco Vertex', 'yAxis': '', 'yMax': '', 'yMin': ''},
    # {'name': 'RecoAllAssoc2Gen_PairDistanceZ', 'o': '', 'xAxis': 'Reco Vertex, Pair Distance', 'yAxis': '', 'yMax': '', 'yMin': ''},
    # {'name': 'globalEfficiencies', 'o': '', 'xAxis': '', 'yAxis': '', 'yMax': '', 'yMin': ''},
    # {'name': 'KindOfSignalPV', 'o': '', 'xAxis': 'Type Of Signal VTX', 'yAxis': '', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate', 'o': '', 'xAxis': 'Misidentification', 'yAxis': '', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate_vs_PU', 'o': '', 'xAxis': 'Pileup Interactions', 'yAxis': 'Misidentification', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate_vs_sum-pt2', 'o': 'logx', 'xAxis': '#sum_{pt^{2}}', 'yAxis': 'Misidentification', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate_vs_Z', 'o': '', 'xAxis': 'Z', 'yAxis': 'Misidentification', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate_vs_R', 'o': '', 'xAxis': 'R', 'yAxis': 'Misidentification', 'yMax': '', 'yMin': '0'},
    # {'name': 'MisTagRate_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'Misidentification', 'yMax': '', 'yMin': '0'},
    #  {'name': 'TruePVLocationIndex', 'o': 'norm', 'xAxis': 'True PV index in RecoVtx collection', 'yAxis': 'fraction of events', 'yMax': '1', 'yMin': ''},
     {'name': 'TruePVLocationIndexCumulative', 'o': 'norm', 'xAxis': 'Signal PV Status in Reco Collection', 'yAxis': 'Fraction of Events', 'yMax': '1.2', 'yMin': ''},
     {'name': 'effic_vs_NumVertices', 'o': '', 'xAxis': 'Pileup Interactions', 'yAxis': 'Efficiency', 'yMax': '1.1', 'yMin': '0'},
     {'name': 'effic_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'Efficiency', 'yMax': '1.2', 'yMin': '0'},
    # {'name': 'effic_vs_ClosestVertexInZ', 'o': 'logx', 'xAxis': 'Closest Distance in Z', 'yAxis': 'Efficiency', 'yMax': '', 'yMin': ''},
     {'name': 'effic_vs_Pt2', 'o': 'logx', 'xAxis': 'Vertex #sum pT^{2} [GeV^2]', 'yAxis': 'Efficiency', 'yMax': '1.2', 'yMin': '0'},
     {'name': 'effic_vs_Z', 'o': 'zoomz', 'xAxis': 'Vertex Z [cm]', 'yAxis': 'Efficiency', 'yMax': '1.2', 'yMin': '0'},
    # {'name': 'gen_duplicate_vs_NumVertices', 'o': '', 'xAxis': 'Number of Vertices', 'yAxis': 'GenLevel Duplicates', 'yMax': '', 'yMin': ''},
    # {'name': 'gen_duplicate_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'GenLevel Duplicates', 'yMax': '', 'yMin': ''},
    # {'name': 'gen_duplicate_vs_ClosestVertexInZ', 'o': 'logx', 'xAxis': 'Closest Distance in Z', 'yAxis': 'GenLevel Duplicates', 'yMax': '', 'yMin': ''},
    # {'name': 'gen_duplicate_vs_Pt2', 'o': 'logx', 'xAxis': '#sum_{pt^{2}}', 'yAxis': 'GenLevel Duplicates', 'yMax': '', 'yMin': ''},
    # {'name': 'gen_duplicate_vs_Z', 'o': '', 'xAxis': 'Z', 'yAxis': 'GenLevel Duplicates', 'yMax': '', 'yMin': ''},
    {'name': 'fakerate_vs_NumVertices', 'o': '', 'xAxis': 'Number of Vertices', 'yAxis': 'Fake Rate', 'yMax': '1.1', 'yMin': '0'},
    {'name': 'fakerate_vs_PU', 'o': '', 'xAxis': 'Pileup Interactions', 'yAxis': 'Fake Rate', 'yMax': '1.1', 'yMin': '0'},
    {'name': 'fakerate_vs_Ndof', 'o': '', 'xAxis': 'Vertex DOF', 'yAxis': 'Fake Rate', 'yMax': '1.2', 'yMin': '0'},
    # {'name': 'fakerate_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'Fake Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'fakerate_vs_ClosestVertexInZ', 'o': 'logx', 'xAxis': 'Closest Distance in Z', 'yAxis': 'Fake Rate', 'yMax': '', 'yMin': ''},
     {'name': 'fakerate_vs_Pt2', 'o': 'logx', 'xAxis': 'Vertex #sum pT^{2} [GeV^2]', 'yAxis': 'Fake Rate', 'yMax': '1.2', 'yMin': '0'},
    # {'name': 'fakerate_vs_Z', 'o': '', 'xAxis': 'Z', 'yAxis': 'Fake Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_NumVertices', 'o': '', 'xAxis': 'Number of Vertices', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_PU', 'o': '', 'xAxis': 'Pileup Interactions', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_ClosestVertexInZ', 'o': 'logx', 'xAxis': 'Closest Distance in Z', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_Pt2', 'o': 'logx', 'xAxis': '#sum_{pt^{2}}', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'duplicate_vs_Z', 'o': '', 'xAxis': 'Z', 'yAxis': 'Duplicate Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'merged_vs_NumVertices', 'o': '', 'xAxis': 'Number of Vertices', 'yAxis': 'Merge Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'merged_vs_PU', 'o': '', 'xAxis': 'Pileup Interactions', 'yAxis': 'Merge Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'merged_vs_NumTracks', 'o': '', 'xAxis': 'Number of Tracks in Vertex', 'yAxis': 'Merge Rate', 'yMax': '', 'yMin': ''},
     {'name': 'merged_vs_ClosestVertexInZ', 'o': 'logx', 'xAxis': 'Closest Distance in Z [cm]', 'yAxis': 'Merge Rate', 'yMax': '1.2', 'yMin': '0'},
    # {'name': 'merged_vs_Pt2', 'o': 'logx', 'xAxis': '#sum_{pt^{2}}', 'yAxis': 'Merge Rate', 'yMax': '', 'yMin': ''},
    # {'name': 'merged_vs_Z', 'o': '', 'xAxis': 'Z', 'yAxis': 'Merge Rate', 'yMax': '', 'yMin': ''}
    ## {'name': 'GenAllV_Z', 'o': '', 'xAxis': 'Vertex Z [cm]', 'yAxis': 'Number of Vertices', 'yMax': '', 'yMin': ''}
]

histograms = []
# Build full list of histograms
for h in histo_names:
    for f in folders:
        histograms.append({'name': '%s/%s' % (f, h['name']), 'o': h['o'],
                           'xAxis': h['xAxis'], 'yAxis': h['yAxis'],
                           'yMax': h['yMax'], 'yMin': h['yMin']})

file_handles = []

def TDRStyle():
    gROOT.ProcessLine(".L tdrStyle.C");
    setTDRStyle();
    gStyle.SetOptStat(0)
    #gSystem.AddDynamicPath("./")
    #gSystem.Load("tdrStyle_C")
    #setTDRStyle()
    pass

def prepareFileHandles():
    for file in files:
        file_handles.append(TFile(file))

def cleanOptions():
    gPad.SetLogx(0)
    gPad.SetLogy(0)

def setTextProperties(obj, label=False, title=False):
    textFont = 42
    textSize = 0.035
    titleOffset = 1.4
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

def drawCMSLabel():
    labelcms  = TPaveText(0.15,0.90,0.9,0.93,"NDCBR");
    labelcms.SetTextAlign(12);
    labelcms.SetTextSize(0.033);
    labelcms.SetFillColor(kWhite);
    labelcms.AddText("CMS Simulation, #sqrt{s} = 13 TeV, #bar{t}t + PU, BX=25ns");
    labelcms.SetBorderSize(0);
    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    return labelcms

def producePlots():
    gStyle.SetOptStat(0)
    c = TCanvas('c', 'c', 1024, 1024)
    histo = {}
    for h in histograms:
        icolor = 0
        counter = 0
        legend = TLegend(0.15,0.83,0.9,0.89)
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetNColumns(4)
        for f in file_handles:
            draw_options = ''
            histo = f.Get(h['name'])
            if not histo:
                print 'Failed to get histograms %s', h
            else:
                cleanOptions()
                if h['o'] != '':
                    if h['o'] == 'logx':
                        gPad.SetLogx()
                    if h['o'] == 'norm':
                        histo.Scale(1./histo.Integral())
                        histo.GetXaxis().SetBinLabel(1,'Not Reconstructed')
                        histo.GetXaxis().SetBinLabel(2,'Reco And Identified')
                        histo.GetXaxis().SetBinLabel(3,'Reco Not Identified')
                        draw_options += 'P,H '
                    if h['o'] == 'xmax200':
                        histo.GetXaxis().SetRangeUser(0,200)
                if counter == 0:
                    counter += 1
                    draw_options += 'P'
                else:
                    draw_options += 'SAME P'
                if h['yMax'] != '':
                    histo.SetMaximum(float(h['yMax']))
                if h['yMin'] != '':
                    histo.SetMinimum(float(h['yMin']))
                histo.GetXaxis().SetTitle(h['xAxis'])
                histo.GetYaxis().SetTitle(h['yAxis'])
                setTextProperties(histo.GetXaxis(), title=True)
                setTextProperties(histo.GetYaxis(), title=True)
                setTextProperties(histo.GetXaxis(), label=True)
                setTextProperties(histo.GetYaxis(), label=True)
                legend.AddEntry(histo,file_titles[icolor],'LP')
                if h['o'] == 'zoomz': histo.GetXaxis().SetRangeUser(-25,25)
                histo.SetMarkerStyle(20)
                histo.SetMarkerColor(color[icolor])
                histo.SetMarkerSize(1.2)
                histo.SetLineColor(color[icolor])
                histo.SetTitle('')
                histo.Draw(draw_options)
                (labelcms) = drawCMSLabel()
                labelcms.Draw()
                legend.Draw()
                c.Update()
                c.SaveAs('%s' % ("_".join(h['name'].split('/')[-2:]) + ".png"))
                icolor += 1

if __name__ == '__main__':
    TDRStyle()
    prepareFileHandles()
    producePlots()
