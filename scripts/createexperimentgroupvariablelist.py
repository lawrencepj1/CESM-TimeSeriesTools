#! /usr/bin/env python
import sys
import os.path
import string
import subprocess
import datetime as date
import numpy as np
import netCDF4 as netcdf4
# import pandas as pd
# import xarray as xr
# import matplotlib.pyplot as plt

import gfileutils as gf

# Global Variables

# Function Definitions

def dimension_count(variable_dimensions):
    dimensionnumber = 0
    for dim_name in variable_dimensions:
        dimensionnumber += 1
    return dimensionnumber

def dimension_name(variable_dimensions,dimensionindex):
    dimensionnumber = 0
    dimensionstring = ""
    for dim_name in variable_dimensions:
        if (dimensionnumber == dimensionindex):
            dimensionstring = dim_name
        dimensionnumber += 1
    return dimensionstring

# Main Body

arguments = len(sys.argv) - 1

if (arguments != 6):
    print("Error: Usage createexperimentgroupvariablelist.py experimentgroup historyfiletype experimentgrouphistorylist templateexperiment experimentlist variablefilesdir")
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

templateexperimentname = str(sys.argv[4])
experimentlistfilename = str(sys.argv[5])

numexperiments = gf.read_experiment_file(experimentlistfilename)
experimentindex = gf.set_experiment_index(templateexperimentname)

print("Template Experiment Details")
print("Name: " + gf.experimentname)
print("Source: " + gf.experimentsourcedir)
print("Output: " + gf.experimentoutputdir)
print("Start Year: " + gf.experimentstartyearname)
print("End Year: " + gf.experimentendyearname)

experimentnumperiods = gf.create_experiment_period_times()

currenthistoryyear = gf.experimentperiodstartyears[0]
currenthistorymonth = gf.experimenthistoryfilemonths[0]
currenthistoryday = gf.experimenthistoryfiledays[0]
currenthistoryhour = gf.experimenthistoryfilehours[0]
templateexperimentfilename = gf.create_history_filename(currenthistoryyear,currenthistorymonth,currenthistoryday,currenthistoryhour)

print("Reading File: " + templateexperimentfilename)

templateexperimentfile = netcdf4.Dataset(templateexperimentfilename,'r')

variablefilesdir = str(sys.argv[6])
variablelistoutputdir = variablefilesdir + "/"  + experimentgroupname
variablelistoutputfilename = variablelistoutputdir + "/" + experimentgroupname + "." + experimentgrouphistoryfiletype + ".variablelist.txt"

if os.path.isdir(variablelistoutputdir):
    print("Found Output: " + variablelistoutputdir)
else:
    print("Creating Output: " + variablelistoutputdir)
    os.makedirs(variablelistoutputdir)

if os.path.isfile(variablelistoutputfilename):
    print("Error: " + variablelistoutputfilename + " already exists")
    sys.exit()

print("Writing File: " + variablelistoutputfilename)
variablelistoutputfile = open(variablelistoutputfilename,"w")

for var_name, variable in templateexperimentfile.variables.items():
    if (var_name == "time"):
        variablelistoutputline = f"Variable: {var_name} " + f" , Process: TimeIndex , DataType: {variable.dtype}" + f" , Dimensions: {variable.dimensions} \n"
    else:
        readdimensions = variable.dimensions
        readdimensioncount = dimension_count(readdimensions)
        foundtimedimension = 0
        for readdimensionindex in range(readdimensioncount):
            readdimensionname = dimension_name(readdimensions,readdimensionindex)
            if (readdimensionname == "time"):
                foundtimedimension = 1
        if (foundtimedimension == 1):
            variablelistoutputline = f"Variable: {var_name} " + f" , Process: TimeSeries , DataType: {variable.dtype}" + f" , Dimensions: {variable.dimensions} \n"
        else:
            variablelistoutputline = f"Variable: {var_name} " + f" , Process: FrameworkAll , DataType: {variable.dtype}" + f" , Dimensions: {variable.dimensions} \n"
    variablelistoutputfile.write(variablelistoutputline)
