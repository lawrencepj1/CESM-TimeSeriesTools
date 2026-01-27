#! /usr/bin/env python
import sys
import os.path
import numpy as np

# Global Variables

nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 

experimentname = ""
experimentsourcedir = ""
experimentoutputdir = ""
experimentstartyearname = ""
experimentstartyear = -1
experimentendyearname = ""
experimentendyear = -1

experimentnames = [""]
experimentsourcedirs = [""]
experimentoutputdirs = [""]
experimentstartyearnames = [""]
experimentendyearnames = [""]
experimentindex = -1
numexperiments = -1

experimentnumyears = np.zeros(shape=(0),dtype=int)
experimentnummonths = np.zeros(shape=(0),dtype=int)
experimentnumdays = np.zeros(shape=(0),dtype=int)
experimentnumtimes = np.zeros(shape=(0),dtype=int)

experimentperiodnumyears = np.zeros(shape=(0),dtype=int)
experimentperiodnummonths = np.zeros(shape=(0),dtype=int)
experimentperiodnumdays = np.zeros(shape=(0),dtype=int)
experimentperiodnumtimes = np.zeros(shape=(0),dtype=int)
experimentperiodstartyears = np.zeros(shape=(0),dtype=int)
experimentperiodendyears = np.zeros(shape=(0),dtype=int)
experimenthistoryfilemonths = np.zeros(shape=(0),dtype=int)
experimenthistoryfiledays = np.zeros(shape=(0),dtype=int)
experimenthistoryfilehours = np.zeros(shape=(0),dtype=int)
experimentperiodoutputtimes = np.zeros(shape=(0,0),dtype=np.float64)
experimentnumperiods = -1
experimentnumperiodtimes = -1

experimentgrouphistoryname = ""
experimentgrouphistoryfiletype = ""
experimentgrouphistorysource = ""
experimentgrouphistoryoutput = ""
experimentgrouphistorytimetype = ""
experimentgrouphistoryfilesperyear = -1
experimentgrouphistorydaysperfile = -1
experimentgrouphistorytimesperfile = -1
experimentgrouphistorytimesperyear = -1
experimentgrouphistorysubmittype = ""
experimentgrouphistorycompression = -1

experimentgrouphistorynames = [""]
experimentgrouphistoryfiletypes = [""]
experimentgrouphistorysources = [""]
experimentgrouphistoryoutputs = [""]
experimentgrouphistorytimetypes = [""]
experimentgrouphistoryfilesperyears = [""]
experimentgrouphistorydaysperfiles = [""]
experimentgrouphistorytimesperfiles = [""]
experimentgrouphistorysubmittypes = [""]
experimentgrouphistorycompressions = [""]
experimentgrouphistoryindex = -1
numexperimentgrouphistorys = -1

variablenames = [""]
variableprocesstypes = [""]
numvariables = -1

# Function Definitions

def read_experiment_file(experimentlistfilename):

    global numexperiments
    global experimentnames
    global experimentsourcedirs
    global experimentoutputdirs
    global experimentstartyearnames
    global experimentendyearnames

    if (not os.path.isfile(experimentlistfilename)):
        print("Unknown Experiment List: " + experimentlistfilename)
        sys.exit()

    experimentlistfile = open(experimentlistfilename,'r')
    experimentlist = experimentlistfile.readlines()
    numexperiments = len(experimentlist)
    experimentnames = [""] * numexperiments
    experimentsourcedirs = [""] * numexperiments
    experimentoutputdirs = [""] * numexperiments
    experimentstartyearnames = [""] * numexperiments
    experimentendyearnames = [""] * numexperiments
    for experimentlistindex in range(numexperiments):
        experimentlistvalues = experimentlist[experimentlistindex].split()
        experimentnames[experimentlistindex] = experimentlistvalues[0]
        experimentsourcedirs[experimentlistindex] = experimentlistvalues[1]
        experimentoutputdirs[experimentlistindex] = experimentlistvalues[2]
        experimentstartyearnames[experimentlistindex] = experimentlistvalues[3]
        experimentendyearnames[experimentlistindex] = experimentlistvalues[4]

    return numexperiments

