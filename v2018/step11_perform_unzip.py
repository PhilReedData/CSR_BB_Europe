#!/usr/bin/python    

# Unzip everything to one folder

### Change this True/False to run Europe or UK version of code. ###
isEurope = True # UK not implemented yet

# Import my utilities
import utilCSR

# Paths
zipPathEurope = "U:/Ser-Huang_Poon/Europe_CSRzipBloomberg/"
unzipPathEurope = "U:/Phil_Read/CSR_Europe/unzipped_allinone/"
zipPathUK = "" # there are three folders of zips! Rethink this, loop or similar
unzipPathUK = "U:/Phil_Read/CSR_UK/unzipped_allinone/"
zipPath = zipPathEurope if isEurope else zipPathUK
unzipPath = unzipPathEurope if isEurope else unzipPathUK
tableOutPath = 'stats11EU.csv' if isEurope else 'stats11UK.csv'
refinedTableOutPath = 'stats13EU.csv' if isEurope else 'stats13UK.csv'
SEP = ','
# Files to skip within the zip archives, such as files that should not be there.
SKIP_FILES = ['20170717c_EuropeCSR.xlsx']

# Prepare dataframe and output table
tableOut = open(tableOutPath,'w')
columnHeadings = ['filenamefull', 'filetype', 'filenameshort','reporttype','uploadyear','ticker','country','unzip']
tableOut.write(SEP.join(columnHeadings) + '\n')
import pandas as pd
df = pd.DataFrame(columns=columnHeadings)
rowCount = 0

# Get list of zip files
from os import listdir
from os.path import isfile, join
zipfiles = [f for f in listdir(zipPath) if (isfile(join(zipPath, f)) )]
zipfiles.sort()
print(len(zipfiles),'zipfiles to unzip')

# Loop zip files
import zipfile
import os.path
for zip in zipfiles:
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
                previousCountry = match['country']
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
newColumnHeadings = columnHeadings[:-2] + ['countries']
df.rename(index=str, columns = newColumnHeadings, inplace = True)
# Export dataframe
df.to_csv(refinedTableOutPath, encoding='utf-8', index=False)