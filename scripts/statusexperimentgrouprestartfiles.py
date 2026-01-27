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

if (arguments != 4):
    print("Error: Usage statuseexperimentgrouprestartfiles.py experimentgroup experimentgrouphistorylist experiment experimentlist")
    sys.exit()
else:
    print("Processing: " + str(sys.argv[1]) + " => " + str(sys.argv[3]))

experimentgroupname = str(sys.argv[1])
experimentgrouphistorylistfilename = str(sys.argv[2])

numexperimentgrouphistorys = gf.read_experiment_group_history_file(experimentgrouphistorylistfilename)

numexperimentgrouphistoryfiles = 0
for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
    if (experimentgroupname == gf.experimentgrouphistorynames[experimentgrouphistorylistindex]):
        numexperimentgrouphistoryfiles += 1

if (numexperimentgrouphistoryfiles == 0):
    print("Unknown Experiment Group: " + experimentgroupname)
    sys.exit()

print("Experiment Group Details")
print("Name: " + experimentgroupname)

experimentname = str(sys.argv[3])
experimentlistfilename = str(sys.argv[4])

numexperiments = gf.read_experiment_file(experimentlistfilename)
experimentindex = gf.set_experiment_index(experimentname)

print("Experiment Details")
print("Name: " + gf.experimentname)
print("Source: " + gf.experimentsourcedir)
print("Output: " + gf.experimentoutputdir)
print("Start Year: " + gf.experimentstartyearname)
print("End Year: " + gf.experimentendyearname)

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

statusfilename = gf.create_status_restart_filename(gf.experimentstartyear,gf.experimentendyear)
statusfile = open(statusfilename, "w")

statusrestartlist = []

experimentrestartfileslocation = gf.experimentoutputdir + "/" + gf.experimentname + "/rest/"
if os.path.isdir(experimentrestartfileslocation):
    statusrestartlist = os.listdir(experimentrestartfileslocation)
    statusrestartlist.sort()

if (len(statusrestartlist) > 0):    
    statusfile.write("Restart Directories in Timeseries:\n")
    for restartdirectory in statusrestartlist:
        statusfile.write(restartdirectory + "\n")
else:
    statusfile.write("NO RESTARTS Transferred:\n")

statusfile.close()