def set_experiment_index(experimentsetname):

    global experimentindex
    global experimentname
    global experimentsourcedir
    global experimentoutputdir
    global experimentstartyearname
    global experimentstartyear
    global experimentendyearname
    global experimentendyear
    
    experimentindex = -1
    for experimentlistindex in range(numexperiments):
        if (experimentsetname == experimentnames[experimentlistindex]):
            experimentindex = experimentlistindex

    if (experimentindex == -1):
        print("Unknown Experiment: " + experimentsetname)
        sys.exit()

    experimentname = experimentnames[experimentindex]
    experimentsourcedir = experimentsourcedirs[experimentindex]
    experimentoutputdir = experimentoutputdirs[experimentindex]
    experimentstartyearname = experimentstartyearnames[experimentindex]
    experimentstartyear = int(experimentstartyearname)
    experimentendyearname = experimentendyearnames[experimentindex]
    experimentendyear = int(experimentendyearname)

    return experimentindex

def read_experiment_group_history_file(experimentgrouphistorylistfilename):

    global numexperimentgrouphistorys
    global experimentgrouphistorynames
    global experimentgrouphistoryfiletypes
    global experimentgrouphistorysources
    global experimentgrouphistoryoutputs
    global experimentgrouphistorytimetypes
    global experimentgrouphistoryfilesperyears
    global experimentgrouphistorydaysperfiles
    global experimentgrouphistorytimesperfiles
    global experimentgrouphistorysubmittypes
    global experimentgrouphistorycompressions

    if (not os.path.isfile(experimentgrouphistorylistfilename)):
        print("Unknown Experiment Group History List: " + experimentgrouphistorylistfilename)
        sys.exit()

    experimentgrouphistorylistfile = open(experimentgrouphistorylistfilename,'r')
    experimentgrouphistorylist = experimentgrouphistorylistfile.readlines()
    numexperimentgrouphistorys = len(experimentgrouphistorylist)
    experimentgrouphistorynames = [""] * numexperimentgrouphistorys
    experimentgrouphistoryfiletypes = [""] * numexperimentgrouphistorys
    experimentgrouphistorytimetypes = [""] * numexperimentgrouphistorys
    experimentgrouphistorysources = [""] * numexperimentgrouphistorys
    experimentgrouphistoryoutputs = [""] * numexperimentgrouphistorys
    experimentgrouphistoryfilesperyears = [""] * numexperimentgrouphistorys
    experimentgrouphistorydaysperfiles = [""] * numexperimentgrouphistorys
    experimentgrouphistorytimesperfiles = [""] * numexperimentgrouphistorys
    experimentgrouphistorysubmittypes = [""] * numexperimentgrouphistorys
    experimentgrouphistorycompressions = [""] * numexperimentgrouphistorys
    for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
        experimentgrouphistorylistvalues = experimentgrouphistorylist[experimentgrouphistorylistindex].split()
        experimentgrouphistorynames[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[0]
        experimentgrouphistoryfiletypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[1]
        experimentgrouphistorysources[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[2]
        experimentgrouphistoryoutputs[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[3]
        experimentgrouphistorytimetypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[4]
        experimentgrouphistoryfilesperyears[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[5]
        experimentgrouphistorydaysperfiles[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[6]
        experimentgrouphistorytimesperfiles[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[7]
        experimentgrouphistorysubmittypes[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[8]
        experimentgrouphistorycompressions[experimentgrouphistorylistindex] = experimentgrouphistorylistvalues[9]

    return numexperimentgrouphistorys

def set_experiment_group_history_index(experimentgroupsetname,historyfilesettype):

    global experimentgrouphistoryindex
    global experimentgrouphistoryname
    global experimentgrouphistoryfiletype
    global experimentgrouphistorysource
    global experimentgrouphistoryoutput
    global experimentgrouphistorytimetype
    global experimentgrouphistoryfilesperyear
    global experimentgrouphistorydaysperfile
    global experimentgrouphistorytimesperfile
    global experimentgrouphistorytimesperyear
    global experimentgrouphistorysubmittype
    global experimentgrouphistorycompression

    experimentgrouphistoryindex = -1
    for experimentgrouphistorylistindex in range(numexperimentgrouphistorys):
        if (experimentgroupsetname == experimentgrouphistorynames[experimentgrouphistorylistindex] and historyfilesettype == experimentgrouphistoryfiletypes[experimentgrouphistorylistindex]):
            experimentgrouphistoryindex = experimentgrouphistorylistindex

    if (experimentgrouphistoryindex == -1):
        print("Unknown Experiment Group History Type: " + experimentgroupsetname + " with " + historyfilesettype)
        sys.exit()

    experimentgrouphistoryname = experimentgrouphistorynames[experimentgrouphistoryindex]
    experimentgrouphistoryfiletype = experimentgrouphistoryfiletypes[experimentgrouphistoryindex]
    experimentgrouphistorysource = experimentgrouphistorysources[experimentgrouphistoryindex]
    experimentgrouphistoryoutput = experimentgrouphistoryoutputs[experimentgrouphistoryindex]
    experimentgrouphistorytimetype = experimentgrouphistorytimetypes[experimentgrouphistoryindex]
    experimentgrouphistoryfilesperyear = int(experimentgrouphistoryfilesperyears[experimentgrouphistoryindex])
    experimentgrouphistorydaysperfile = int(experimentgrouphistorydaysperfiles[experimentgrouphistoryindex])
    experimentgrouphistorytimesperfile = int(experimentgrouphistorytimesperfiles[experimentgrouphistoryindex])
    if (experimentgrouphistorydaysperfile > 0 and experimentgrouphistorytimesperfile > 0):
        experimentgrouphistorytimesperyear = experimentgrouphistoryfilesperyear * experimentgrouphistorytimesperfile
    else:
        experimentgrouphistorytimesperyear = 365
    experimentgrouphistorysubmittype = experimentgrouphistorysubmittypes[experimentgrouphistoryindex]
    experimentgrouphistorycompression = int(experimentgrouphistorycompressions[experimentgrouphistoryindex])

    return experimentgrouphistoryindex

def get_first_history_day():
    firstday = 1
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_5"):
        firstday = 5
    return firstday

def get_file_month(inmonth,inday):
    currentmonth = -1
    if (experimentgrouphistorytimetype == "year_1"):
        currentmonth = 1
    elif (experimentgrouphistorytimetype == "day_365"):
        currentmonth = 1
    elif (experimentgrouphistorytimetype == "month_1"):
        currentmonth = inmonth
    elif (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        currentmonth = inmonth
    elif (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        currentmonth = inmonth
    else:
        currentmonth = inmonth
    return currentmonth
    
def get_next_month(inmonth,inday):
    nextmonth = -1
    if (experimentgrouphistorytimetype == "year_1"):
        nextmonth = 1
    elif (experimentgrouphistorytimetype == "day_365"):
        nextmonth = 1
    elif (experimentgrouphistorytimetype == "month_1"):
        nextmonth = inmonth + 1
    elif (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        nextmonth = inmonth + 1
    elif (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        nextmonth = inmonth + 1
    else:
        if (inday + experimentgrouphistorydaysperfile > nummonthdays[inmonth-1]):
            nextmonth = inmonth + 1
        else:
            nextmonth = inmonth
    return nextmonth

def get_file_day(inmonth,inday):
    currentday = -1
    if (experimentgrouphistorytimetype == "year_1"):
        currentday = 1
    elif (experimentgrouphistorytimetype == "day_365"):
        currentday = 1
    elif (experimentgrouphistorytimetype == "month_1"):
        currentday = 1
    elif (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        currentday = 1
    elif (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        currentday = 1
    else:
        currentday = inday
    return currentday

def get_next_day(inmonth,inday):
    nextday = -1
    if (experimentgrouphistorytimetype == "year_1"):
        nextday = 1
    elif (experimentgrouphistorytimetype == "day_365"):
        nextday = 1
    elif (experimentgrouphistorytimetype == "month_1"):
        nextday = 1
    elif (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        nextday = 1
    elif (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        nextday = 1
    else:
        if (inday + experimentgrouphistorydaysperfile > nummonthdays[inmonth-1]):
            nextday = inday + experimentgrouphistorydaysperfile - nummonthdays[inmonth-1]
        else:
            nextday = inday + experimentgrouphistorydaysperfile
    return nextday

def get_file_hour(inmonth,inday):
    currenthour = -1
    if (experimentgrouphistorytimetype == "year_1"):
        currenthour = 0
    elif (experimentgrouphistorytimetype == "day_365"):
        currenthour = 0
    elif (experimentgrouphistorytimetype == "month_1"):
        currenthour = 0
    elif (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        currenthour = 0
    elif (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        currenthour = 0
    else:
        currenthour = 0
        if (experimentgrouphistoryfiletype == "mosart.h1" and experimentgrouphistorytimetype == "hour_3"):
            currenthour = 10800
    return currenthour

def create_experiment_period_times():

    global experimentnumperiods
    global experimentnumperiodtimes
    global experimentperiodnumyears
    global experimentperiodnummonths
    global experimentperiodnumdays
    global experimentperiodnumtimes
    global experimentperiodstartyears
    global experimentperiodendyears
    global experimenthistoryfilemonths
    global experimenthistoryfiledays
    global experimenthistoryfilehours
    global experimentperiodoutputtimes

    experimentnumtotalyears = experimentendyear - experimentstartyear + 1
    experimentnumtotalmonths = experimentnumtotalyears * 12
    experimentnumtotaldays = experimentnumtotalyears * 365
    experimentnumperiods = int(experimentnumtotalyears / 10)
    experimentnumextrayears = experimentnumtotalyears - (experimentnumperiods * 10)
    if (experimentnumextrayears > 0):
        experimentnumperiods += 1
    
    experimentperiodnumyears = np.zeros(experimentnumperiods,dtype=int)
    experimentperiodnummonths = np.zeros(experimentnumperiods,dtype=int)
    experimentperiodnumdays = np.zeros(experimentnumperiods,dtype=int)
    experimentperiodnumtimes = np.zeros(experimentnumperiods,dtype=int)
    experimentperiodstartyears = np.zeros(experimentnumperiods,dtype=int)
    experimentperiodendyears = np.zeros(experimentnumperiods,dtype=int)

    periodstartyear = experimentstartyear
    periodendyear = experimentstartyear + 9
    periodyearnum = periodendyear - periodstartyear + 1
    for periodindex in range(experimentnumperiods):
        experimentperiodnumyears[periodindex] = periodyearnum
        experimentperiodnummonths[periodindex] = periodyearnum * 12
        experimentperiodnumdays[periodindex] = periodyearnum * 365
        experimentperiodnumtimes[periodindex] = periodyearnum * experimentgrouphistorytimesperyear
        experimentperiodstartyears[periodindex] = periodstartyear
        experimentperiodendyears[periodindex] = periodendyear
        periodstartyear += 10
        if (periodindex < experimentnumperiods - 2):
            periodendyear += 10
        else:
            periodendyear = experimentendyear
        periodyearnum = periodendyear - periodstartyear + 1

    experimenthistoryfilemonths = np.zeros(experimentgrouphistoryfilesperyear,dtype=int)
    experimenthistoryfiledays = np.zeros(experimentgrouphistoryfilesperyear,dtype=int)
    experimenthistoryfilehours = np.zeros(experimentgrouphistoryfilesperyear,dtype=int)

    historyfilemonth = 1
    historyfileday = get_first_history_day()
    historyfilehour = get_file_hour(historyfilemonth,historyfileday)
    for historyfileindex in range(experimentgrouphistoryfilesperyear):
        experimenthistoryfilemonths[historyfileindex] = historyfilemonth
        experimenthistoryfiledays[historyfileindex] = historyfileday
        experimenthistoryfilehours[historyfileindex] = historyfilehour
        nexthistoryfilemonth = get_next_month(historyfilemonth,historyfileday)
        nexthistoryfileday = get_next_day(historyfilemonth,historyfileday)
        historyfilemonth = nexthistoryfilemonth
        historyfileday = nexthistoryfileday

    experimentnumperiodtimes = 10 * experimentgrouphistorytimesperyear
    experimentperiodoutputtimes = np.zeros(shape=(experimentnumperiods,experimentnumperiodtimes),dtype=np.float64)

    outputtimecount = 0.0
    monthdaysindex = -1
    for periodindex in range(experimentnumperiods):
        for timeindex in range(experimentnumperiodtimes):
            if (experimentgrouphistorytimetype == "hour_1"):
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 1.0 / 24.0
            if (experimentgrouphistorytimetype == "hour_3"):
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 3.0 / 24.0
            if (experimentgrouphistorytimetype == "hour_6"):
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 6.0 / 24.0
            if (experimentgrouphistorytimetype == "day_1"):
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 1.0
            if (experimentgrouphistorytimetype == "month_1"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 14
                else:
                    outputtimecount += nummonthdays[monthdaysindex]
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
                if (monthdaysindex < 11):
                    monthdaysindex += 1
                else:
                    monthdaysindex = 0
            if (experimentgrouphistorytimetype == "day_365"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 181
                else:
                    outputtimecount += 365
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount
            if (experimentgrouphistorytimetype == "year_1"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 181
                else:
                    outputtimecount += 365
                experimentperiodoutputtimes[periodindex,timeindex] = outputtimecount

    return experimentnumperiods

def read_variable_file(variablelistfilename):

    global numvariables
    global variablenames
    global variableprocesstypes

    if (not os.path.isfile(variablelistfilename)):
        print("Unknown Variable List: " + variablelistfilename)
        sys.exit()

    variablelistfile = open(variablelistfilename,'r')
    variablelist = variablelistfile.readlines()
    numvariables = len(variablelist)
    variablenames = [""] * numvariables
    variableprocesstypes = [""] * numvariables
    for variablelistindex in range(numvariables):
        variablelistvalues = variablelist[variablelistindex].split()
        variablenames[variablelistindex] = variablelistvalues[1]
        variableprocesstypes[variablelistindex] = variablelistvalues[4]

    return numvariables

def create_history_filename(historyyear,historymonth,historyday,historyhour):
    historyexperimentfilename = experimentsourcedir + "/" + experimentname + "/" + experimentgrouphistorysource + "/" + experimentname + "." + experimentgrouphistoryfiletype
    if (experimentgrouphistoryfiletype == "cam.h0" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "cam.h1" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "cam.h2" and experimentgrouphistorytimetype == "hour_6"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "cam.h4" and experimentgrouphistorytimetype == "hour_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "cam.h6" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "cice.h" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_5"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h0" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h1" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h2" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_365"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_365"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h5" and experimentgrouphistorytimetype == "hour_6"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h6" and experimentgrouphistorytimetype == "day_365"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "clm2.h7" and experimentgrouphistorytimetype == "day_365"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "cism.h" and experimentgrouphistorytimetype == "year_1"):
        if (historyyear == experimentstartyear):
            historyexperimentfilename = historyexperimentfilename + "." + str(historyyear+1).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
        else:
            historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "mosart.h0" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "mosart.h1" and experimentgrouphistorytimetype == "hour_3"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + "-" + str(historyhour).zfill(5) + ".nc"
    if (experimentgrouphistoryfiletype == "pop.h" and experimentgrouphistorytimetype == "month_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + "-" + str(historymonth).zfill(2) + "-" + str(historyday).zfill(2) + ".nc"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nyear1" and experimentgrouphistorytimetype == "year_1"):
        historyexperimentfilename = historyexperimentfilename + "." + str(historyyear).zfill(4) + ".nc"
    return historyexperimentfilename

def create_timeseries_filename(timeseriesvariable,timeseriesstartyear,timeseriesendyear,timeseriesstatus):
    timeseriesfilename = experimentoutputdir + "/" + experimentname + "/" + experimentgrouphistoryoutput + "/" + experimentgrouphistorytimetype + "/"
    timeseriesfilename = timeseriesfilename + experimentname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + timeseriesstatus + "."
    if (experimentgrouphistoryfiletype == "cam.h0" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "cam.h1" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "cam.h2" and experimentgrouphistorytimetype == "hour_6"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "123100.nc"
    if (experimentgrouphistoryfiletype == "cam.h4" and experimentgrouphistorytimetype == "hour_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "123100.nc"
    if (experimentgrouphistoryfiletype == "cam.h6" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "cice.h" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_5"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h0" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "clm2.h1" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "clm2.h2" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_365"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_365"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h5" and experimentgrouphistorytimetype == "hour_6"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "123100.nc"
    if (experimentgrouphistoryfiletype == "clm2.h6" and experimentgrouphistorytimetype == "day_365"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "clm2.h7" and experimentgrouphistorytimetype == "day_365"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "cism.h" and experimentgrouphistorytimetype == "year_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "mosart.h0" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "mosart.h1" and experimentgrouphistorytimetype == "hour_3"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "123100.nc"
    if (experimentgrouphistoryfiletype == "pop.h" and experimentgrouphistorytimetype == "month_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "01-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "12.nc"
    if (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + "1231.nc"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nyear1" and experimentgrouphistorytimetype == "year_1"):
        timeseriesfilename = timeseriesfilename + str(timeseriesstartyear).zfill(4) + "-"
        timeseriesfilename = timeseriesfilename + str(timeseriesendyear).zfill(4) + ".nc"
    return timeseriesfilename

def create_log_filename(timeseriesvariable,timeseriesstartyear,timeseriesendyear):
    logfilename = experimentoutputdir + "/" + experimentname + "/" + experimentgrouphistoryoutput + "/logfiles/"
    logfilename = logfilename + experimentname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + "."
    if (experimentgrouphistoryfiletype == "cam.h0" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "cam.h1" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "cam.h2" and experimentgrouphistorytimetype == "hour_6"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "123100.log"
    if (experimentgrouphistoryfiletype == "cam.h4" and experimentgrouphistorytimetype == "hour_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "123100.log"
    if (experimentgrouphistoryfiletype == "cam.h6" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "cice.h" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_5"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h0" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "clm2.h1" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "clm2.h2" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_365"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_365"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h5" and experimentgrouphistorytimetype == "hour_6"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "123100.log"
    if (experimentgrouphistoryfiletype == "clm2.h6" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "clm2.h7" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "cism.h" and experimentgrouphistorytimetype == "year_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "mosart.h0" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "mosart.h1" and experimentgrouphistorytimetype == "hour_3"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "123100.log"
    if (experimentgrouphistoryfiletype == "pop.h" and experimentgrouphistorytimetype == "month_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "01-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "12.log"
    if (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nyear1" and experimentgrouphistorytimetype == "year_1"):
        logfilename = logfilename + str(timeseriesstartyear).zfill(4) + "-"
        logfilename = logfilename + str(timeseriesendyear).zfill(4) + ".log"
    return logfilename

def create_submission_filename(timeseriesvariable,timeseriesstartyear,timeseriesendyear):
    submissionfilename = experimentoutputdir + "/" + experimentname + "/" + experimentgrouphistoryoutput + "/submissionfiles/"
    submissionfilename = submissionfilename + experimentname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + "."
    if (experimentgrouphistoryfiletype == "cam.h0" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "cam.h1" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "cam.h2" and experimentgrouphistorytimetype == "hour_6"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "123100.sh"
    if (experimentgrouphistoryfiletype == "cam.h4" and experimentgrouphistorytimetype == "hour_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "123100.sh"
    if (experimentgrouphistoryfiletype == "cam.h6" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "cice.h" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "cice.h1" and experimentgrouphistorytimetype == "day_5"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h0" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "clm2.h1" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "clm2.h2" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h3" and experimentgrouphistorytimetype == "day_365"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h4" and experimentgrouphistorytimetype == "day_365"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h5" and experimentgrouphistorytimetype == "hour_6"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "123100.sh"
    if (experimentgrouphistoryfiletype == "clm2.h6" and experimentgrouphistorytimetype == "day_365"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "clm2.h7" and experimentgrouphistorytimetype == "day_365"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "cism.h" and experimentgrouphistorytimetype == "year_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "mosart.h0" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "mosart.h1" and experimentgrouphistorytimetype == "hour_3"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "010100-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "123100.sh"
    if (experimentgrouphistoryfiletype == "pop.h" and experimentgrouphistorytimetype == "month_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "01-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "12.sh"
    if (experimentgrouphistoryfiletype == "pop.h.nday1" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nday1" and experimentgrouphistorytimetype == "day_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "0101-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + "1231.sh"
    if (experimentgrouphistoryfiletype == "pop.h.ecosys.nyear1" and experimentgrouphistorytimetype == "year_1"):
        submissionfilename = submissionfilename + str(timeseriesstartyear).zfill(4) + "-"
        submissionfilename = submissionfilename + str(timeseriesendyear).zfill(4) + ".sh"
    return submissionfilename

def create_status_filename(timeseriesstartyear,timeseriesendyear):
    statusfilename = experimentoutputdir + "/" + experimentname + "/statusfiles/"
    statusfilename = statusfilename + experimentname + "." + experimentgrouphistoryfiletype + ".status."
    statusfilename = statusfilename + str(timeseriesstartyear).zfill(4) + "0101-"
    statusfilename = statusfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    return statusfilename

def create_status_restart_filename(timeseriesstartyear,timeseriesendyear):
    statusfilename = experimentoutputdir + "/" + experimentname + "/statusfiles/"
    statusfilename = statusfilename + experimentname + ".restartfiles.status."
    statusfilename = statusfilename + str(timeseriesstartyear).zfill(4) + "0101-"
    statusfilename = statusfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    return statusfilename

