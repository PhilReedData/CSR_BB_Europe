#!/usr/bin/python    

import utilReadExcelCSREurope
from utilReadExcelCSREurope import companies

import pandas as pd
import numpy as np

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

doCopy = True

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
outPath = "U:/Phil_Read/CSR_Europe/unzipped_country_year/"
planPath = 'years.csv'

log = open('stats.csv','w')
log.write('country,sourcefile,year,sic,isin,CRpart,destfile\n')

df = pd.read_csv(planPath)
# Headings ('country,file,year')

if not exists(outPath):
    mkdir(outPath)

for index, row in df.iterrows():
    country = row["country"]
    sourcefile = row["file"]
    year = row["year"]
    print(country, sourcefile, year)
    company = companies.getCompanyByBBFilename(country, sourcefile)
    sic = company.sic
    isin = company.isin
    reporttype = 'CR' # Only this for now
    # Try out filenames that do not exist
    # (there are multiple reports for some ticker/year/country)
    copycount = 1
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    #print(outfilename)
    while isfile(join(outPath, country+'/'+str(year)+'/'+outfilename)):
        # Increment suffix until no overwriting possible
        copycount += 1
        outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    
    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
    outfilepath =  join(outPath, country+'/'+str(year)+'/'+outfilename)
    if not exists(join(outPath, country)):
        mkdir(join(outPath, country))
    if not exists(join(outPath, country+'/'+str(year))):
        mkdir(join(outPath, country+'/'+str(year)))
    
    fromPath = join(unzipPath, country, sourcefile)
    try:
        if doCopy:
            copy2(fromPath, outfilepath)
            print ('Written to: ' + country + '/' + str(year) + '/' + outfilename)
    except IOError as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print ('Could not write to ' + country + '/' + str(year) + '/' + outfilename)
    # Update log
    log.write(country + ',' + sourcefile + ',' + str(year) + ',' + str(sic) + ',' + isin + ',' + str(copycount) + ',' + outfilename + '\n')


log.close()