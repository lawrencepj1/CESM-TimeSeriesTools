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

def set_or_create_attr(var, attr_name, attr_value):
    if attr_name in var.ncattrs(): 
        var.setncattr(attr_name, attr_value)
    else:
        var.UnusedNameAttribute = attr_value
        var.renameAttribute("UnusedNameAttribute", attr_name)
    return

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

def create_variable(outputfile,variableaddname,readvariable):
    readdimensions = readvariable.dimensions
    if (dimension_count(readdimensions) == 0):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype)
    elif (dimension_count(readvariable.dimensions) == 1):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),))
    elif (dimension_count(readvariable.dimensions) == 2):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),))
    elif (dimension_count(readvariable.dimensions) == 3):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),))
    elif (dimension_count(readvariable.dimensions) == 4):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),),)
    elif (dimension_count(readvariable.dimensions) == 5):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),dimension_name(readdimensions,4),),)
    return

def create_filevalue_variable(outputfile,variableaddname,timedimensionlen,readvariable):
    readdimensions = readvariable.dimensions
    if (dimension_count(readdimensions) == 0):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,'time')
    elif (dimension_count(readvariable.dimensions) == 1):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,('time',dimension_name(readdimensions,0),))
    elif (dimension_count(readvariable.dimensions) == 2):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,('time',dimension_name(readdimensions,0),dimension_name(readdimensions,1),))
    elif (dimension_count(readvariable.dimensions) == 3):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,('time',dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),))
    elif (dimension_count(readvariable.dimensions) == 4):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,('time',dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),),)
    elif (dimension_count(readvariable.dimensions) == 5):
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,('time',dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),dimension_name(readdimensions,4),),)
    return

#--  end of function definitions  ---------------------------------

# process the input arguments

arguments = len(sys.argv) - 1

if (arguments != 9):
    print("Error: Usage generateexperimentgrouptimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablename variablefilesdir requestedstartyear requestedendyear")
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

variablegeneratename = str(sys.argv[6])
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
    print("Creating Output: " + experimentoutputlocation)
    os.makedirs(experimentoutputlocation)

# Generate Global Files

currenthistoryyear = gf.experimentperiodstartyears[requestedstartperiod]
currenthistorymonth = gf.experimenthistoryfilemonths[0]
currenthistoryday = gf.experimenthistoryfiledays[0]
currenthistoryhour = gf.experimenthistoryfilehours[0]
firsthistoryfilename = gf.create_history_filename(currenthistoryyear,currenthistorymonth,currenthistoryday,currenthistoryhour)

print("Reading File: " + firsthistoryfilename)

firsthistoryfile = netcdf4.Dataset(firsthistoryfilename,'r')

for requestedperiodindex in range(numrequestedperiods):
    periodindex = requestedstartperiod + requestedperiodindex
    outtimeseriesstartyear = gf.experimentperiodstartyears[periodindex]
    outtimeseriesendyear = gf.experimentperiodendyears[periodindex]
    outputcreatedname = ""
    outputupdatingname = ""
    outputfilename = ""
    if (variablegeneratename == "GLOBAL"):
        outputcreatedname = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"_created")
        outputupdatingname = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"_updating")
        outputfilename = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"")
    else:
        for variablelistindex in range(numvariables):
            if (gf.variableprocesstypes[variablelistindex] == "TimeSeries" and gf.variablenames[variablelistindex] == variablegeneratename):
                for firstvariablename, firstvariable in firsthistoryfile.variables.items():
                    if (firstvariablename == variablegeneratename):
                        outputcreatedname = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"_created")
                        outputupdatingname = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"_updating")
                        outputfilename = gf.create_timeseries_filename(variablegeneratename,outtimeseriesstartyear,outtimeseriesendyear,"")

    if (outputcreatedname == ""):
        print("Variable Not Found on History File: " + variablegeneratename)
        sys.exit()

    if os.path.isfile(outputcreatedname):
        print("Warning Overwriting Created File: " + outputcreatedname)
        os.remove(outputcreatedname)

    if os.path.isfile(outputupdatingname):
        print("Warning Overwriting Updating File: " + outputupdatingname)
        os.remove(outputupdatingname)

    if os.path.isfile(outputfilename):
        print("Warning Overwriting Final File: " + outputupdatingname)
        os.remove(outputfilename)

    print("Writing File: " + outputcreatedname)

    outputfile = netcdf4.Dataset(outputcreatedname, "w")
    for attr_name in firsthistoryfile.ncattrs():
        set_or_create_attr(outputfile,attr_name,getattr(firsthistoryfile, attr_name))

    periodnumtimes = gf.experimentperiodnumtimes[periodindex]
    
    for firstdimension in firsthistoryfile.dimensions.values():
        if (firstdimension.name == "time"):
            outputfile.createDimension("time",int(periodnumtimes))
        else:
            if (firstdimension.isunlimited()):
                outputfile.createDimension(firstdimension.name,size=None)
            else:
                outputfile.createDimension(firstdimension.name,size=firstdimension.size)

    for variablelistindex in range(numvariables):

        if (gf.variableprocesstypes[variablelistindex] == "TimeIndex"):

            timeaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[timeaddname]
            create_variable(outputfile,timeaddname,readvariable)
            writevariable = outputfile.variables[timeaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

        if (gf.variableprocesstypes[variablelistindex] == "TimeAll"):

            timeaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[timeaddname]
            create_variable(outputfile,timeaddname,readvariable)
            writevariable = outputfile.variables[timeaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

        if (gf.variableprocesstypes[variablelistindex] == "TimeGlobal" and variablegeneratename == "GLOBAL"):

            variableaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

        if (gf.variableprocesstypes[variablelistindex] == "FrameworkAll"):

            variableaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            writevariable[:] = readvariable[:]

        if (gf.variableprocesstypes[variablelistindex] == "FrameworkGlobal" and variablegeneratename == "GLOBAL"):

            variableaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            writevariable[:] = readvariable[:]

        if (gf.variableprocesstypes[variablelistindex] == "FilevalueAll"):

            variableaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_filevalue_variable(outputfile,variableaddname,periodnumtimes,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

        if (gf.variableprocesstypes[variablelistindex] == "FilevalueGlobal" and variablegeneratename == "GLOBAL"):

            variableaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_filevalue_variable(outputfile,variableaddname,periodnumtimes,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

        if (gf.variableprocesstypes[variablelistindex] == "TimeSeries" and variablegeneratename == gf.variablenames[variablelistindex]):
            timeseriesaddname = gf.variablenames[variablelistindex]
            readvariable = firsthistoryfile.variables[timeseriesaddname]
            create_variable(outputfile,timeseriesaddname,readvariable)
            writevariable = outputfile.variables[timeseriesaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    outputfile.close()
