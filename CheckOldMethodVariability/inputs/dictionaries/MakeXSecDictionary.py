#!/bin/python

theline = "/afs/cern.ch/user/d/doglioni/cateos/atlas/atlascerngroupdisk/phys-exotics/jdm/dijet/mc15truth/DMsummary/230189/log.generate.bz213:42:40      Cross-section :   0.05736 +- 2.184e-05 pb"

#want:     470000: { 'xsec':   4.331 , 'xsec_error': 0.005108 },

fin = open("xsec-90")

for theline in fin.readlines() :
    #print theline
    dsid = theline.split("/")[14]
    xsec = theline.split("Cross-section :")[1].strip().split("+-")[0]
    xsecError = theline.split("Cross-section :")[1].strip().split("+-")[1].strip(" pb")
    print dsid, ": { 'xsec': ", xsec, ", 'xsec_error': ", xsecError, " }, "