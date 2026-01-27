#! /usr/bin/env python
import numpy as np

# Global Variables

nummonthdays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] 

experimentgrouphistoryshortname = ""
experimentgrouphistoryfiletype = ""
experimentgrouphistorysourcedir = ""
experimentgrouphistorysource = ""
experimentgrouphistoryoutputdir = ""
experimentgrouphistoryoutput = ""
experimentgrouphistorytimetype = ""
experimentgrouphistoryfilesperyear = -1
experimentgrouphistorydaysperfile = -1
experimentgrouphistorytimesperfile = -1
experimentgrouphistorytimesperyear = -1

experimentgroupoutputtimes = np.zeros(shape=(0,0),dtype=np.float64)

experimentshortname = ""
experimentlocation = ""
experimentlongname = ""
experimentstartyearname = ""
experimentstartyear = -1
experimentendyearname = ""
experimentendyear = -1

# Function Definitions

def create_history_output_times(num10yrfiles):
    global experimentgroupoutputtimes
    periodnumtimes = 10 * experimentgrouphistorytimesperyear
    experimentgroupoutputtimes = np.resize(experimentgroupoutputtimes,(num10yrfiles,periodnumtimes))
    outputtimecount = 0.0
    monthdaysindex = -1
    for periodindex in range(num10yrfiles):
        for timeindex in range(periodnumtimes):
            if (experimentgrouphistorytimetype == "hour_1"):
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 1.0 / 24.0
            if (experimentgrouphistorytimetype == "hour_3"):
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 3.0 / 24.0
            if (experimentgrouphistorytimetype == "hour_6"):
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 6.0 / 24.0
            if (experimentgrouphistorytimetype == "day_1"):
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
                outputtimecount += 1.0
            if (experimentgrouphistorytimetype == "month_1"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 14
                else:
                    outputtimecount += nummonthdays[monthdaysindex]
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
                if (monthdaysindex < 11):
                    monthdaysindex += 1
                else:
                    monthdaysindex = 0
            if (experimentgrouphistorytimetype == "day_365"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 181
                else:
                    outputtimecount += 365
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount
            if (experimentgrouphistorytimetype == "year_1"):
                if (periodindex == 0 and timeindex == 0):
                    outputtimecount = 181
                else:
                    outputtimecount += 365
                experimentgroupoutputtimes[periodindex,timeindex] = outputtimecount

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

def create_history_filename(historyyear,historymonth,historyday,historyhour):
    historyexperimentfilename = experimentgrouphistorysourcedir + "/" + experimentlongname + "/" + experimentgrouphistorysource + "/" + experimentlongname + "." + experimentgrouphistoryfiletype
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
    timeseriesfilename = experimentgrouphistoryoutputdir + "/" + experimentlongname + "/" + experimentgrouphistoryoutput + "/" + experimentgrouphistorytimetype + "/"
    timeseriesfilename = timeseriesfilename + experimentlongname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + timeseriesstatus + "."
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
    logfilename = experimentgrouphistoryoutputdir + "/" + experimentlongname + "/" + experimentgrouphistoryoutput + "/logfiles/"
    logfilename = logfilename + experimentlongname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + "."
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
    submissionfilename = experimentgrouphistoryoutputdir + "/" + experimentlongname + "/" + experimentgrouphistoryoutput + "/submissionfiles/"
    submissionfilename = submissionfilename + experimentlongname + "." + experimentgrouphistoryfiletype + "." + timeseriesvariable + "."
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
    statusfilename = experimentgrouphistoryoutputdir + "/" + experimentlongname + "/statusfiles/"
    statusfilename = statusfilename + experimentlongname + "." + experimentgrouphistoryfiletype + ".status."
    statusfilename = statusfilename + str(timeseriesstartyear).zfill(4) + "0101-"
    statusfilename = statusfilename + str(timeseriesendyear).zfill(4) + "1231.log"
    return statusfilename

