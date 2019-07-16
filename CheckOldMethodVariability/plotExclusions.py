import sys
import ROOT
# Contains atlas style
sys.path.insert(0, '/afs/cern.ch/work/k/kpachal/PythonModules/art/')
import AtlasStyle

tag = "TLA"
#tag = "HighMassDijet"

infile = ROOT.TFile.Open("results_gaussians.root","READ")
#infile = ROOT.TFile.Open("results_gaussians_highmassdijet.root","READ")

widths =  ["res","0p05","0p07","0p10"] if "TLA" in tag else ["res","0p03","0p05","0p07","0p10","0p15"]

for width in widths :

  for model in ["DMsA","DMsV"] :

    for coupling in ["0.1","0.25"] :

        excluded = infile.Get("excluded_using_gaussians_{0}_{1}_gq{2}".format(model,width,coupling))
        not_excluded = infile.Get("not_excluded_using_gaussians_{0}_{1}_gq{2}".format(model,width,coupling))

        # Format
        excluded.SetMarkerStyle(20)
        excluded.SetMarkerColor(ROOT.kBlue)
        excluded.SetMarkerSize(1.5)

        not_excluded.SetMarkerStyle(24)
        not_excluded.SetMarkerColor(ROOT.kRed)
        not_excluded.SetMarkerSize(2)

        if "TLA" in tag :
            xlow = 0
            xhigh = 1200
        elif "HighMassDijet" in tag :
            xlow = 1100
            xhigh = 3500
        else :
            print "Unknown tag!"
            exit(1)

        # For plotting
        excluded.GetYaxis().SetRangeUser(0,1600)
        excluded.GetXaxis().SetRangeUser(xlow,xhigh)
        not_excluded.GetYaxis().SetRangeUser(0,1600)
        not_excluded.GetXaxis().SetRangeUser(xlow,xhigh)

        c = ROOT.TCanvas("c",'',0,0,800,600)
        if excluded.GetN() > 0 :
          excluded.Draw("AP")
          if not_excluded.GetN() > 0 :
            not_excluded.Draw("P SAME")
        else :
          if not_excluded.GetN() > 0 :
            not_excluded.Draw("AP")

        c.Update()
        c.SaveAs("plots/exclusion_width_{0}_{1}_gq{2}_{3}.eps".format(model,width,coupling.replace(".","p"),tag))

