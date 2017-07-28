#!/usr/bin/python    

import utilReadExcelCSRUK
from utilReadExcelCSRUK import companies

import pandas as pd
import numpy as np

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

doCopy = True
countriesToSkip = []

unzipPathAR = "U:/Ser-Huang_Poon/UK_ARunzip/"
unzipPathCR = "U:/Ser-Huang_Poon/UK_CRunzip/"
unzipPathESG = "U:/Ser-Huang_Poon/UK_ESGunzip/"
outPath = "U:/Phil_Read/CSR_UK/unzipped_reporttype_year-2/"
planPath = 'yearsFilledUK.csv'
logPath = 'statsUK-2.csv'

# Dictionary of reporttype to unzipPath
unzipPathDict = {'AR':unzipPathAR, 'CR':unzipPathCR, 'ESG':unzipPathESG}

if isfile(logPath):
    # Continue from before
    log = open(logPath,'a')
else:
    log = open(logPath,'w')
    # Rpart is called copycount later
    log.write('reporttype,sourcefile,year,yearsource,sic,isin,Rpart,destfile,ticker,name\n')

df = pd.read_csv(planPath)
# Headings ('reporttype,sourcefile,year,yearsource,metayear')

if not exists(outPath):
    mkdir(outPath)

for index, row in df.iterrows():
    reporttype = row["reporttype"]
    sourcefile = row["sourcefile"]
    year = row["year"]
    yearsource = row["yearsource"]
    metayear = row["metayear"]
    print(reporttype, sourcefile, year)
    company = companies.getCompanyByBBFilename('GB', sourcefile)
    sic = company.sic
    isin = company.isin
    ticker = company.tickerFull
    name = company.name
    #
    # Try out filenames that do not exist
    # (there are multiple reports for some ticker/year/reporttype)
    copycount = 1
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    #print(outfilename)
    while isfile(join(outPath, reporttype+'/'+str(year)+'/'+outfilename)):
        # Increment suffix until no overwriting possible
        copycount += 1
        outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    outfilepath =  join(outPath, reporttype+'/'+str(year)+'/'+outfilename)
    if not exists(join(outPath, reporttype)):
        mkdir(join(outPath, reporttype))
    if not exists(join(outPath, reporttype+'/'+str(year))):
        mkdir(join(outPath, reporttype+'/'+str(year)))
    
    if reporttype not in unzipPathDict.keys():
        print ('Report type unknown (' + reporttype + ') for sourcefile: ' + sourcefile)
        continue
    unzipPath = unzipPathDict[reporttype]
    
    fromPath = join(unzipPath, sourcefile)
    try:
        if doCopy and (not reporttype in countriesToSkip):
            copy2(fromPath, outfilepath)
            print ('Written to: ' + reporttype + '/' + str(year) + '/' + outfilename)
    except IOError as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        #print ('fromPath ' + fromPath)
        #print ('outfilepath ' + outfilepath)
        print ('Could not write to ' + reporttype + '/' + str(year) + '/' + outfilename)
        #raise e
    # Update log
    lineout = reporttype + ',' + sourcefile + ',' + str(year) + ',' + str(yearsource) 
    lineout += ',' + str(metayear)
    lineout += ',' + str(sic) + ',' + isin + ',' + str(copycount) + ',' + outfilename 
    lineout += ',"' + ticker + '","' + name + '"\n'
    log.write(lineout)


log.close()