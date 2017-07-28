#!/usr/bin/python    

corruptFiles = []

import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF

unzipPathAR = "U:/Ser-Huang_Poon/UK_AnnualReportUnzip/"
unzipPathCR = "U:/Ser-Huang_Poon/UK_CSRunzip/"
unzipPathESG = "U:/Ser-Huang_Poon/UK_ESGunzip/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

# List of Tuples of (reportType, unzipPath)
unzipPaths = [('AR',unzipPathAR), ('CR',unzipPathCR), ('ESG',unzipPathESG)]

print(len(unzipPathAR + unzipPathCR + unzipPathESG), 'unzipped')

fout = open('yearsUK.csv','w')
fout.write('reporttype,sourcefile,year\n')

reportTypesToSkip = [] # to use later if we run a subset 

for pair in unzipPaths:
    reportType = pair[0]
    unzipPath = pair[1]
    if reportType not in reportTypesToSkip:
        print(reportType)
        files = [f for f in listdir(unzipPath) if isfile(join(unzipPath, f))]
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in corruptFiles):
                # Get year from first page of PDF
                path = join(unzipPath, file)
                year = -2
                try:
                    year = findModeYearInPDF(path)
                    #print (file, year)
                except Exception as e:
                    year = -1
                    print ('Could not open file: ' + file)

                # Update log
                fout.write(reportType + ',' + file + ',' + str(year) + '\n')
                
fout.close()