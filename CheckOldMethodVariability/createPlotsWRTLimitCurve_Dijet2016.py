import ROOT
import sys,os
import math

# For extrapolating from cross-section versus mass limits
def find_limit(mass, indict, subval = "") :

  if mass in indict.keys() :
    return indict[mass]

  for check in sorted(indict.keys()) :
    if check < mass :
      mlow = check 
    check_index = sorted(indict.keys()).index(check)+1
    if check_index < len(indict.keys())-1 :
      check_val = sorted(indict.keys())[check_index+1]
    else :
      check_val = check
    if check_val > mass :
      mlow = check
      mhigh = check_val
      break

  print "For mass",mass,"found mlow, mhigh",mlow,mhigh

# Get dictionary of all points' info by DSID
import sys
sys.path.insert(0, 'inputs/dictionaries/')
from ParameterDict_DijetHighMass_13TeV_Full20152016 import paramDict_HighMass_13TeV_Full20152016 as paramDict
from XSecDict_DijetHighMass_13TeV_Full20152016 import signalCrossSectionDict as xsecDict
from Acceptances_DijetHighMass_13TeV_Full20152016_All import AcceptanceDict_DijetHighMass_13TeV_Full20152016 as acc_all

# Get dictionary of Gaussian limits
file_limits = open('inputs/limit_vals/HighMassDijet_gaussians.txt', 'r')
limits = eval(file_limits.read())
file_limits.close()

fullDict = {}

# Look at every point
for point in paramDict.keys() :

  # Get all info, going to merge into a massive monsterdict
  localDict = {}  
  params = paramDict[point]
  xsec_info = xsecDict[point]

  # Get acceptance: stored by acceptance and model, so a little annoying
  mZP = params["mmed"]
  model = params["model"]

  if not point in acc_all.keys() :
    print "No acceptance for",model,"point at mZP =",mZP," mDM =",params["mdm"]
    continue
  acc = acc_all[point]

  # Calculate sigma * BR * A for each point, store as theory
  # Check units before running....
  theory = xsec_info['xsec']*acc['acc']

  mZP_TeV = mZP/1000.

  # Get possible limits to compare to
  limits_dict = {}

  # Didn't make points lower.
#  if mZP < 450 : continue

  if not mZP_TeV in limits.keys() :
    print "No limit for mass",mZP
    continue

  my_limits = limits[mZP_TeV]
  for key in my_limits.keys() :
    limits_dict[key] = my_limits[key]

  # For each point, define a bool of excluded or not excluded 
  # relative to each available limit
  results_dict = {}
  for key in limits_dict.keys() :
    obs_limit = limits_dict[key]
    excluded = False
    if obs_limit <= theory :
      excluded = True
    results_dict[key] = excluded

  # Doing more similar to old method: 
  # get acceptance by truncating histogram to 0.8 < M < 1.2
  
  # Save everything in mosterdict
  localDict.update(params)
  localDict.update(xsec_info)
  localDict['theory'] = theory
  localDict['limits'] = limits_dict
  localDict['results'] = results_dict
  #print localDict
  fullDict[point] = localDict

# Using same limit for all (same Gaussian width, etc):
# Make TGraph of points which are in and points which are out
outfile = ROOT.TFile.Open("results_gaussians_highmassdijet.root",'RECREATE')
outfile.cd()

for model in ["DMsA","DMsV"] :

  for coupling in [0.10,0.25] :

    for width in ["res","0p03","0p05","0p07","0p10","0p15"] :

      excluded = ROOT.TGraph()
      not_excluded = ROOT.TGraph()

      for point in fullDict.keys() :

        info = fullDict[point]

        # Skip if not the model we want
        if not model in info['model'] :
          continue

        # Skip if not the coupling we want
        if not math.fabs(coupling - info['gq']) < 0.01 :
          continue

        mMed = info['mmed']
        mDM = info['mdm']

        if not width in info['results'].keys() :
          continue

        did_exclude = info['results'][width]

        if did_exclude :
          excluded.SetPoint(excluded.GetN(),mMed,mDM)
        else :
          not_excluded.SetPoint(not_excluded.GetN(),mMed,mDM)

      excluded.Write("excluded_using_gaussians_{0}_{1}_gq{2}".format(model,width,coupling))
      not_excluded.Write("not_excluded_using_gaussians_{0}_{1}_gq{2}".format(model,width,coupling))

outfile.Close()

#Mix?








