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

# Main Body

arguments = len(sys.argv) - 1

if (arguments != 6):
    print("Error: Usage statusexperimentgrouptimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablefilesdir")
    sys.exit()
else:
    print("Processing: " + str(sys.argv[1]) + " => " + str(sys.argv[2]) + " => " + str(sys.argv[4]))

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

variablefilesdir = str(sys.argv[6])
variablelistfilename = variablefilesdir + "/"  + experimentgroupname + "/" + experimentgroupname + "." + experimentgrouphistoryfiletype + ".variablelist.txt"

numvariables = gf.read_variable_file(variablelistfilename)

statusstartyearname = gf.experimentstartyearname
statusstartyear = gf.experimentstartyear
statusstartperiod = -1
for periodindex in range(experimentnumperiods):
    if (statusstartyear == gf.experimentperiodstartyears[periodindex]):
        statusstartperiod = periodindex
if (statusstartperiod == -1):
    print("Status Start Year does not correspond to an Experiment History Period")
    sys.exit()
statusendyearname = gf.experimentendyearname
statusendyear = gf.experimentendyear
statusendperiod = -1
for periodindex in range(experimentnumperiods):
    if (statusendyear == gf.experimentperiodendyears[periodindex]):
        statusendperiod = periodindex
if (statusendperiod == -1):
    print("Status End Year does not correspond to an Experiment History Period")
    sys.exit()

numstatusperiods = statusendperiod - statusstartperiod + 1
    
# Check that source and destination directories for the experiment

experimentsourcelocation = gf.experimentsourcedir + "/" + gf.experimentname + "/" + gf.experimentgrouphistorysource
if os.path.isdir(experimentsourcelocation):
    print("Found Source: " + experimentsourcelocation)
else:
    print("Missing Source: " + experimentsourcelocation)

experimentoutputlocation = gf.experimentoutputdir + "/" + gf.experimentname + "/" + gf.experimentgrouphistoryoutput
if os.path.isdir(experimentoutputlocation):
    print("Found Output: " + experimentoutputlocation)
else:
    print("Missing Output: " + experimentoutputlocation)
    sys.exit()

# Status TimeSeries Files

experimentstatusfileslocation = gf.experimentoutputdir + "/" + gf.experimentname + "/statusfiles/"
if not os.path.isdir(experimentstatusfileslocation):
    os.makedirs(experimentstatusfileslocation)

statusfilename = gf.create_status_filename(statusstartyear,statusendyear)
statusfile = open(statusfilename, "w")
statusfile.write("Period      -  Expected  -  Missing  -  Created  -  Updating  -  Final \n")

statusmissingvariables = []

for statusperiodindex in range(numstatusperiods):
    periodindex = statusstartperiod + statusperiodindex

    currenttimeseriesstartyear = gf.experimentperiodstartyears[periodindex]
    currenttimeseriesendyear = gf.experimentperiodendyears[periodindex]
    globalfilename = gf.create_timeseries_filename("GLOBAL",currenttimeseriesstartyear,currenttimeseriesendyear,"")

    statussearchfiles = 1
    statussearchmissingfiles = 0
    statussearchcreatedfiles = 0
    statussearchupdatingfiles = 0
    statussearchfinalfiles = 0
    if (os.path.isfile(globalfilename)):
        statussearchfinalfiles += 1

    for variablelistindex in range(numvariables):
        if (gf.variableprocesstypes[variablelistindex] == "TimeSeries"):

            variabletimeseriesname = gf.variablenames[variablelistindex]

            createdfilename = gf.create_timeseries_filename(variabletimeseriesname,currenttimeseriesstartyear,currenttimeseriesendyear,"_created")
            updatingfilename = gf.create_timeseries_filename(variabletimeseriesname,currenttimeseriesstartyear,currenttimeseriesendyear,"_updating")
            finalfilename = gf.create_timeseries_filename(variabletimeseriesname,currenttimeseriesstartyear,currenttimeseriesendyear,"")
            statussearchfiles += 1
            statusfilefound = 0
            if (os.path.isfile(createdfilename)):
                statussearchcreatedfiles += 1
                statusfilefound = 1
            if (os.path.isfile(updatingfilename)):
                statussearchupdatingfiles += 1
                statusfilefound = 1
            if (os.path.isfile(finalfilename)):
                statussearchfinalfiles += 1
                statusfilefound = 1
            if (statusfilefound == 0):
                statussearchmissingfiles += 1
                if (not variabletimeseriesname in statusmissingvariables):
                    statusmissingvariables.append(variabletimeseriesname)

    statusoutstring = str(currenttimeseriesstartyear).zfill(4) + "-" + str(currenttimeseriesendyear).zfill(4) + "   -  " + str(statussearchfiles)
    statusoutstring = statusoutstring + "        -  " + str(statussearchmissingfiles) + "        -  " + str(statussearchcreatedfiles) 
    statusoutstring = statusoutstring + "        -  " + str(statussearchupdatingfiles) + "        -  " + str(statussearchfinalfiles) + " \n"
    statusfile.write(statusoutstring)

if (len(statusmissingvariables) > 0):    
    statusfile.write("Missing Variables:\n")
    for missingvariable in statusmissingvariables:
        statusfile.write(missingvariable + "\n")

currenthistoryyear = gf.experimentperiodstartyears[0]
currenthistorymonth = gf.experimenthistoryfilemonths[0]
currenthistoryday = gf.experimenthistoryfiledays[0]
currenthistoryhour = gf.experimenthistoryfilehours[0]
templateexperimentfilename = gf.create_history_filename(currenthistoryyear,currenthistorymonth,currenthistoryday,currenthistoryhour)

statusnotprocessedvariables = []

if (os.path.isfile(templateexperimentfilename)):
    templateexperimentfile = netcdf4.Dataset(templateexperimentfilename,'r')

    for var_name, variable in templateexperimentfile.variables.items():
        variablefound = 0
        for variablelistindex in range(numvariables):
            variablelistname = gf.variablenames[variablelistindex]
            if (var_name == variablelistname):
                variablefound = 1

        if (variablefound == 0):
            if (not var_name in statusnotprocessedvariables):
                statusnotprocessedvariables.append(var_name)

if (len(statusnotprocessedvariables) > 0):    
    statusfile.write("Not Processed Variables:\n")
    for notprocessedvariable in statusnotprocessedvariables:
        statusfile.write(notprocessedvariable + "\n")

statusfile.close()
