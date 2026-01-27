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
        timedimension = outputfile.dimensions[dimension_name(readdimensions,0)]
        timedimensionchunk = len(timedimension)/12
        writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),),)
    return

#--  end of function definitions  ---------------------------------

# process the input arguments

arguments = len(sys.argv) - 1

if (arguments != 8):
    print("Error: Usage generateallexperimenttimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablelist requestedstartyear requestedendyear")
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

variablelistfilename = str(sys.argv[6])

variablelistfile = open(variablelistfilename,'r')
variablelist = variablelistfile.readlines()
numvariables = len(variablelist)
variablesnames = [""] * numvariables
variableprocesstypes = [""] * numvariables
variableframeworkcount = 0
variabletimecount = 0
variableglobalcount = 0
variabletimeseriescount = 0
for variablelistindex in range(numvariables):
    variablelistvalues = variablelist[variablelistindex].split()
    variablesnames[variablelistindex] = variablelistvalues[1]
    variableprocesstypes[variablelistindex] = variablelistvalues[4]
    if (variableprocesstypes[variablelistindex] == "Framework"):
        variableframeworkcount += 1
    if (variableprocesstypes[variablelistindex] == "Time"):
        variabletimecount += 1
    if (variableprocesstypes[variablelistindex] == "Global"):
        variableglobalcount += 1
    if (variableprocesstypes[variablelistindex] == "TimeSeries"):
        variabletimeseriescount += 1

requestedstartyearname = str(sys.argv[7])
requestedstartyear = int(requestedstartyearname)
requestedstartperiod = -1
for periodindex in range(num10yrfiles):
    if (requestedstartyear == startyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[8])
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
    print("Creating Output: " + experimentoutputlocation)
    os.makedirs(experimentoutputlocation)

# Generate Global Files

experimentfilename = experimentlocation + experimentlongname + "/" + experimentgrouphistorysource + "/" + experimentlongname + "." + experimentgrouphistoryfiletype
experimentfilename = experimentfilename + "." + str(startyears[requestedstartperiod]).zfill(4) + "-01.nc"

print("Reading File: " + experimentfilename)

experimentfile = netcdf4.Dataset(experimentfilename,'r')

