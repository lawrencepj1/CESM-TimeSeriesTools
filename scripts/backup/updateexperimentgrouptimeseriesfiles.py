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

if (arguments != 9):
    print("Error: Usage updateexperimentgrouptimeseries10yrfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablename variablelist requestedstartyear requestedendyear")
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
experimentgrouphistorysourcedirs = [""] * numexperimentgrouphistorys
experimentgrouphistorysources = [""] * numexperimentgrouphistorys
experimentgrouphistoryoutputdirs = [""] * numexperimentgrouphistorys
experimentgrouphistoryoutputs = [""] * numexperimentgrouphistorys
experimentgrouphistorytimetypes = [""] * numexperimentgrouphistorys
experimentgrouphistoryfilesperyears = [""] * numexperimentgrouphistorys
experimentgrouphistorydaysperfiles = [""] * numexperimentgrouphistorys
experimentgrouphistorytimesperfiles = [""] * numexperimentgrouphistorys
experimentgrouphistoryindex = -1
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
    if (experimentgroupname == experimentgrouphistoryshortnames[experimentgrouphistorylistindex] and historyfiletype == experimentgrouphistoryfiletypes[experimentgrouphistorylistindex]):
        experimentgrouphistoryindex = experimentgrouphistorylistindex

if (experimentgrouphistoryindex == -1):
    print("Unknown Experiment Group History Type: " + experimentgroupname + " with " + historyfiletype)
    sys.exit()

gf.experimentgrouphistoryshortname = experimentgrouphistoryshortnames[experimentgrouphistoryindex]
gf.experimentgrouphistoryfiletype = experimentgrouphistoryfiletypes[experimentgrouphistoryindex]
gf.experimentgrouphistorysourcedir = experimentgrouphistorysourcedirs[experimentgrouphistoryindex]
gf.experimentgrouphistorysource = experimentgrouphistorysources[experimentgrouphistoryindex]
gf.experimentgrouphistoryoutputdir = experimentgrouphistoryoutputdirs[experimentgrouphistoryindex]
gf.experimentgrouphistoryoutput = experimentgrouphistoryoutputs[experimentgrouphistoryindex]
gf.experimentgrouphistorytimetype = experimentgrouphistorytimetypes[experimentgrouphistoryindex]
gf.experimentgrouphistoryfilesperyear = int(experimentgrouphistoryfilesperyears[experimentgrouphistoryindex])
gf.experimentgrouphistorydaysperfile = int(experimentgrouphistorydaysperfiles[experimentgrouphistoryindex])
gf.experimentgrouphistorytimesperfile = int(experimentgrouphistorytimesperfiles[experimentgrouphistoryindex])
if (gf.experimentgrouphistorydaysperfile > 0 and gf.experimentgrouphistorytimesperfile > 0):
    gf.experimentgrouphistorytimesperyear = gf.experimentgrouphistoryfilesperyear * gf.experimentgrouphistorytimesperfile
else:
    gf.experimentgrouphistorytimesperyear = 365

print("Experiment Group History Details")
print("Name: " + gf.experimentgrouphistoryshortname)
print("Type: " + gf.experimentgrouphistoryfiletype)
print("Source: " + gf.experimentgrouphistorysource)
print("Output: " + gf.experimentgrouphistoryoutput)

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
    experimentnumtimes[periodindex] = periodyearnum * gf.experimentgrouphistorytimesperyear
    experimentstartyears[periodindex] = periodstartyear
    experimentendyears[periodindex] = periodendyear
    periodstartyear += 10
    if (periodindex < experimentnum10yrfiles - 2):
        periodendyear += 10
    else:
        periodendyear = gf.experimentendyear
    periodyearnum = periodendyear - periodstartyear + 1

