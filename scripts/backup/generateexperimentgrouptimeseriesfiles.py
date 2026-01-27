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
        timedimensionlen = len(outputfile.dimensions[dimension_name(readdimensions,0)])
        if (timedimensionlen < 365):
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),))
        else:
            dimension0len = 365
            dimension1len = len(outputfile.dimensions[dimension_name(readdimensions,1)])
            dimension2len = len(outputfile.dimensions[dimension_name(readdimensions,2)])
            writechunks = (dimension0len,dimension1len,dimension2len)
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),),chunksizes=writechunks)
    elif (dimension_count(readvariable.dimensions) == 4):
        timedimensionlen = len(outputfile.dimensions[dimension_name(readdimensions,0)])
        if (timedimensionlen < 365):
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),),)
        else:
            dimension0len = 365
            dimension1len = len(outputfile.dimensions[dimension_name(readdimensions,1)])
            dimension2len = len(outputfile.dimensions[dimension_name(readdimensions,2)])
            dimension3len = len(outputfile.dimensions[dimension_name(readdimensions,3)])
            writechunks = (dimension0len,dimension1len,dimension2len,dimension3len)
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),),chunksizes=writechunks,)
    elif (dimension_count(readvariable.dimensions) == 5):
        timedimensionlen = len(outputfile.dimensions[dimension_name(readdimensions,0)])
        if (timedimensionlen < 365):
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),dimension_name(readdimensions,4),),)
        else:
            dimension0len = 365
            dimension1len = len(outputfile.dimensions[dimension_name(readdimensions,1)])
            dimension2len = len(outputfile.dimensions[dimension_name(readdimensions,2)])
            dimension3len = len(outputfile.dimensions[dimension_name(readdimensions,3)])
            dimension4len = len(outputfile.dimensions[dimension_name(readdimensions,4)])
            writechunks = (dimension0len,dimension1len,dimension2len,dimension3len,dimension4len)
            writevariable = outputfile.createVariable(variableaddname,readvariable.dtype,(dimension_name(readdimensions,0),dimension_name(readdimensions,1),dimension_name(readdimensions,2),dimension_name(readdimensions,3),dimension_name(readdimensions,4),),chunksizes=writechunks,)
    return

def create_filevalue_variable(outputfile,variableaddname,readvariable):
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

if (arguments != 8):
    print("Error: Usage generateexperimentgrouptimeseriesfiles.py experimentgroup historyfiletype experimentgrouphistorylist experiment experimentlist variablelist requestedstartyear requestedendyear")
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

gf.create_history_output_times(experimentnum10yrfiles)

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
for periodindex in range(experimentnum10yrfiles):
    if (requestedstartyear == experimentstartyears[periodindex]):
        requestedstartperiod = periodindex
if (requestedstartperiod == -1):
    print("Requested Start Year does not correspond to an Experiment History Period")
    sys.exit()
requestedendyearname = str(sys.argv[8])
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
    print("Creating Output: " + experimentoutputlocation)
    os.makedirs(experimentoutputlocation)

# Generate Global Files

currenthistoryyear = experimentstartyears[requestedstartperiod]
currenthistorymonth = experimentgrouphistoryfilemonths[0]
currenthistoryday = experimentgrouphistoryfiledays[0]
currenthistoryhour = experimentgrouphistoryfilehours[0]
firsthistoryfilename = gf.create_history_filename(currenthistoryyear,currenthistorymonth,currenthistoryday,currenthistoryhour)

print("Reading File: " + firsthistoryfilename)

firsthistoryfile = netcdf4.Dataset(firsthistoryfilename,'r')

