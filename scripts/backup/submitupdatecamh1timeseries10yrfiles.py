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

# load proper modules first, i.e.
# cgd machines
'''
module load lang/python/2.7.14

'''

#--  end of function definitions  ---------------------------------

# process the input arguments

arguments = len(sys.argv) - 1

if (arguments != 11):
    print("Error: Usage submitupdatecamh1timeseries10yrfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablelist startyear endyear updatecamh1command submissions projectcode")
    sys.exit()
else:
    print("Processing: " + str(sys.argv[1]) + " => " + str(sys.argv[2]))


experimentgroupname = str(sys.argv[1])
historyfiletype = str(sys.argv[2])
experimentgrouphistorylistfilename = str(sys.argv[3])

experimentgrouphistorylistfile = open(experimentgrouphistorylistfilename,'r')
experimentgrouphistorylist = experimentgrouphistorylistfile.readlines()
numexperimentgrouphistorys = len(experimentgrouphistorylist)
experimentgrouphistoryshortnames = [""] * numexperimentgrouphistorys
experimentgrouphistoryfiletypes = [""] * numexperimentgrouphistorys
experimentgrouphistorysources = [""] * numexperimentgrouphistorys
experimentgrouphistorytempdirs = [""] * numexperimentgrouphistorys
experimentgrouphistoryoutputs = [""] * numexperimentgrouphistorys
experimentgrouphistoryindex = -1
for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
    experimentgrouphistorylistvalues = experimentgrouphistorylist[experimentgrouphistorylistindex].split()
    experimentgrouphistoryshortnames[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[0]
    experimentgrouphistoryfiletypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[1]
    experimentgrouphistorysources[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[2]
    experimentgrouphistorytempdirs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[3]
    experimentgrouphistoryoutputs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[4]
    if (experimentgroupname == experimentgrouphistoryshortnames[experimentgrouphistorylistindex] and historyfiletype == experimentgrouphistoryfiletypes[experimentgrouphistorylistindex]):
        experimentgrouphistoryindex = experimentgrouphistorylistindex

if (experimentgrouphistoryindex == -1):
    print("Unknown Experiment Group History Type: " + experimentgroupname + " with " + historyfiletype)
    sys.exit()

experimentgrouphistoryshortname = experimentgrouphistoryshortnames[experimentgrouphistoryindex]
experimentgrouphistoryfiletype = experimentgrouphistoryfiletypes[experimentgrouphistoryindex]
experimentgrouphistorysource = experimentgrouphistorysources[experimentgrouphistoryindex]
experimentgrouphistorytempdir = experimentgrouphistorytempdirs[experimentgrouphistoryindex]
experimentgrouphistoryoutput = experimentgrouphistoryoutputs[experimentgrouphistoryindex]

print("Experiment Group History Details")
print("Name: " + experimentgrouphistoryshortname)
print("Type: " + experimentgrouphistoryfiletype)
print("Source: " + experimentgrouphistorysource)
print("Output: " + experimentgrouphistoryoutput)

experimentname = str(sys.argv[4])
experimentlistfilename = str(sys.argv[5])

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

experimentshortname = experimentshortnames[experimentindex]
experimentlocation = experimentlocations[experimentindex]
experimentlongname = experimentlongnames[experimentindex]
experimentstartyearname = experimentstartyearnames[experimentindex]
experimentstartyear = int(experimentstartyearname)
experimentendyearname = experimentendyearnames[experimentindex]
experimentendyear = int(experimentendyearname)

print("Experiment Details")
print("Name: " + experimentshortname)
print("Location: " + experimentlocation)
print("Experiment: " + experimentlongname)
print("Start Year: " + experimentstartyearname)
print("End Year: " + experimentendyearname)

numtotalyears = experimentendyear - experimentstartyear + 1
numtotalmonths = numtotalyears * 12
num10yrfiles = int(numtotalyears / 10)
numextrayears = numtotalyears - (num10yrfiles * 10)
if (numextrayears > 0):
    num10yrfiles += 1
    
numtotalyears = experimentendyear - experimentstartyear + 1
numtotalmonths = numtotalyears * 12
numtotaldays = numtotalyears * 365
num10yrfiles = int(numtotalyears / 10)
numextrayears = numtotalyears - (num10yrfiles * 10)
if (numextrayears > 0):
    num10yrfiles += 1
    
numyears = np.zeros(num10yrfiles,dtype=int)
nummonths = np.zeros(num10yrfiles,dtype=int)
numdays = np.zeros(num10yrfiles,dtype=int)
startyears = np.zeros(num10yrfiles,dtype=int)
endyears = np.zeros(num10yrfiles,dtype=int)

periodstartyear = experimentstartyear
periodendyear = experimentstartyear + 9
periodyearnum = periodendyear - periodstartyear + 1
for periodindex in range(num10yrfiles):
    numyears[periodindex] = periodyearnum
    nummonths[periodindex] = periodyearnum * 12
    numdays[periodindex] = periodyearnum * 365
    startyears[periodindex] = periodstartyear
    endyears[periodindex] = periodendyear
    periodstartyear += 10
    if (periodindex < num10yrfiles - 2):
        periodendyear += 10
    else:
        periodendyear = experimentendyear
    periodyearnum = periodendyear - periodstartyear + 1

periodnummonths = 120
periodnumdays = 3650
nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 
outtimes = np.zeros(shape=(num10yrfiles,periodnumdays),dtype=np.float64)
outtimecount = 0.0
for periodindex in range(num10yrfiles):
    for dayindex in range(periodnumdays):
        outtimes[periodindex,dayindex] = outtimecount
        outtimecount += 1.0

historyfilesperyear = 73
historyfilenumdays = 5
historyfilemonths = np.zeros(historyfilesperyear,dtype=int)
historyfiledays = np.zeros(historyfilesperyear,dtype=int)
monthcount = 1
daycount = 1
for historyfileindex in range(historyfilesperyear):
    historyfilemonths[historyfileindex] = monthcount
    historyfiledays[historyfileindex] = daycount
    if (daycount + historyfilenumdays > nummonthdays[monthcount-1]):
        daycount = daycount + historyfilenumdays - nummonthdays[monthcount-1]
        monthcount += 1
    else:
        daycount += historyfilenumdays

variablelistfilename = str(sys.argv[6])

variablelistfile = open(variablelistfilename,'r')
variablelist = variablelistfile.readlines()
numvariables = len(variablelist)
variablenames = [""] * numvariables
variableprocesstypes = [""] * numvariables
for variablelistindex in range(numvariables):
    variablelistvalues = variablelist[variablelistindex].split()
    variablenames[variablelistindex] = variablelistvalues[1]
    variableprocesstypes[variablelistindex] = variablelistvalues[4]

requestedstartyearname = str(sys.argv[7])
requestedstartyear = int(requestedstartyearname)
requestedstartperiod = -1
for periodindex in range(num10yrfiles):
    if (requestedstartyear == startyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[8])
requestedendyear = int(requestedendyearname)
requestedendperiod = -1
for periodindex in range(num10yrfiles):
    if (requestedendyear == endyears[periodindex]):
        requestedendperiod = periodindex
if (requestedendperiod == -1):
    print("Requested End Year does not correspond to an Experiment History Period")
    sys.exit()

numrequestedperiods = requestedendperiod - requestedstartperiod + 1
    
updatecamh1command = str(sys.argv[9])
totalsubmissions = int(sys.argv[10])
projectcode = str(sys.argv[11])

# Check that source and destination directories for the experiment

experimentsourcelocation = experimentlocation + experimentlongname + "/" + experimentgrouphistorysource
if os.path.isdir(experimentsourcelocation):
    print("Found Source: " + experimentsourcelocation)
else:
    print("Missing Source: " + experimentsourcelocation)
    sys.exit()

experimentoutputlocation = experimentgrouphistorytempdir + "/" + experimentlongname + "/" + experimentgrouphistoryoutput + "/"
if os.path.isdir(experimentoutputlocation):
    print("Found Output: " + experimentoutputlocation)
else:
    print("Missing Output: " + experimentoutputlocation)
    sys.exit()

# Transfer TimeSeries Files

    if (variablenames[variablelistindex] == variableupdatename and variableprocesstypes[variablelistindex] == "TimeSeries"):
        variableupdateindex = variablelistindex

submissioncount = 0
for variablelistindex in range(numvariables):
    if (variableprocesstypes[variablelistindex] == "TimeSeries"):

        variabletimeseriesname = variablenames[variablelistindex]

        periodindex = requestedstartperiod
        createdfilename = experimentoutputlocation + experimentlongname + ".cam.h1." + variabletimeseriesname + "_created." + str(startyears[periodindex]).zfill(4) + "0101-" + str(endyears[periodindex]).zfill(4) + "1231.nc"
        logfilename = experimentoutputlocation + experimentlongname + ".cam.h1." + variabletimeseriesname + "_updating." + str(startyears[periodindex]).zfill(4) + "0101-" + str(endyears[periodindex]).zfill(4) + "1231.log"
        if (os.path.isfile(createdfilename) and submissioncount < totalsubmissions):
            print("Submitting Variable: " + variabletimeseriesname)
            for requestedperiodindex in range(numrequestedperiods):
                periodindex = requestedstartperiod + requestedperiodindex
                createdfilename = experimentoutputlocation + experimentlongname + ".cam.h1." + variabletimeseriesname + "_created." + str(startyears[periodindex]).zfill(4) + "0101-" + str(endyears[periodindex]).zfill(4) + "1231.nc"
                updatingfilename = experimentoutputlocation + experimentlongname + ".cam.h1." + variabletimeseriesname + "_updating." + str(startyears[periodindex]).zfill(4) + "0101-" + str(endyears[periodindex]).zfill(4) + "1231.nc"
                os.rename(createdfilename,updatingfilename)
            subprocesscommand = "qcmd -A " + projectcode + " -l select=1:ncpus=1:mem=55GB -l walltime=10:00:00 -- " + updatecamh1command + " " + experimentgroupname + " " + experimentshortname + " " + variabletimeseriesname + " " + requestedstartyearname + " " + requestedendyearname 
            logfile = open(logfilename, "w")
            subprocess.Popen(subprocesscommand.split(),stdout=logfile)
            submissioncount += 1

if (submissioncount < totalsubmissions):
    print("All " + experimentlongname + " cam.h1 Variables Submitted for Update")
