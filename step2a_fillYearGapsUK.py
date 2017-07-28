#!/usr/bin/python    
# Where did we get the year from?
YEARSOURCES = {0:'MINED', -1:'FILENAME_PDF-UNOPENED', -2:'FILENAME_PDF-NOYEARFOUND'}

import pandas as pd
import numpy as np

import utilGetYearFromPDF
from os.path import join
unzipPathAR = "U:/Ser-Huang_Poon/UK_ARunzip/"
unzipPathCR = "U:/Ser-Huang_Poon/UK_CRunzip/"
unzipPathESG = "U:/Ser-Huang_Poon/UK_ESGunzip/"
unzipPathDict = {'AR':unzipPathAR, 'CR':unzipPathCR, 'ESG':unzipPathESG}

pathIn = 'yearsUK.csv'
pathOut = 'yearsFilledUK.csv'

fout = open(pathOut,'w')
fout.write('reporttype,sourcefile,year,yearsource,metayear\n')

df = pd.read_csv(pathIn)
for index, row in df.iterrows():
    reporttype = row["reporttype"]
    sourcefile = row["sourcefile"]
    year = row["year"]
         
    # Where did we get the year? And subsitute if needed
    yearsource = 0
    if year == -1: # if file was unreadable (encrypted)
        yearsource = year
    elif year == -2: # if year not found in 3 pages of PDF
        yearsource = year
        # The filename is MMDDYY...
        yyFromFilename = sourcefile[4:6]
        try:
            year = 2000 + int(yyFromFilename)
        except ValueError:
            pass
    
    # Get year from metadata too, where possible
    if reporttype not in unzipPathDict.keys():
        print ('Report type unknown (' + reporttype + ') for sourcefile: ' + sourcefile)
        continue
    unzipPath = unzipPathDict[reporttype]
    sourcepath = join(unzipPath, sourcefile)
    metayear = utilGetYearFromPDF.getPDFMetaCreationYear(sourcepath)
    # Update log
    fout.write(reporttype + ',' + sourcefile + ',' + str(year) + ',' + str(yearsource) +  ',' + str(metayear) + '\n')

fout.close()