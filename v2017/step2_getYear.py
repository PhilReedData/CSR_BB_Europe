#!/usr/bin/python   
# Mine the documents for most frequent year 

corruptFiles = [
    "072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf",
    "050808_BARC_Corporate_Responsibility_SD000000000083695052.pdf",
    "072208_PSN_Corporate_Responsibility_WC000000000087325914.pdf",
    "072408_BARC_Corporate_Responsibility_WC000000000087461360.pdf"
    ]
# Do we process the PDF/HTM files this time?
doPDF = True
doHTM = True

import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF
import utilGetYearFromHTM
from utilGetYearFromHTM import findModeYearInHTM

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2
unzipDirs = [f for f in listdir(unzipPath) if not (isfile(join(unzipPath, f)) )]
unzipDirs.sort()

#print(len(unzipDirs), 'unzipped')


fout = open('years.csv','w')
fout.write('country,sourcefile,format,year\n')

countriesToSkip = ['ZZ_OTHER']

for unzipDir in unzipDirs:
    country = unzipDir
    if unzipDir not in countriesToSkip:
        print(unzipDir)
        files = [f for f in listdir(join(unzipPath, unzipDir)) if (isfile(join(unzipPath, unzipDir ,f)) )]
        files.sort()
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in corruptFiles) and doPDF:
                print (file)
                # Get year from first page(s) of PDF
                path = join(unzipPath, unzipDir, file)
                year = -2
                try:
                    year = findModeYearInPDF(path)
                    #print (file, year)
                except:
                    year = -1
                    print ('Could not read file: ' + file)

                # Update log
                fout.write(country + ',' + file + ',pdf,' + str(year) + '\n')
            elif file.endswith('.htm') and (not file in corruptFiles) and doHTM:
                format = 'htm'
                # Get year from HTML file
                path = join(unzipPath, unzipDir, file)
                year = -3
                try:
                    year = findModeYearInHTM(path)
                except:
                    year = -1
                    print ('Could not read file: ' +file)
                
                # Update log
                fout.write(country + ',' + file + ',htm,' + str(year) + '\n')
fout.close()
