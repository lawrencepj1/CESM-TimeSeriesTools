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

if (arguments != 6):
    print("Error: Usage statusallexperimentgrouptimeseriesfiles.py experimentgroup experimentgrouphistorylist experiment experimentlist statusexperimentgroupcommand statusexperimentrestartcommand")
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

statusexperimentgroupcommand = str(sys.argv[5])

# Generate and Submit Update TimeSeries Files

for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
    if (experimentgroupname == gf.experimentgrouphistorynames[experimentgrouphistorylistindex]):
        experimentgrouphistoryfiletype = gf.experimentgrouphistoryfiletypes[experimentgrouphistorylistindex]
        subprocesscommand = statusexperimentgroupcommand + " " + experimentgroupname + " " + experimentgrouphistoryfiletype + " " + experimentname
        subprocess.run(subprocesscommand.split())

statusexperimentrestartcommand = str(sys.argv[6])

subprocesscommand = statusexperimentrestartcommand + " " + experimentgroupname + " " + experimentname
subprocess.run(subprocesscommand.split())
