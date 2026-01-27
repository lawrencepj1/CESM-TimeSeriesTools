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

if (arguments != 9):
    print("Error: Usage updatecamh0timeseries10yrfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablename variablelist requestedstartyear requestedendyear")
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
    
numyears = np.zeros(num10yrfiles,dtype=int)
nummonths = np.zeros(num10yrfiles,dtype=int)
startyears = np.zeros(num10yrfiles,dtype=int)
endyears = np.zeros(num10yrfiles,dtype=int)

periodstartyear = experimentstartyear
periodendyear = experimentstartyear + 9
periodyearnum = periodendyear - periodstartyear + 1
for periodindex in range(num10yrfiles):
    numyears[periodindex] = periodyearnum
    nummonths[periodindex] = periodyearnum * 12
    startyears[periodindex] = periodstartyear
    endyears[periodindex] = periodendyear
    periodstartyear += 10
    if (periodindex < num10yrfiles - 2):
        periodendyear += 10
    else:
        periodendyear = experimentendyear
    periodyearnum = periodendyear - periodstartyear + 1

periodnummonths = 120
nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 
outtimes = np.zeros(shape=(num10yrfiles,periodnummonths),dtype=np.float64)
outtimecount = 0.0
monthdaysindex = -1
for periodindex in range(num10yrfiles):
    for monthindex in range(periodnummonths):
        if (periodindex == 0 and monthindex == 0):
            outtimecount = 14
        else:
            outtimecount += nummonthdays[monthdaysindex]
        outtimes[periodindex,monthindex] = outtimecount
        if (monthdaysindex < 11):
            monthdaysindex += 1
        else:
            monthdaysindex = 0

variableupdatename = str(sys.argv[6])
variablelistfilename = str(sys.argv[7])

variablelistfile = open(variablelistfilename,'r')
variablelist = variablelistfile.readlines()
numvariables = len(variablelist)
variablenames = [""] * numvariables
variableprocesstypes = [""] * numvariables
variableupdateindex = -1
for variablelistindex in range(numvariables):
    variablelistvalues = variablelist[variablelistindex].split()
    variablenames[variablelistindex] = variablelistvalues[1]
    variableprocesstypes[variablelistindex] = variablelistvalues[4]
    if (variablenames[variablelistindex] == variableupdatename and variableprocesstypes[variablelistindex] == "TimeSeries"):
        variableupdateindex = variablelistindex

if (variableupdateindex == -1):
    print("Unknown Time Series Variable: " + variableupdatename)
    sys.exit()

requestedstartyearname = str(sys.argv[8])
requestedstartyear = int(requestedstartyearname)
requestedstartperiod = -1
for periodindex in range(num10yrfiles):
    if (requestedstartyear == startyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[9])
requestedendyear = int(requestedendyearname)
requestedendperiod = -1
for periodindex in range(num10yrfiles):
    if (requestedendyear == endyears[periodindex]):
        requestedendperiod = periodindex
if (requestedendperiod == -1):
    print("Requested End Year does not correspond to an Experiment History Period")
    sys.exit()
    
numrequestedperiods = requestedendperiod - requestedstartperiod + 1

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

for variablelistindex in range(numvariables):
    if (variableprocesstypes[variablelistindex] == "TimeSeries" and variablenames[variablelistindex] == variableupdatename):

        variabletimeseriesname = variablenames[variablelistindex]

        for requestedperiodindex in range(numrequestedperiods):
            periodindex = requestedstartperiod + requestedperiodindex

            outputtempname = experimentoutputlocation + experimentlongname + ".cam.h0." + variabletimeseriesname + "_updating." + str(startyears[periodindex]).zfill(4) + "01-" + str(endyears[periodindex]).zfill(4) + "12.nc"
            outputfilename = experimentoutputlocation + experimentlongname + ".cam.h0." + variabletimeseriesname + "." + str(startyears[periodindex]).zfill(4) + "01-" + str(endyears[periodindex]).zfill(4) + "12.nc"

            if os.path.isfile(outputtempname):
                print("Updating File: " + outputtempname)
            else:
                print("Missing: " + outputtempname)
                sys.exit()
       
            outputfile = netcdf4.Dataset(outputtempname, "r+")

            timeindex = 0
            for yearindex in range(numyears[periodindex]):
                processyear = startyears[periodindex] + yearindex
                for monthindex in range(12):
                    outputindex = yearindex * 12 + monthindex
                    processmonth = monthindex + 1

                    monthlyexperimentfilename = experimentlocation + experimentlongname + "/" + experimentgrouphistorysource + "/" + experimentlongname + "." + experimentgrouphistoryfiletype
                    monthlyexperimentfilename = monthlyexperimentfilename + "." + str(processyear).zfill(4) + "-" + str(processmonth).zfill(2) + ".nc"

                    print("Reading: " + variabletimeseriesname + " From: " + monthlyexperimentfilename)

                    monthlyexperimentfile = netcdf4.Dataset(monthlyexperimentfilename,'r')

                    readvariable = monthlyexperimentfile.variables[variabletimeseriesname]
                    writevariable = outputfile.variables[variabletimeseriesname]
                    if (len(writevariable.dimensions) == 1):
                        writevariable[outputindex] = readvariable[0]
                    else:
                        writevariable[outputindex,:] = readvariable[0,:]

            outputfile.close()
            nco.Nco().ncks(input=outputtempname, output=outputfilename, options=['-L 1'])
            os.remove(outputtempname)
