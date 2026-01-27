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

if (arguments != 5):
    print("Error: Usage copyrestartsexperimentgrouptimeseriesfiles.py experimentgroup experimentgrouphistorylist experiment experimentlist restartdate")
    sys.exit()
else:
    print("Copying Restarts: " + str(sys.argv[1]) + " => " + str(sys.argv[3]))


experimentgroupname = str(sys.argv[1])
experimentgrouphistorylistfilename = str(sys.argv[2])

numexperimentgrouphistorys = gf.read_experiment_group_history_file(experimentgrouphistorylistfilename)

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

experimentsourcelocation = gf.experimentsourcedir + "/" + gf.experimentname
if os.path.isdir(experimentsourcelocation):
    print("Found Source: " + experimentsourcelocation)
else:
    print("Missing Source: " + experimentsourcelocation)
    sys.exit()

experimentoutputlocation = gf.experimentoutputdir + "/" + gf.experimentname
if os.path.isdir(experimentoutputlocation):
    print("Found Output: " + experimentoutputlocation)
else:
    print("Creating Output: " + experimentoutputlocation)
    os.makedirs(experimentoutputlocation)

# Generate and Submit Update TimeSeries Files

restartdate = str(sys.argv[5])

experimentrestartsourcelocation = gf.experimentsourcedir + "/" + gf.experimentname + "/rest"
experimentrestarttimeserieslocation = gf.experimentoutputdir + "/" + gf.experimentname + "/rest"
if (os.path.isdir(experimentrestartsourcelocation)):
    if (not os.path.isdir(experimentrestarttimeserieslocation)):
        os.makedirs(experimentrestarttimeserieslocation)
    experimentrestartsourcelocation = experimentrestartsourcelocation + "/"
    experimentrestarttimeserieslocation = experimentrestarttimeserieslocation + "/"
    statusrestartlist = os.listdir(experimentrestartsourcelocation)
    if (len(statusrestartlist) > 0):
        statusrestartlist.sort()

    for restartname in statusrestartlist:
        if (restartdate in restartname):
            restartsourcelocation = experimentrestartsourcelocation + restartname
            restarttimeserieslocation = experimentrestarttimeserieslocation + restartname
            experimentcopyrestartscommand = "cp -r " + restartsourcelocation + " " + restarttimeserieslocation
            print(experimentcopyrestartscommand)
            subprocess.run(experimentcopyrestartscommand.split())
