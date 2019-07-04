import sys
import ROOT
# Contains atlas style
sys.path.insert(0, '/afs/cern.ch/work/k/kpachal/PythonModules/art/')
import AtlasStyle

infile = ROOT.TFile.Open("results_gaussians.root","READ")

for width in ["res","0p05","0p07","0p10"] :

  for model in ["DMsA","DMsV"] :

    excluded = infile.Get("excluded_using_gaussians_{0}_{1}".format(model,width))
    not_excluded = infile.Get("not_excluded_using_gaussians_{0}_{1}".format(model,width))

    # Format
    excluded.SetMarkerStyle(20)
    excluded.SetMarkerColor(ROOT.kBlue)
    excluded.SetMarkerSize(1.5)

    not_excluded.SetMarkerStyle(24)
    not_excluded.SetMarkerColor(ROOT.kRed)
    not_excluded.SetMarkerSize(2)

    # For plotting
    excluded.GetYaxis().SetRangeUser(0,1200)
    excluded.GetXaxis().SetRangeUser(0,1200)

    c = ROOT.TCanvas("c",'',0,0,800,600)
    excluded.Draw("AP")
    not_excluded.Draw("P SAME")

    c.Update()
    c.SaveAs("plots/exclusion_width_{0}_{1}.eps".format(model,width))