for requestedperiodindex in range(numrequestedperiods):
    periodindex = requestedstartperiod + requestedperiodindex

    currenttimeseriesstartyear = experimentstartyears[periodindex]
    currenttimeseriesendyear = experimentendyears[periodindex]
    outputfilename = gf.create_timeseries_filename("GLOBAL",currenttimeseriesstartyear,currenttimeseriesendyear,"")

    print("Writing File: " + outputfilename)

    outputfile = netcdf4.Dataset(outputfilename, "w")
    for attr_name in firsthistoryfile.ncattrs():
        set_or_create_attr(outputfile,attr_name,getattr(firsthistoryfile, attr_name))

    periodnumtimes = experimentnumtimes[periodindex]
    outputfile.createDimension('time',int(periodnumtimes))
    
    writetime = outputfile.createVariable('time',firsthistoryfile.variables['time'].dtype,('time',))
    writetime.units = 'days since ' + str(gf.experimentstartyear) + '-01-01 00:00:00'
    writetime.long_name = 'days since ' + str(gf.experimentstartyear) + '-01-01 00:00:00'
    writetime.calendar = "noleap"
    writetime[:] = gf.experimentgroupoutputtimes[periodindex][0:periodnumtimes]

    for dim_name, dimension in firsthistoryfile.dimensions.items():
        if (dim_name != "time"):
            if (dimension.isunlimited()):
                outputfile.createDimension(dim_name,size=None)
            else:
                outputfile.createDimension(dim_name,size=dimension.size)

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "TimeAll"):

            timeaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[timeaddname]
            create_variable(outputfile,timeaddname,readvariable)
            writevariable = outputfile.variables[timeaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "TimeGlobal"):

            variableaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "FrameworkAll"):

            variableaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            writevariable[:] = readvariable[:]

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "FrameworkGlobal"):

            variableaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            writevariable[:] = readvariable[:]

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "FilevalueGlobal"):

            variableaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[variableaddname]
            create_filevalue_variable(outputfile,variableaddname,readvariable)
            writevariable = outputfile.variables[variableaddname]

            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

    # Update the Global file for all time and global variables

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

            print("Reading File: " + experimenthistoryfilename)

            experimenthistoryfile = netcdf4.Dataset(experimenthistoryfilename,'r')

            for variablelistindex in range(numvariables):
                if (variableprocesstypes[variablelistindex] == "TimeGlobal"):

                    variableaddname = variablesnames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[variableaddname]
                    writevariable = outputfile.variables[variableaddname]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]
        	
            for timeindex in range(numvariables):
                if (variableprocesstypes[timeindex] == "TimeAll"):

                    timeaddname = variablesnames[timeindex]
                    readvariable = experimenthistoryfile.variables[timeaddname]
                    writevariable = outputfile.variables[timeaddname]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable[historytimeindex]
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[historytimeindex,:]

            for variablelistindex in range(numvariables):
                if (variableprocesstypes[variablelistindex] == "FilevalueGlobal"):

                    variableaddname = variablesnames[variablelistindex]
                    readvariable = experimenthistoryfile.variables[variableaddname]
                    writevariable = outputfile.variables[variableaddname]
                    if (len(writevariable.dimensions) == 1):
                        for historytimeindex in range(grouphistorytimesperfile):
                            writevariable[outputindex+historytimeindex] = readvariable
                    else:
                        for historytimeindex in range(historytimesperfile):
                            writevariable[outputindex+historytimeindex,:] = readvariable[:]

            outputfileindex += historytimesperfile

    outputfile.close()

    globalfilename = gf.create_timeseries_filename("GLOBAL",currenttimeseriesstartyear,currenttimeseriesendyear,"")
    globalfile = netcdf4.Dataset(globalfilename, "r")
    globaltimevalues = np.asfarray(globalfile.variables['time'][:])

    # Generate TimeSeries Files

    for variablelistindex in range(numvariables):
        if (variableprocesstypes[variablelistindex] == "TimeSeries"):

            variabletimeseriesname = variablesnames[variablelistindex]

            outtimeseriesstartyear = experimentstartyears[periodindex]
            outtimeseriesendyear = experimentendyears[periodindex]
            outputfilename = gf.create_timeseries_filename(variabletimeseriesname,outtimeseriesstartyear,outtimeseriesendyear,"_created")

            print("Writing File: " + outputfilename)
       
            outputfile = netcdf4.Dataset(outputfilename, "w")
            for attr_name in globalfile.ncattrs():
                set_or_create_attr(outputfile,attr_name,getattr(globalfile, attr_name))

            periodnumtimes = experimentnumtimes[periodindex]
            outputfile.createDimension('time',int(periodnumtimes))
    
            writetime = outputfile.createVariable('time',globalfile.variables['time'].dtype,('time',))
            writetime.units = 'days since ' + str(gf.experimentstartyear) + '-01-01 00:00:00'
            writetime.long_name = 'days since ' + str(gf.experimentstartyear) + '-01-01 00:00:00'
            writetime.calendar = "noleap"
            writetime[:] = globaltimevalues[:]

            for dim_name, dimension in globalfile.dimensions.items():
                if (dim_name != "time"):
                    if (dimension.isunlimited()):
                        outputfile.createDimension(dim_name,size=None)
                    else:
                        outputfile.createDimension(dim_name,size=dimension.size)

            for frameworkindex in range(numvariables):
                if (variableprocesstypes[frameworkindex] == "FrameworkAll"):

                    frameworkaddname = variablesnames[frameworkindex]
                    readvariable = globalfile.variables[frameworkaddname]
                    readdimensions = readvariable.dimensions
                    create_variable(outputfile,frameworkaddname,readvariable)
                    writevariable = outputfile.variables[frameworkaddname]
                    for attr_name in readvariable.ncattrs():
                        set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))
                    writevariable[:] = np.asfarray(readvariable[:])

            for timeindex in range(numvariables):
                if (variableprocesstypes[timeindex] == "TimeAll"):

                    timeaddname = variablesnames[timeindex]
                    readvariable = globalfile.variables[timeaddname]
                    create_variable(outputfile,timeaddname,readvariable)
                    writevariable = outputfile.variables[timeaddname]
                    for attr_name in readvariable.ncattrs():
                        set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))
                    globalvariable = globalfile.variables[timeaddname]
                    writevariable[:] = np.asfarray(globalvariable[:])

            timeseriesaddname = variablesnames[variablelistindex]
            readvariable = firsthistoryfile.variables[timeseriesaddname]
            create_variable(outputfile,timeseriesaddname,readvariable)
            writevariable = outputfile.variables[timeseriesaddname]
            for attr_name in readvariable.ncattrs():
                set_or_create_attr(writevariable,attr_name,getattr(readvariable, attr_name))

            outputfile.close()

