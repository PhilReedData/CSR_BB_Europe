#!/usr/bin/python    

# Unzip everything to one folder

### Change this True/False to run Europe or UK version of code. ###
isEurope = False

# Import my utilities
import utilCSR

# Paths
zipPathEurope = "U:/Ser-Huang_Poon/Europe_CSRzipBloomberg/"
unzipPathEurope = "U:/Phil_Read/CSR_Europe/unzipped_allinone/"
zipPathUK = "U:/Phil_Read/CSR_UK/zipped_allinone/"
unzipPathUK = "U:/Phil_Read/CSR_UK/unzipped_allinone/"
zipPath = zipPathEurope if isEurope else zipPathUK
unzipPath = unzipPathEurope if isEurope else unzipPathUK
tableOutPath = 'stats11EU.csv' if isEurope else 'stats11UK.csv'
refinedTableOutPath = 'stats13EU.csv' if isEurope else 'stats13UK.csv'
SEP = ','
# Files to skip within the zip archives, such as files that should not be there.
SKIP_FILES = ['20170717c_EuropeCSR.xlsx']
SKIP_ZIPS = ['IBEX2013x_BB_Docs_071417_114251.zip']

# Prepare dataframe and output table
tableOut = open(tableOutPath,'w')
columnHeadings = ['filenamefull', 'filetype', 'filenameshort','reporttype','uploadyear','ticker','country','unzip']
tableOut.write(SEP.join(columnHeadings) + '\n')
import pandas as pd
import numpy as np
df = pd.DataFrame(columns=columnHeadings)
rowCount = 0

# Get list of zip files
from os import listdir
from os.path import isfile, join
zipfiles = [f for f in listdir(zipPath) if (isfile(join(zipPath, f)) )]
zipfiles.sort()
#TEMP
#zipfiles = ['AEX2010_BB_Docs_071417_092823.zip', 'BEL2008-11_BB_Docs_071617_163546.zip']
print(len(zipfiles),'zipfiles to unzip')

# Loop zip files
import zipfile
import os.path
for zip in zipfiles:
    if zip in SKIP_ZIPS:
        continue
    countryCode = utilCSR.getIsoFromString(zip) if isEurope else "GB"
    extractPath = os.path.abspath(unzipPath)
    try:
        zipobject = zipfile.ZipFile(zipPath + zip)
        namelist = zipobject.namelist()
        print(len(namelist),'files to extract within', countryCode, zip)
        for name in namelist :
            if name in SKIP_FILES:
                continue
            extractAlreadyExists = os.path.isfile(os.path.join(extractPath, name))
            
            # For each file within the zip, add a row to tableOut
            filenamefull = name
            filetype = utilCSR.rawFilename2Ext(name)
            filenameshort = utilCSR.rawFilename2Short(name)
            reporttype = utilCSR.rawFilename2ReportType(name)
            uploadyear = str(utilCSR.rawFilename2UploadYear(name))
            ticker = utilCSR.rawFilename2Ticker(name)
            country = countryCode
            unzip = '0' if extractAlreadyExists else '1'
            rowValues = [filenamefull,filetype,filenameshort,reporttype,uploadyear,ticker,country,unzip]
            tableOut.write(SEP.join(rowValues) + '\n')
            
            # if df contains name, update country column, else add new row
            match = df.loc[df['filenamefull'] == name]
            if len(match) > 0:
                previousCountry = df.loc[df['filenamefull'] == name, 'country'].iloc[0]
                if previousCountry != country:
                    df.loc[df['filenamefull'] == name, 'country'] = previousCountry + "|" + country
            else:
                df.loc[rowCount] = rowValues
                rowCount += 1
            
            if extractAlreadyExists:
                print('Skipping already unzipped', name, country)
            else:
                # Do the extraction for this report
                zipobject.extract(name, extractPath)
                print('Unzipped', name, country)
            
        ## Do the extraction for this whole zip
        ##zipobject.extractall(extractPath)
        print('Finished extracting', zip)
    except zipfile.BadZipfile as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print('File:' + zip)
        raise e
        
# Write out tables
tableOut.close()
# Drop unzip column 
df = df.drop('unzip',1)
# Rename now last column of df; country to countries
df['countries'] = df['country']
df = df.drop('country',1)
# Export dataframe
df.to_csv(refinedTableOutPath, encoding='utf-8', index=False)