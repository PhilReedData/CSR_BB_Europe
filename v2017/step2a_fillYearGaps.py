#!/usr/bin/python    
# Choose the best year, from where?
YEARSOURCES = {10:'META', 20:'MINED', -1:'NOTFOUND'}

import pandas as pd
import numpy as np

# Do we process the PDF/HTM files this time?
doPDF = True
doHTM = False

import utilGetYearFromPDF
import utilGetYearFromHTM
from os.path import join
unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
pathIn = 'years.csv'
pathOut = 'yearsFilled.csv'

fout = open(pathOut,'w')
fout.write('country,sourcefile,format,bestyear,yearsource,metayear,minedyear,uploadyear\n')

df = pd.read_csv(pathIn)
for index, row in df.iterrows():
    country = row["country"]
    sourcefile = row["sourcefile"]
    format = row["format"]
    minedyear = row["year"]
         
    if (format=='pdf' and doPDF) or (format=='htm' and doHTM):     
        # Get year from metadata, where possible
        sourcepath = join(unzipPath, country+'/'+sourcefile)
        if format=='pdf':
            metayear = utilGetYearFromPDF.getPDFMetaCreationYear(sourcepath) - 1
        elif format=='htm':
            metayear = utilGetYearFromHTM.getHTMMetaYear(sourcepath)
        else:
            metayear = -3
            
        # Year from upload date in filename MMDDYY...
        yyFromFilename = sourcefile[4:6]
        try:
            uploadyear = 2000 + int(yyFromFilename)
        except ValueError:
            uploadyear = -1
                
        # Decide bestyear 
        if metayear > 0 and metayear <= uploadyear:
            bestyear = metayear
            yearsource = 10
        elif minedyear > 0 and minedyear <= uploadyear:
            bestyear = minedyear
            yearsource = 20
        else:
            bestyear = -1
            yearsource = -1
        
        # Update log
        lineout = country + ',' + sourcefile + ',' + format + ',' + str(bestyear)
        lineout += ',' + str(yearsource) +  ',' + str(metayear) + ',' + str(minedyear)
        lineout += ',' + str(uploadyear) + '\n'
        fout.write(lineout)
        
fout.close()
