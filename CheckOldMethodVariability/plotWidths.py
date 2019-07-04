import ROOT
import sys
sys.path.insert(0, '/afs/cern.ch/work/k/kpachal/PythonModules/art/')
import AtlasStyle

AtlasStyle.SetAtlasStyle()
ROOT.gROOT.ForceStyle()

# Want to compare 3 things:
#  - points in the nose where there is disagreement: 
#  - mMed = 750 & 800, mDM = 1.0, A-V plot couplints
# with points from the paper couplings which match this plot:
# https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CombinedSummaryPlots/EXOTICS/ATLAS_DarkMatterCoupling_Summary/ATLAS_DarkMatterCoupling_Summary.pdf
# where we have 10% width and 7% width

# Analysis couplings available: up to 0.4

infile_narrow = "/afs/cern.ch/work/k/kpachal/TLA2017/CleanLimitCode/inputs/dataLikeHists_yStar06/dataLikeHistograms.m{0}_g0.05.root"
infile_broad = "/afs/cern.ch/work/k/kpachal/TLA2017/CleanLimitCode/inputs/dataLikeHists_yStar06/dataLikeHistograms.m{0}_g0.40.root"
infile_target = "/afs/cern.ch/work/k/kpachal/TLA2017/CleanLimitCode/inputs/signalsForMassMass/DijetTLA_13TeV2018_Full20152016_A2_y06_dataLikeHists_v1/dataLikeHistograms.{0}.root"

# this correlates the two points on the x axis which we want to check 
# to DSIDs
DSIDtoMass = {
310055 : {"mMed" : 750.0},
310065 : {"mMed" : 800.0}
}

# Check both masses
for mass in ["0.75","0.8"] :

  # Get all 3 hists
  open_narrow = ROOT.TFile.Open(infile_narrow.format(mass))
  hist_narrow = open_narrow.Get("mjj_Scaled_m{0}_g0.05_1fb_Nominal".format(mass))
  hist_narrow.SetDirectory(0)
  open_narrow.Close()

  open_broad = ROOT.TFile.Open(infile_broad.format(mass))
  hist_broad = open_broad.Get("mjj_Scaled_m{0}_g0.40_1fb_Nominal".format(mass))
  hist_broad.SetDirectory(0)
  open_broad.Close()

  mass_number = eval(mass)*1000.
  for DSID in DSIDtoMass.keys() :
    if (DSIDtoMass[DSID]["mMed"] - mass_number)/mass_number < 0.01 :
      break
  open_target = ROOT.TFile.Open(infile_target.format(DSID))
  hist_target = open_target.Get("Nominal/mjj_Scaled_{0}_1fb".format(DSID))
  hist_target.SetDirectory(0)
  open_target.Close()

  # Want to plot the three on top of each other
  # Normalise for convenience of comparing
  hist_narrow.Scale(1.0/hist_narrow.Integral())
  hist_broad.Scale(1.0/hist_broad.Integral())
  hist_target.Scale(1.0/hist_target.Integral())

  c = ROOT.TCanvas("c_{0}".format(mass),'',0,0,800,600)
  hist_narrow.SetLineColor(ROOT.kGreen+2)
  hist_narrow.SetLineWidth(2)
  hist_narrow.GetXaxis().SetTitle("Mass [GeV]")
  hist_narrow.GetYaxis().SetTitle("A.U.")
  hist_narrow.GetXaxis().SetRangeUser(mass_number*(0.5),mass_number*(1.4))
  hist_target.SetLineColor(ROOT.kMagenta+1)
  hist_target.SetLineWidth(2)
  hist_broad.SetLineColor(ROOT.kBlue)
  hist_broad.SetLineWidth(2)

  hist_narrow.Draw("HIST")
  hist_broad.Draw("HIST SAME")
  hist_target.Draw("HIST SAME")

  c.Update()
  c.SaveAs("plots/width_comparison_{0}.eps".format(mass))