for requestedperiodindex in range(numrequestedperiods):
    periodindex = requestedstartperiod + requestedperiodindex
    outputfilename = experimentoutputlocation + experimentlongname + ".cam.h0.GLOBAL." + str(startyears[periodindex]).zfill(4) + "01-" + str(endyears[periodindex]).zfill(4) + "12.nc"

    print("Writing File: " + outputfilename)

    outputfile = netcdf4.Dataset(outputfilename, "w")
    for attr_name in experimentfile.ncattrs():
        set_or_create_attr(outputfile,attr_name,getattr(experimentfile, attr_name))

    periodnummonths = nummonths[periodindex]
    outputfile.createDimension('time',int(periodnummonths))
    
    writetime = outputfile.createVariable('time',experimentfile.variables['time'].dtype,('time',))
    writetime.units = 'days since ' + str(experimentstartyear) + '-01-01 00:00:00'
    writetime.long_name = 'days since ' + str(experimentstartyear) + '-01-01 00:00:00'
    writetime.calendar = "noleap"
    writetime[:] = outtimes[periodindex][0:periodnummonths]

    for dim_name, dimension in experimentfile.dimensions.items():
        if (dim_name != "time"):
            if (dimension.isunlimited()):
                outputfile.createDimension(dim_name,size=None)
            else:
                outputfile.createDimension(dim_name,size=dimension.size)

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "Global"):

            variableaddname = variablesnames[variablelistindex]
            readvariable = experimentfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    for timeindex in range(numvariables):
        if (variableprocesstypes[timeindex] == "Time"):

            timeaddname = variablesnames[timeindex]
            readvariable = experimentfile.variables[timeaddname]
            create_variable(outputfile,timeaddname,readvariable)
            writevariable = outputfile.variables[timeaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    # Update the Global file for all time and global variables

    for yearindex in range(numyears[periodindex]):
        processyear = startyears[periodindex] + yearindex
        for monthindex in range(12):
            outputindex = yearindex * 12 + monthindex
            processmonth = monthindex + 1

            monthlyexperimentfilename = experimentlocation + experimentlongname + "/" + experimentgrouphistorysource + "/" + experimentlongname + "." + experimentgrouphistoryfiletype
            monthlyexperimentfilename = monthlyexperimentfilename + "." + str(processyear).zfill(4) + "-" + str(processmonth).zfill(2) + ".nc"

            print("Reading File: " + monthlyexperimentfilename)

            monthlyexperimentfile = netcdf4.Dataset(monthlyexperimentfilename,'r')

            for variablelistindex in range(numvariables):
                if (variableprocesstypes[variablelistindex] == "Global"):

                    variableaddname = variablesnames[variablelistindex]
                    readvariable = monthlyexperimentfile.variables[variableaddname]
                    writevariable = outputfile.variables[variableaddname]
                    if (len(writevariable.dimensions) == 1):
                        writevariable[outputindex] = readvariable[0]
                    else:
                        writevariable[outputindex,:] = readvariable[0,:]
        	
            for timeindex in range(numvariables):
                if (variableprocesstypes[timeindex] == "Time"):

                    timeaddname = variablesnames[timeindex]
                    readvariable = monthlyexperimentfile.variables[timeaddname]
                    writevariable = outputfile.variables[timeaddname]
                    if (len(writevariable.dimensions) == 1):
                        writevariable[outputindex] = readvariable[0]
                    else:
                        writevariable[outputindex,:] = readvariable[0,:]

    outputfile.close()

    globalfilename = experimentoutputlocation + experimentlongname + ".cam.h0.GLOBAL." + str(startyears[periodindex]).zfill(4) + "01-" + str(endyears[periodindex]).zfill(4) + "12.nc"
    globalfile = netcdf4.Dataset(globalfilename, "r")

    # Generate TimeSeries Files

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "TimeSeries"):

            variabletimeseriesname = variablesnames[variablelistindex]

            outputfilename = experimentoutputlocation + experimentlongname + ".cam.h0." + variabletimeseriesname + "_created." + str(startyears[periodindex]).zfill(4) + "01-" + str(endyears[periodindex]).zfill(4) + "12.nc"

            print("Writing File: " + outputfilename)
       
            outputfile = netcdf4.Dataset(outputfilename, "w")
            for attr_name in experimentfile.ncattrs():
                set_or_create_attr(outputfile,attr_name,getattr(experimentfile, attr_name))

            outputfile.createDimension('time',int(nummonths[periodindex]))
    
            writetime = outputfile.createVariable('time',experimentfile.variables['time'].dtype,('time',))
            writetime.units = 'days since ' + str(experimentstartyear) + '-01-01 00:00:00'
            writetime.long_name = 'days since ' + str(experimentstartyear) + '-01-01 00:00:00'
            writetime.calendar = "noleap"
            writetime[:] = outtimes[periodindex][0:periodnummonths]

            for dim_name, dimension in experimentfile.dimensions.items():
                if (dim_name != "time"):
                    if (dimension.isunlimited()):
                        outputfile.createDimension(dim_name,size=None)
                    else:
                        outputfile.createDimension(dim_name,size=dimension.size)

            for frameworkindex in range(numvariables):
                if (variableprocesstypes[frameworkindex] == "Framework"):

                    frameworkaddname = variablesnames[frameworkindex]
                    readvariable = experimentfile.variables[frameworkaddname]
                    readdimensions = readvariable.dimensions
                    create_variable(outputfile,frameworkaddname,readvariable)
                    writevariable = outputfile.variables[frameworkaddname]
                    for attr_name in readvariable.ncattrs():
                        set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))
                    writevariable[:] = np.asfarray(readvariable[:])

            for timeindex in range(numvariables):
                if (variableprocesstypes[timeindex] == "Time"):

                    timeaddname = variablesnames[timeindex]
                    readvariable = experimentfile.variables[timeaddname]
                    create_variable(outputfile,timeaddname,readvariable)
                    writevariable = outputfile.variables[timeaddname]
                    for attr_name in readvariable.ncattrs():
                        set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))
                    globalvariable = globalfile.variables[timeaddname]
                    writevariable[:] = np.asfarray(globalvariable[:])

            timeseriesaddname = variablesnames[variablelistindex]
            readvariable = experimentfile.variables[timeseriesaddname]
            create_variable(outputfile,timeseriesaddname,readvariable)
            writevariable = outputfile.variables[timeseriesaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            outputfile.close()