experimentgrouphistoryfilemonths = np.zeros(gf.experimentgrouphistoryfilesperyear,dtype=int)
experimentgrouphistoryfiledays = np.zeros(gf.experimentgrouphistoryfilesperyear,dtype=int)
experimentgrouphistoryfilehours = np.zeros(gf.experimentgrouphistoryfilesperyear,dtype=int)
historyfilemonth = 1
historyfileday = gf.get_first_history_day()
historyfilehour = gf.get_file_hour(historyfilemonth,historyfileday)
for historyfileindex in range(gf.experimentgrouphistoryfilesperyear):
    experimentgrouphistoryfilemonths[historyfileindex] = historyfilemonth
    experimentgrouphistoryfiledays[historyfileindex] = historyfileday
    experimentgrouphistoryfilehours[historyfileindex] = historyfilehour
    nexthistoryfilemonth = gf.get_next_month(historyfilemonth,historyfileday)
    nexthistoryfileday = gf.get_next_day(historyfilemonth,historyfileday)
    historyfilemonth = nexthistoryfilemonth
    historyfileday = nexthistoryfileday

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
for periodindex in range(experimentnum10yrfiles):
    if (requestedstartyear == experimentstartyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[9])
requestedendyear = int(requestedendyearname)
requestedendperiod = -1
for periodindex in range(experimentnum10yrfiles):
    if (requestedendyear == experimentendyears[periodindex]):
        requestedendperiod = periodindex
if (requestedendperiod == -1):
    print("Requested End Year does not correspond to an Experiment History Period")
    sys.exit()
    
numrequestedperiods = requestedendperiod - requestedstartperiod + 1

# Check that source and destination directories for the experiment

experimentsourcelocation = gf.experimentgrouphistorysourcedir + "/" + gf.experimentlongname + "/" + gf.experimentgrouphistorysource
if os.path.isdir(experimentsourcelocation):
    print("Found Source: " + experimentsourcelocation)
else:
    print("Missing Source: " + experimentsourcelocation)
    sys.exit()

experimentoutputlocation = gf.experimentgrouphistoryoutputdir + "/" + gf.experimentlongname + "/" + gf.experimentgrouphistoryoutput + "/" + gf.experimentgrouphistorytimetype + "/"
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

            outtimeseriesstartyear = experimentstartyears[periodindex]
            outtimeseriesendyear = experimentendyears[periodindex]
            outputtempname = gf.create_timeseries_filename(variabletimeseriesname,outtimeseriesstartyear,outtimeseriesendyear,"_updating")
            outputfilename = gf.create_timeseries_filename(variabletimeseriesname,outtimeseriesstartyear,outtimeseriesendyear,"")

            if os.path.isfile(outputtempname):
                print("Updating File: " + outputtempname)
            else:
                print("Missing: " + outputtempname)
                sys.exit()
       
            outputfile = netcdf4.Dataset(outputtempname, "r+")

            timeindex = 0
            for yearindex in range(experimentnumyears[periodindex]):
                processyear = experimentstartyears[periodindex] + yearindex
                outputyearindex = yearindex * gf.experimentgrouphistorytimesperyear
                outputfileindex = 0
                for historyfileindex in range(gf.experimentgrouphistoryfilesperyear):
                    if (gf.experimentgrouphistorytimesperfile > 0):
                        historytimesperfile = gf.experimentgrouphistorytimesperfile
                    else:
                        historytimesperfile = nummonthdays[historyfileindex]
                    outputindex = outputyearindex + outputfileindex
                    processmonth = experimentgrouphistoryfilemonths[historyfileindex]
                    processday = experimentgrouphistoryfiledays[historyfileindex]
                    processhour = experimentgrouphistoryfilehours[historyfileindex]

                    experimenthistoryfilename = gf.create_history_filename(processyear,processmonth,processday,processhour)

                    print("Reading: " + variabletimeseriesname + " From: " + experimenthistoryfilename)

                    experimenthistoryfile = netcdf4.Dataset(experimenthistoryfilename,'r')

                    readvariable = experimenthistoryfile.variables[variabletimeseriesname]
                    writevariable = outputfile.variables[variabletimeseriesname]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]

                    outputfileindex += historytimesperfile

            outputfile.close()
            nco.Nco().ncks(input=outputtempname, output=outputfilename, options=['-L 1'])
            os.remove(outputtempname)
