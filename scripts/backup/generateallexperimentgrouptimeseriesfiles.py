#! /usr/bin/env python
import sys
import os.path
import nco
import string
import subprocess
import datetime as date
import numpy as np
import pandas as pd
import netCDF4 as netcdf4
# import xarray as xr
# import matplotlib.pyplot as plt

import gfileutils as gf

# Global Variables

nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 

# Function Definitions

# Main Body

arguments = len(sys.argv) - 1

if (arguments != 11):
    print("Error: Usage generateallexperimentgrouptimeseries10yrfiles.py experimentgroup experimentgrouphistorylist experiment experimentlist startyear endyear generateexperimentgroupcommand submitupdateexperimentgroupcommand submissions queuename projectcode")
    sys.exit()
else:
    print("Processing: " + str(sys.argv[1]) + " => " + str(sys.argv[2]))


experimentgroupname = str(sys.argv[1])
experimentgrouphistorylistfilename = str(sys.argv[2])

experimentgrouphistorylistfile = open(experimentgrouphistorylistfilename,'r')
experimentgrouphistorylist = experimentgrouphistorylistfile.readlines()
numexperimentgrouphistorys = len(experimentgrouphistorylist)
experimentgrouphistoryshortnames = [""] * numexperimentgrouphistorys
experimentgrouphistoryfiletypes = [""] * numexperimentgrouphistorys
experimentgrouphistorysourcedirs = [""] * numexperimentgrouphistorys
experimentgrouphistorysources = [""] * numexperimentgrouphistorys
experimentgrouphistoryoutputdirs = [""] * numexperimentgrouphistorys
experimentgrouphistoryoutputs = [""] * numexperimentgrouphistorys
experimentgrouphistorytimetypes = [""] * numexperimentgrouphistorys
experimentgrouphistoryfilesperyears = [""] * numexperimentgrouphistorys
experimentgrouphistorydaysperfiles = [""] * numexperimentgrouphistorys
experimentgrouphistorytimesperfiles = [""] * numexperimentgrouphistorys
numexperimentgrouphistoryfiles = 0
for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
    experimentgrouphistorylistvalues = experimentgrouphistorylist[experimentgrouphistorylistindex].split()
    experimentgrouphistoryshortnames[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[0]
    experimentgrouphistoryfiletypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[1]
    experimentgrouphistorysourcedirs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[2]
    experimentgrouphistorysources[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[3]
    experimentgrouphistoryoutputdirs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[4]
    experimentgrouphistoryoutputs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[5]
    experimentgrouphistorytimetypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[6]
    experimentgrouphistoryfilesperyears[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[7]
    experimentgrouphistorydaysperfiles[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[8]
    experimentgrouphistorytimesperfiles[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[9]
    if (experimentgroupname == experimentgrouphistoryshortnames[experimentgrouphistorylistindex]):
        numexperimentgrouphistoryfiles += 1

if (numexperimentgrouphistoryfiles == 0):
    print("Unknown Experiment Group: " + experimentgroupname)
    sys.exit()

gf.experimentgrouphistoryshortname = experimentgroupname

print("Experiment Group Details")
print("Name: " + gf.experimentgrouphistoryshortname)

experimentname = str(sys.argv[3])
experimentlistfilename = str(sys.argv[4])

experimentlistfile = open(experimentlistfilename,'r')
experimentlist = experimentlistfile.readlines()
numexperiments = len(experimentlist)
experimentshortnames = [""] * numexperiments
experimentlocations = [""] * numexperiments
experimentlongnames = [""] * numexperiments
experimentstartyearnames = [""] * numexperiments
experimentendyearnames = [""] * numexperiments
experimentindex = -1
for experimentlistindex in range(numexperiments):
    experimentlistvalues = experimentlist[experimentlistindex].split()
    experimentshortnames[experimentlistindex] = experimentlistvalues[0]
    experimentlocations[experimentlistindex] = experimentlistvalues[1]
    experimentlongnames[experimentlistindex] = experimentlistvalues[2]
    experimentstartyearnames[experimentlistindex] = experimentlistvalues[3]
    experimentendyearnames[experimentlistindex] = experimentlistvalues[4]
    if (experimentname == experimentshortnames[experimentlistindex]):
        experimentindex = experimentlistindex

if (experimentindex == -1):
    print("Unknown Experiment: " + experimentgroupname)
    sys.exit()

gf.experimentshortname = experimentshortnames[experimentindex]
gf.experimentlocation = experimentlocations[experimentindex]
gf.experimentlongname = experimentlongnames[experimentindex]
gf.experimentstartyearname = experimentstartyearnames[experimentindex]
gf.experimentstartyear = int(gf.experimentstartyearname)
gf.experimentendyearname = experimentendyearnames[experimentindex]
gf.experimentendyear = int(gf.experimentendyearname)

print("Experiment Details")
print("Name: " + gf.experimentshortname)
print("Location: " + gf.experimentlocation)
print("Experiment: " + gf.experimentlongname)
print("Start Year: " + gf.experimentstartyearname)
print("End Year: " + gf.experimentendyearname)

experimentnumtotalyears = gf.experimentendyear - gf.experimentstartyear + 1
experimentnumtotalmonths = experimentnumtotalyears * 12
experimentnumtotaldays = experimentnumtotalyears * 365
experimentnum10yrfiles = int(experimentnumtotalyears / 10)
experimentnumextrayears = experimentnumtotalyears - (experimentnum10yrfiles * 10)
if (experimentnumextrayears > 0):
    experimentnum10yrfiles += 1
    
experimentnumyears = np.zeros(experimentnum10yrfiles,dtype=int)
experimentnummonths = np.zeros(experimentnum10yrfiles,dtype=int)
experimentnumdays = np.zeros(experimentnum10yrfiles,dtype=int)
experimentnumtimes = np.zeros(experimentnum10yrfiles,dtype=int)
experimentstartyears = np.zeros(experimentnum10yrfiles,dtype=int)
experimentendyears = np.zeros(experimentnum10yrfiles,dtype=int)

periodstartyear = gf.experimentstartyear
periodendyear = gf.experimentstartyear + 9
periodyearnum = periodendyear - periodstartyear + 1
for periodindex in range(experimentnum10yrfiles):
    experimentnumyears[periodindex] = periodyearnum
    experimentnummonths[periodindex] = periodyearnum * 12
    experimentnumdays[periodindex] = periodyearnum * 365
    experimentstartyears[periodindex] = periodstartyear
    experimentendyears[periodindex] = periodendyear
    periodstartyear += 10
    if (periodindex < experimentnum10yrfiles - 2):
        periodendyear += 10
    else:
        periodendyear = gf.experimentendyear
    periodyearnum = periodendyear - periodstartyear + 1

requestedstartyearname = str(sys.argv[5])
requestedstartyear = int(requestedstartyearname)
requestedstartperiod = -1
for periodindex in range(experimentnum10yrfiles):
    if (requestedstartyear == experimentstartyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[6])
requestedendyear = int(requestedendyearname)
requestedendperiod = -1
for periodindex in range(experimentnum10yrfiles):
    if (requestedendyear == experimentendyears[periodindex]):
        requestedendperiod = periodindex
if (requestedendperiod == -1):
    print("Requested End Year does not correspond to an Experiment History Period")
    sys.exit()
    
numrequestedperiods = requestedendperiod - requestedstartperiod + 1
    
generateexperimentgroupcommand = str(sys.argv[7])
submitupdateexperimentgroupcommand = str(sys.argv[8])
submitsubmissions = str(sys.argv[9])
submitqueuename = str(sys.argv[10])
submitprojectcode = str(sys.argv[11])

# Generate and Submit Update TimeSeries Files

for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
    if (experimentgroupname == experimentgrouphistoryshortnames[experimentgrouphistorylistindex]):
        experimentgrouphistoryfiletype = experimentgrouphistoryfiletypes[experimentgrouphistorylistindex]
        subprocessgeneratecommand = generateexperimentgroupcommand + " " + experimentgroupname + " " + experimentgrouphistoryfiletype + " " + experimentname + " " + requestedstartyearname + " " + requestedendyearname 
        subprocess.run(subprocessgeneratecommand.split())
        subprocessupdatecommand = submitupdateexperimentgroupcommand + " " + experimentgroupname + " " + experimentgrouphistoryfiletype + " " + experimentname + " " + requestedstartyearname + " " + requestedendyearname + " " + submitsubmissions + " " + submitqueuename + " " + submitprojectcode
        subprocess.run(subprocessupdatecommand.split())

