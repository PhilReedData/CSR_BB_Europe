#!/usr/bin/python    

import utilReadExcelCSREurope
from utilReadExcelCSREurope import companies

import pandas as pd
import numpy as np

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

doCopy = True
countriesToSkip = []
#countriesToSkip = ['AT', 'CH', 'DE', 'ES', 'FR', 'IE', 'PT', 'SE', 'GB'] # TEMP

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
outPath = "U:/Phil_Read/CSR_Europe/unzipped_country_year/"
planPath = 'yearsFilled.csv'
logPath = 'stats.csv'

if isfile(logPath):
    # Continue from before
    log = open(logPath,'a')
else:
    log = open(logPath,'w')
    headline = 'country,sourcefile,format,'
    headline += 'bestyear,yearsource,metayear,minedyear,uploadyear,'
    headline += 'sic,isin,Rpart,destfile,ticker,name\n'
    log.write(headline)

df = pd.read_csv(planPath)
# Headings ('country,sourcefile,format,bestyear,yearsource,metayear,minedyear,uploadyear')

if not exists(outPath):
    mkdir(outPath)

for index, row in df.iterrows():
    country = row["country"]
    sourcefile = row["sourcefile"]
    format = row["format"]
    ext = '.' + format
    year = row["bestyear"]
    yearsource = row["yearsource"]
    metayear = row["metayear"]
    minedyear = row["minedyear"]
    uploadyear = row["uploadyear"]
    print(country, sourcefile, year)
    company = companies.getCompanyByBBFilename(country, sourcefile)
    sic = company.sic
    isin = company.isin
    ticker = company.tickerFull
    name = company.name
    reporttype = 'CR' # Only this for now
    # Try out filenames that do not exist
    # (there are multiple reports for some ticker/year/country)
    copycount = 1
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+ext
    #print(outfilename)
    while isfile(join(outPath, country+'/'+str(year)+'/'+outfilename)):
        # Increment suffix until no overwriting possible
        copycount += 1
        outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+ext
    
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+ext
    outfilepath =  join(outPath, country+'/'+str(year)+'/'+outfilename)
    if not exists(join(outPath, country)):
        mkdir(join(outPath, country))
    if not exists(join(outPath, country+'/'+str(year))):
        mkdir(join(outPath, country+'/'+str(year)))
    
    fromPath = join(unzipPath, country, sourcefile)
    try:
        if doCopy and (not country in countriesToSkip):
            copy2(fromPath, outfilepath)
            print ('Written to: ' + country + '/' + str(year) + '/' + outfilename)
    except IOError as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print ('Could not write to ' + country + '/' + str(year) + '/' + outfilename)
    # Update log
    lineout = country + ',' + sourcefile + ',' + format
    lineout += ',' + str(year) + ',' + str(yearsource) 
    lineout += ',' + str(metayear) + ',' + str(minedyear) + ',' + str(uploadyear)
    lineout += ',' + str(sic) + ',' + isin + ',' + str(copycount) + ',' + outfilename 
    lineout += ',"' + ticker + '","' + name + '"\n'
    log.write(lineout)


log.close()