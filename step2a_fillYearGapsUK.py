#!/usr/bin/python    
# Where did we get the year from?
YEARSOURCES = {10:'META', 20:'MINED', -1:'NOTFOUND'}

# Do we process the PDF/HTM files this time?
doPDF = True
doHTM = True

import pandas as pd
import numpy as np

import utilGetYearFromPDF
import utilGetYearFromHTM
from os.path import join
unzipPathAR = "U:/Ser-Huang_Poon/UK_ARunzip/"
unzipPathCR = "U:/Ser-Huang_Poon/UK_CRunzip/"
unzipPathESG = "U:/Ser-Huang_Poon/UK_ESGunzip/"
unzipPathDict = {'AR':unzipPathAR, 'CR':unzipPathCR, 'ESG':unzipPathESG}

pathIn = 'yearsUK.csv'
pathOut = 'yearsFilledUK.csv'

fout = open(pathOut,'w')
fout.write('reporttype,sourcefile,format,bestyear,yearsource,metayear,minedyear,uploadyear\n')

df = pd.read_csv(pathIn)
for index, row in df.iterrows():
    reporttype = row["reporttype"]
    sourcefile = row["sourcefile"]
    format = row["format"]
    minedyear = row["year"]
    if (format=='pdf' and doPDF) or (format=='htm' and doHTM):     
        # Get year from metadata, where possible
        if reporttype not in unzipPathDict.keys():
            print ('Report type unknown (' + reporttype + ') for sourcefile: ' + sourcefile)
            continue
        unzipPath = unzipPathDict[reporttype]
        sourcepath = join(unzipPath, sourcefile)
        if format=='pdf':
            metayear = utilGetYearFromPDF.getPDFMetaCreationYear(sourcepath)
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
        if metayear > 0:
            bestyear = metayear
            yearsource = 10
        elif minedyear > 0:
            bestyear = minedyear
            yearsource = 20
        else:
            bestyear = -1
            yearsource = -1
        
        # Update log
        lineout = reporttype + ',' + sourcefile + ',' + format + ',' + str(bestyear)
        lineout += ',' + str(yearsource) +  ',' + str(metayear) + ',' + str(minedyear)
        lineout += ',' + str(uploadyear) + '\n'
        fout.write(lineout)

fout.close()