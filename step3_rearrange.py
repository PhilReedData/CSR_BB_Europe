#!/usr/bin/python    
# Move the Step 2 rearranging of files here.
# Currently a duplication, will remove from Step 2 later.

import pandas as pd
import numpy as np

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
outPath = "U:/Phil_Read/CSR_Europe/unzipped_country_year/"
planPath = 'years.csv'

df = pd.read_csv(planPath)
# Headings ('country,sourcefile,year,sic,isin,copy')

if not exists(outPath):
    mkdir(outPath)

for index, row in df.iterrows():
    country = row["country"]
    sourcefile = row["sourcefile"]
    year = row["year"]
    sic = row["sic"]
    isin = row["isin"]
    # The _IOError will not be there once file copying removed from step 2
    copy = row["copy"].rstrip('_IOError')
    
    outfilename = sic + '_' + isin + '_' + reporttype +copycount+'.pdf'
    outfilepath =  join(outPath, country+'/'+year+'/'+outfilename)
    if not exists(join(outPath, country)):
        mkdir(join(outPath, country))
    if not exists(join(outPath, country+'/'+str(year))):
        mkdir(join(outPath, country+'/'+str(year)))
    try:
        copy2(path , outfilepath)
        print ('Written to: ' + country + '/' + year + '/' + outfilename)
    except IOError as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print ('Could not write to ' + country + '/' + year + '/' + outfilepath)