#! /usr/bin/env python
import sys
import os.path
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

# Function Definitions

def dimension_size(historyfile,dimensionname):
    historydimensionsize = -1
    for historydimension in historyfile.dimensions.values():
        if (historydimension.name == dimensionname):
            if (not historydimension.isunlimited()):
                historydimensionsize = historydimension.size

    return historydimensionsize
    
# Main Body

arguments = len(sys.argv) - 1

if (arguments != 9):
    print("Error: Usage updateexperimentgrouptimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablename variablefilesdir requestedstartyear requestedendyear")
    sys.exit()
else:
    print("Processing: " + str(sys.argv[1]) + " => " + str(sys.argv[2]))

experimentgroupname = str(sys.argv[1])
experimentgrouphistoryfiletype = str(sys.argv[2])
experimentgrouphistorylistfilename = str(sys.argv[3])

numexperimentgrouphistorys = gf.read_experiment_group_history_file(experimentgrouphistorylistfilename)
experimentgrouphistoryindex = gf.set_experiment_group_history_index(experimentgroupname,experimentgrouphistoryfiletype)

print("Experiment Group History Details")
print("Name: " + gf.experimentgrouphistoryname)
print("Type: " + gf.experimentgrouphistoryfiletype)

experimentname = str(sys.argv[4])
experimentlistfilename = str(sys.argv[5])

numexperiments = gf.read_experiment_file(experimentlistfilename)
experimentindex = gf.set_experiment_index(experimentname)

print("Experiment Details")
print("Name: " + gf.experimentname)
print("Source: " + gf.experimentsourcedir)
print("Output: " + gf.experimentoutputdir)
print("Start Year: " + gf.experimentstartyearname)
print("End Year: " + gf.experimentendyearname)

experimentnumperiods = gf.create_experiment_period_times()

variableupdatename = str(sys.argv[6])
variablefilesdir = str(sys.argv[7])
variablelistfilename = variablefilesdir + "/"  + experimentgroupname + "/" + experimentgroupname + "." + experimentgrouphistoryfiletype + ".variablelist.txt"

numvariables = gf.read_variable_file(variablelistfilename)

requestedstartyearname = str(sys.argv[8])
requestedstartyear = int(requestedstartyearname)
requestedstartperiod = -1
for periodindex in range(experimentnumperiods):
    if (requestedstartyear == gf.experimentperiodstartyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[9])
requestedendyear = int(requestedendyearname)
requestedendperiod = -1
for periodindex in range(experimentnumperiods):
    if (requestedendyear == gf.experimentperiodendyears[periodindex]):
        requestedendperiod = periodindex
if (requestedendperiod == -1):
    print("Requested End Year does not correspond to an Experiment History Period")
    sys.exit()
    
numrequestedperiods = requestedendperiod - requestedstartperiod + 1

# Check that source and destination directories for the experiment

experimentsourcelocation = gf.experimentsourcedir + "/" + gf.experimentname + "/" + gf.experimentgrouphistorysource
if os.path.isdir(experimentsourcelocation):
    print("Found Source: " + experimentsourcelocation)
else:
    print("Missing Source: " + experimentsourcelocation)
    sys.exit()

experimentoutputlocation = gf.experimentoutputdir + "/" + gf.experimentname + "/" + gf.experimentgrouphistoryoutput + "/" + gf.experimentgrouphistorytimetype + "/"
if os.path.isdir(experimentoutputlocation):
    print("Found Output: " + experimentoutputlocation)
else:
    print("Missing Output: " + experimentoutputlocation)
    sys.exit()

# Transfer TimeSeries Files

