#!/usr/bin/python    

# Mine the PDF and HTM files for year (HTM not yet written)

corruptFiles = []
# Do we process the PDF/HTM files this time?
doPDF = True
doHTM = True

import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF
import utilGetYearFromHTM
from utilGetYearFromHTM import findModeYearInHTM

unzipPathAR = "U:/Ser-Huang_Poon/UK_ARunzip/"
unzipPathCR = "U:/Ser-Huang_Poon/UK_CRunzip/"
unzipPathESG = "U:/Ser-Huang_Poon/UK_ESGunzip/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

# List of Tuples of (reportType, unzipPath)
unzipPaths = [('AR',unzipPathAR), ('CR',unzipPathCR), ('ESG',unzipPathESG)]

print(len(unzipPathAR + unzipPathCR + unzipPathESG), 'unzipped')

fout = open('yearsUK.csv','w')
fout.write('reporttype,sourcefile,format,year\n')

reportTypesToSkip = [] # to use later if we run a subset 

for pair in unzipPaths:
    reportType = pair[0] # e.g. 'AR'
    unzipPath = pair[1]  # e.g. unzipPathAR
    if reportType not in reportTypesToSkip:
        print(reportType)
        # Get list of files in this report type directory
        files = [f for f in listdir(unzipPath) if isfile(join(unzipPath, f))]
        files.sort()
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in corruptFiles) and doPDF:
                format = 'pdf'
                # Get year from first page(s) of PDF
                path = join(unzipPath, file)
                year = -2
                try:
                    year = findModeYearInPDF(path)
                    #print (file, year)
                except Exception as e:
                    year = -1
                    print ('Could not read file: ' + file)

                # Update log
                fout.write(reportType + ',' + file + ',pdf,' + str(year) + '\n')
            elif file.endswith('.htm') and (not file in corruptFiles) and doHTM:
                format = 'htm'
                # Get year from HTML file
                path = join(unzipPath, file)
                year = -3
                try:
                    year = findModeYearInHTM(path)
                except:
                    year = -1
                    print ('Could not read file: ' +file)
                
                # Update log
                fout.write(reportType + ',' + file + ',htm,' + str(year) + '\n')
fout.close()
