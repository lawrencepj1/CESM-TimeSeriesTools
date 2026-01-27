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

nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 

# Main Body

arguments = len(sys.argv) - 1

if (arguments != 6):
    print("Error: Usage createexperimentgroupvariablelist.py experimentgroup historyfiletype experimentgrouphistorylist templateexperiment experimentlist variablelistoutputhome")
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
gf.experimentgrouphistorytimesperyear = gf.experimentgrouphistoryfilesperyear * gf.experimentgrouphistorytimesperfile

print("Experiment Group History Details")
print("Name: " + gf.experimentgrouphistoryshortname)
print("Type: " + gf.experimentgrouphistoryfiletype)
print("Time: " + gf.experimentgrouphistorytimetype)
print("Source: " + gf.experimentgrouphistorysource)
print("Output: " + gf.experimentgrouphistoryoutput)

templateexperimentname = str(sys.argv[4])
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
    if (templateexperimentname == experimentshortnames[experimentlistindex]):
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

print("Template Experiment Details")
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
    experimentnumtimes[periodindex] = periodyearnum * gf.experimentgrouphistoryfilesperyear * gf.experimentgrouphistorytimesperfile
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

currenthistoryyear = gf.experimentstartyear
currenthistorymonth = experimentgrouphistoryfilemonths[0]
currenthistoryday = experimentgrouphistoryfiledays[0]
currenthistoryhour = experimentgrouphistoryfilehours[0]
templateexperimentfilename = gf.create_history_filename(currenthistoryyear,currenthistorymonth,currenthistoryday,currenthistoryhour)

print("Reading File: " + templateexperimentfilename)

templateexperimentfile = netcdf4.Dataset(templateexperimentfilename,'r')

variablelistoutputhome = str(sys.argv[6])
variablelistoutputfilename = variablelistoutputhome + experimentgroupname + "." + historyfiletype + ".variablelist.txt"

if os.path.isfile(variablelistoutputfilename):
    print("Error: " + variablelistoutputfilename + " already exists")
    sys.exit()

print("Writing File: " + variablelistoutputfilename)
variablelistoutputfile = open(variablelistoutputfilename,"w")

for var_name, variable in templateexperimentfile.variables.items():
    variablelistoutputline = f"Variable: {var_name} " + f" , Process: TimeSeries , DataType: {variable.dtype}" + f" , Dimensions: {variable.dimensions} \n"
    variablelistoutputfile.write(variablelistoutputline)