for requestedperiodindex in range(numrequestedperiods):
    periodindex = requestedstartperiod + requestedperiodindex
    outtimeseriesstartyear = gf.experimentperiodstartyears[periodindex]
    outtimeseriesendyear = gf.experimentperiodendyears[periodindex]
    outputupdatingname = ""
    outputfilename = ""
    if (variableupdatename == "GLOBAL"):
        outputcreatedname = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"_created")
        outputupdatingname = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"_updating")
        outputfilename = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"")
    else:
        for variablelistindex in range(numvariables):
            if (gf.variableprocesstypes[variablelistindex] == "TimeSeries" and gf.variablenames[variablelistindex] == variableupdatename):
                outputcreatedname = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"_created")
                outputupdatingname = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"_updating")
                outputfilename = gf.create_timeseries_filename(variableupdatename,outtimeseriesstartyear,outtimeseriesendyear,"")

    if os.path.isfile(outputcreatedname):
        print("Updating File: " + outputupdatingname)
        os.rename(outputcreatedname,outputupdatingname)
    else:
        print("Missing: " + outputcreatedname)
        sys.exit()
       
    outputfile = netcdf4.Dataset(outputupdatingname, "r+")

    timeindex = 0
    for yearindex in range(gf.experimentperiodnumyears[periodindex]):
        processyear = gf.experimentperiodstartyears[periodindex] + yearindex
        outputyearindex = yearindex * gf.experimentgrouphistorytimesperyear
        outputfileindex = 0
        for historyfileindex in range(gf.experimentgrouphistoryfilesperyear):
            if (gf.experimentgrouphistorytimesperfile > 0):
                historytimesperfile = gf.experimentgrouphistorytimesperfile
            else:
                historytimesperfile = gf.nummonthdays[historyfileindex]
            outputindex = outputyearindex + outputfileindex
            processmonth = gf.experimenthistoryfilemonths[historyfileindex]
            processday = gf.experimenthistoryfiledays[historyfileindex]
            processhour = gf.experimenthistoryfilehours[historyfileindex]

            experimenthistoryfilename = gf.create_history_filename(processyear,processmonth,processday,processhour)

            print("Reading: " + variableupdatename + " From: " + experimenthistoryfilename)

            experimenthistoryfile = netcdf4.Dataset(experimenthistoryfilename,'r')

            for variablelistindex in range(numvariables):

                if (gf.variableprocesstypes[variablelistindex] == "TimeIndex"):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]

                if (gf.variableprocesstypes[variablelistindex] == "TimeAll"):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]
        	
                if (gf.variableprocesstypes[variablelistindex] == "TimeGlobal" and variableupdatename == "GLOBAL"):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]
        	
                if (gf.variableprocesstypes[variablelistindex] == "FilevalueAll"):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(grouphistorytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[:]

                if (gf.variableprocesstypes[variablelistindex] == "FilevalueGlobal" and variableupdatename == "GLOBAL"):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(grouphistorytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[:]

                if (gf.variableprocesstypes[variablelistindex] == "TimeSeries" and gf.variablenames[variablelistindex] == variableupdatename):
                    readvariablename = gf.variablenames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[readvariablename]
                    writevariable = outputfile.variables[readvariablename]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]

            outputfileindex += historytimesperfile

    chunkingspecifier = "time/1"
    for variablelistindex in range(numvariables):
        if (gf.variableprocesstypes[variablelistindex] == "TimeSeries" and gf.variablenames[variablelistindex] == variableupdatename):
            writevariablename = gf.variablenames[variablelistindex]
            writevariable = outputfile.variables[writevariablename]
            if (len(writevariable.dimensions) == 2):
                dimensionname = writevariable.dimensions[1]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
            elif (len(writevariable.dimensions) == 3):
                dimensionname = writevariable.dimensions[1]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[2]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
            elif (len(writevariable.dimensions) == 4):
                dimensionname = writevariable.dimensions[1]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[2]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[3]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
            elif (len(writevariable.dimensions) == 5):
                dimensionname = writevariable.dimensions[1]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[2]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[3]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)
                dimensionname = writevariable.dimensions[4]
                dimensionsize = dimension_size(outputfile,dimensionname)
                chunkingspecifier = chunkingspecifier + "," + dimensionname + "/" + str(dimensionsize)

    outputfile.close()

    subprocessupdatecommand = "nccopy -c " + chunkingspecifier + " -s -d " + str(gf.experimentgrouphistorycompression) + " " + outputupdatingname + " " + outputfilename
    print(subprocessupdatecommand)
    subprocess.run(subprocessupdatecommand.split())
    os.remove(outputupdatingname)
    
