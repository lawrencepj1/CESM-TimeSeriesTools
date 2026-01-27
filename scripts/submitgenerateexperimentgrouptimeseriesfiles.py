#! /usr/bin/env python
import sys
import os.path
import string
import subprocess
import datetime as date
# import numpy as np
# import pandas as pd
# import netCDF4 as netcdf4
# import xarray as xr
# import matplotlib.pyplot as plt

import gfileutils as gf

# Global Variables

# Function Definitions

# Main Body

arguments = len(sys.argv) - 1

if (arguments != 13):
    print("Error: Usage submitupdateexperimentgrouptimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablename variablefilesdir startyear endyear generateexperimentgroupcommand updateexperimentgroupcommand queuename projectcode")
    sys.exit()

experimentgroupname = str(sys.argv[1])
experimentgrouphistoryfiletype = str(sys.argv[2])
experimentgrouphistorylistfilename = str(sys.argv[3])

numexperimentgrouphistorys = gf.read_experiment_group_history_file(experimentgrouphistorylistfilename)
experimentgrouphistoryindex = gf.set_experiment_group_history_index(experimentgroupname,experimentgrouphistoryfiletype)

experimentname = str(sys.argv[4])
experimentlistfilename = str(sys.argv[5])

numexperiments = gf.read_experiment_file(experimentlistfilename)
experimentindex = gf.set_experiment_index(experimentname)

experimentnumperiods = gf.create_experiment_period_times()

variablesubmitname = str(sys.argv[6])
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
    
generateexperimentgroupcommand = str(sys.argv[10])
updateexperimentgroupcommand = str(sys.argv[11])
submitqueuename = str(sys.argv[12])
submitprojectcode = str(sys.argv[13])

# Check that source and destination directories for the experiment

experimentsourcelocation = gf.experimentsourcedir + "/" + gf.experimentname + "/" + gf.experimentgrouphistorysource
if not os.path.isdir(experimentsourcelocation):
    print("Missing Source: " + experimentsourcelocation)
    sys.exit()

experimentoutputlocation = gf.experimentoutputdir + "/" + gf.experimentname + "/" + gf.experimentgrouphistoryoutput + "/" + gf.experimentgrouphistorytimetype + "/"
if not os.path.isdir(experimentoutputlocation):
    os.makedirs(experimentoutputlocation)

experimentlogfileslocation = gf.experimentoutputdir + "/" + gf.experimentname + "/" + gf.experimentgrouphistoryoutput + "/logfiles/"
if not os.path.isdir(experimentlogfileslocation):
    os.makedirs(experimentlogfileslocation)

experimentsubmissionfileslocation = gf.experimentoutputdir + "/" + gf.experimentname + "/" + gf.experimentgrouphistoryoutput + "/submissionfiles/"
if not os.path.isdir(experimentsubmissionfileslocation):
    os.makedirs(experimentsubmissionfileslocation)

# Submit Update TimeSeries Files

for variablelistindex in range(numvariables+1):
    processvariable = 0
    if (variablelistindex == 0):
        if (variablesubmitname == "GLOBAL"):
            processvariable = 1
    else: 
        if (gf.variableprocesstypes[variablelistindex-1] == "TimeSeries" and gf.variablenames[variablelistindex-1] == variablesubmitname):
            processvariable = 1

    if (processvariable == 1):

        if (variablelistindex == 0):
            variabletimeseriesname = "GLOBAL"
        else:
            variabletimeseriesname = gf.variablenames[variablelistindex-1]

        totalsubmissions = 0
        if (gf.experimentgrouphistorysubmittype == "B"):
            totalsubmissions = 1
        if (gf.experimentgrouphistorysubmittype == "S"):
            totalsubmissions = numrequestedperiods

        for submissionindex in range(totalsubmissions):
            if (gf.experimentgrouphistorysubmittype == "B"):
                submissionstartperiodindex = requestedstartperiod
                submissionendperiodindex = requestedendperiod
            if (gf.experimentgrouphistorysubmittype == "S"):
                submissionstartperiodindex = requestedstartperiod + submissionindex
                submissionendperiodindex = submissionstartperiodindex
            submissionstartyear = gf.experimentperiodstartyears[submissionstartperiodindex]
            submissionendyear = gf.experimentperiodendyears[submissionendperiodindex]
            submissionstartyearname = str(submissionstartyear)
            submissionendyearname = str(submissionendyear)
            print("Submitting Variable: " + experimentname + " : " + experimentgroupname + " : " + experimentgrouphistoryfiletype + " : " + variabletimeseriesname + " : " + submissionstartyearname + " - " + submissionendyearname)
            submissionfilename = gf.create_submission_filename(variabletimeseriesname,submissionstartyear,submissionendyear)
            logfilename = gf.create_log_filename(variabletimeseriesname,submissionstartyear,submissionendyear)
            submissionfile = open(submissionfilename, "w")
            submissionfile.write("#!/bin/bash \n")
            submissionfile.write("#PBS -N updating_" + variabletimeseriesname + " \n")
            submissionfile.write("#PBS -A " + submitprojectcode + " \n")
            submissionfile.write("#PBS -j oe \n")
            submissionfile.write("#PBS -o " + logfilename + " \n")
            submissionfile.write("#PBS -e " + logfilename + " \n")
            submissionfile.write("#PBS -q " + submitqueuename + " \n")
            submissionfile.write("#PBS -l walltime=06:00:00 \n")
            submissionfile.write("#PBS -l select=1:ncpus=1:mem=55GB \n")
            submissionfile.write(" \n")
            submissionfile.write("module load conda \n")
            submissionfile.write("conda activate npl \n")
            submissionfile.write(" \n")
            submissionfile.write(generateexperimentgroupcommand + " " + experimentgroupname + " " + experimentgrouphistoryfiletype + " " + variabletimeseriesname + " " + experimentname + " " + submissionstartyearname + " " + submissionendyearname + " \n")
            submissionfile.write(updateexperimentgroupcommand + " " + experimentgroupname + " " + experimentgrouphistoryfiletype + " " + variabletimeseriesname + " " + experimentname + " " + submissionstartyearname + " " + submissionendyearname + " \n")
            submissionfile.close()
            subprocesscommand = "qsub " + submissionfilename
            subprocess.run(subprocesscommand.split())
