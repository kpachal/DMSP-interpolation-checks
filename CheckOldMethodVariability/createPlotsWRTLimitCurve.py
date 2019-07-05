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
from ParameterDict_DijetTLA_13TeV_Full2015 import paramDict_DijetTLA_13TeV_Full2015 as paramDict
from XSecDict_DijetTLA_13TeV_Full2015 import signalCrossSectionDict as xsecDict
from Acceptances_DijetTLA_13TeV2018_Full20152016_A2_y03 import thisdict as acc_A2_y03 
from Acceptances_DijetTLA_13TeV2018_Full20152016_A2_y06 import thisdict as acc_A2_y06 
from Acceptances_DijetTLA_13TeV2018_Full20152016_V2_y03 import thisdict as acc_V2_y03 
from Acceptances_DijetTLA_13TeV2018_Full20152016_V2_y06 import thisdict as acc_V2_y06 

# Get dictionary of Gaussian limits
file_03 = open('inputs/limit_vals/TLA_gaussians_y03.txt', 'r')
limits_03 = eval(file_03.read())
file_03.close()
file_06 = open('inputs/limit_vals/TLA_gaussians_y06.txt', 'r')
limits_06 = eval(file_06.read())
file_06.close()

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
  if mZP < 700 and "DMsA" in model :
    accdict = acc_A2_y03
  elif mZP > 700 and "DMsA" in model :
    accdict = acc_A2_y06
  elif mZP < 700 and "DMsV" in model :
    accdict = acc_V2_y03
  elif mZP > 700 and "DMsV" in model :
    accdict = acc_V2_y06

  if not point in accdict.keys() :
#    print "No acceptance for",model,"point at mZP =",mZP," mDM =",params["mdm"]
    continue
  acc = accdict[point]

  # Calculate sigma * BR * A for each point, store as theory
  # At this point, basically blending 0.3 and 0.6
  theory = xsec_info['xsec']*acc['acc']

  # Get possible limits to compare to
  limits_dict = {}
  gauss_dict = limits_03 if mZP < 700 else limits_06

  # Didn't make points lower.
  if mZP < 450 : continue

  #limit = find_limit(mZP,gauss_dict,"0p07")

  my_limits = gauss_dict[mZP]
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
  localDict['results_firstmethod'] = results_dict
  #print localDict
  fullDict[point] = localDict

# Using same limit for all (same Gaussian width, etc):
# Make TGraph of points which are in and points which are out
outfile = ROOT.TFile.Open("results_gaussians.root",'RECREATE')
outfile.cd()
for width in ["res","0p05","0p07","0p10"] :

  for model in ["DMsA","DMsV"] :

    for coupling in [0.10,0.25] :

      excluded = ROOT.TGraph()
      not_excluded = ROOT.TGraph()

      for point in fullDict.keys() :

        info = fullDict[point]

        # Skip if not the model we want
        if not model in info['model'] :
          continue

        # Skip if not the coupling we want
        if not math.fabs(coupling - info['gq'] < 0.01) :
          continue

        mMed = info['mmed']
        mDM = info['mdm']

        # Something odd going on with overlapping points. Cross check
        #if "res" in width and 699 < mMed and mMed < 701 and mDM < 50 :
        #  print "in point!"
        #  print point, info
        # Difference: DMsV versus DMsA. Forgot that here?

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








