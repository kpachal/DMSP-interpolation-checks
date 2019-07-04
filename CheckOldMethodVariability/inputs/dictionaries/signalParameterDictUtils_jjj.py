#!/bin/python

from ROOT import *
from glob import glob

def makeSignalArrayJjj() :
    
    ##Karol's dictionary: mR,mDM,gSM,gDM.

    JjjDictionary = { 350: {1: {0.25: {1.0: 0.34943382162600756}},
       50: {0.25: {1.0: 0.3640745292796055}},
       100: {0.25: {1.0: 0.4553182041272521}},
       150: {0.25: {1.0: 0.6247355900704861}},
       200: {0.25: {1.0: 0.7278221389860846}},
       300: {0.25: {1.0: 0.7788825617171824}},
       400: {0.25: {1.0: 0.7374721802771091}},
       500: {0.25: {1.0: 0.701887699746294}},
       600: {0.25: {1.0: 0.7265932960435748}},
       700: {0.25: {1.0: 0.7359788970788941}},
       800: {0.25: {1.0: 0.0}},
       900: {0.25: {1.0: 0.7500237796339206}},
       1000: {0.25: {1.0: 0.0}},
       1100: {0.25: {1.0: 0.7374721802771091}},
       1200: {0.25: {1.0: 0.7011947688879445}},
       1300: {0.25: {1.0: 0.7361728065880015}},
       1400: {0.25: {1.0: 0.7347026509232819}},
       1500: {0.25: {1.0: 0.0}},
       1600: {0.25: {1.0: 0.7244833483127877}},
       1700: {0.25: {1.0: 0.7270773134077899}},
       1800: {0.25: {1.0: 0.7251002127013635}},
       1900: {0.25: {1.0: 0.7171570060891099}},
       2000: {0.25: {1.0: 0.7178356344811618}}},
 400: {1: {0.25: {1.0: 0.32888049815665}},
       50: {0.25: {1.0: 0.3405348842206877}},
       100: {0.25: {1.0: 0.39054351006052457}}},
 425: {50: {0.25: {1.0: 0.32919681287603453}},
       100: {0.25: {1.0: 0.35989489656640217}}},
 450: {1: {0.25: {1.0: 0.29923904314637184}},
       50: {0.25: {1.0: 0.2964224378520157}},
       100: {0.25: {1.0: 0.3375251650431892}}},
 500: {1: {0.25: {1.0: 0.2940357572661014}},
       50: {0.25: {1.0: 0.28863882372388616}},
       100: {0.25: {1.0: 0.3244699771312298}}},
 550: {1: {0.25: {1.0: 0.29414818256918807}},
       50: {0.25: {1.0: 0.29993737347831484}},
       100: {0.25: {1.0: 0.3023333176388405}}},
}    ###End of Karol's dictionary


    #get mjj histogram

    JjjDictionaryOutput = {}

    #def findgjjSample(infile) :

    for infile in glob("signals/DijetJetHistos/Histograms/OUT_dijetjet_truth/*NTUP*.root") :
        infile = infile.lstrip("signals/DijetJetHistos/Histograms/OUT_dijetjet_truth/")
        infile = "hist"+infile
        #print infile
        inROOTfile = TFile.Open("signals/DijetJetHistos/Histograms/OUT_dijetjet_truth/"+infile)
        mjjhist = inROOTfile.Get("trijet_j430_2j25/Zprime_mjj_var")

        #parse what we're talking about
        mMed = infile.split("_")[6].strip("mR")
        #    if mMed[0] == "p" :
        #        mMed = float("0."+mMed[1])*1000
        #    else :
        #        mMed = float(str(mMed[0])+"."+str(mMed[1]))*1000
        tokensMmed = mMed.split("p")
        if tokensMmed[0] == "" : tokensMmed[0] = 0
        if len(tokensMmed)==1 : mMed = 1000
        else : mMed = float(str(tokensMmed[0])+"."+str(tokensMmed[1]))*1000


        mDM = infile.split("_")[7].strip("mD")
        tokens = mDM.split("p")
        if tokens[0] == "" : tokens[0] = 0
        if len(tokens)==1 : mDM = 1000
        else : mDM = float(str(tokens[0])+"."+str(tokens[1]))*1000

        #print mMed, mDM
        #find the acc*xsec, which is the 2nd thing in the dictionary above
        aTimesXsec = None
        try :
            aTimesXsec = JjjDictionary[mMed][mDM][0.25][1.0]
        except :
            continue
        if aTimesXsec == 0. : continue
        #print mMed, mDM,  aTimesXsec, mjjhist#in picobarns
        #return mMed, mDM,  aTimesXsec#in picobarns
        JjjDictionaryOutput[infile] = { 'gq' : 0.25 ,
                  'gdm' : 1.0 ,
                  'mdm' : mDM ,
                  'mmed' : mMed,
                  'width' : 0.0 ,
                  'xsec' : aTimesXsec ,
                  'xsec_error' : 0.0 ,
                  'dsid' : 999999,
                      }

        #output: SIGNALS [{'mmed': 1200.0, 'width': 74.269024, 'gq': 0.1, 'mdm': 100.0, 'xsec_error': 5.414e-05, 'xsec': 0.0996, 'dsid': 230000, 'gdm': 1.5},


    #findgjjSample("hist-MC15.999999.MGPy8EG_N30LO_A14N23LO_dmA_jja_Ph100_mRp4_mDp1_gSp25_gD1.NTUP.root")
    return JjjDictionaryOutput


