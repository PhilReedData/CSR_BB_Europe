#!/usr/bin/python    

corruptFiles = [
    "072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf",
    "050808_BARC_Corporate_Responsibility_SD000000000083695052.pdf",
    "072208_PSN_Corporate_Responsibility_WC000000000087325914.pdf",
    "072408_BARC_Corporate_Responsibility_WC000000000087461360.pdf"
    ]

import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2
unzipDirs = [f for f in listdir(unzipPath) if not (isfile(join(unzipPath, f)) )]

#print(len(unzipDirs), 'unzipped')

#TEMP
#fout = open('years.csv','w')
#fout.write('country,sourcefile,year\n')
fout = open('years.csv','a')

countriesToSkip = ['ZZ_OTHER']

for unzipDir in unzipDirs:
    country = unzipDir
    #TEMP
    #if unzipDir not in countriesToSkip:
    if unzipDir == 'GB':
        print(unzipDir)
        files = [f for f in listdir(join(unzipPath, unzipDir)) if (isfile(join(unzipPath, unzipDir ,f)) )]
        files.sort()
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in corruptFiles):
                print (file)
                # Get year from first page of PDF
                path = join(unzipPath, unzipDir, file)
                year = -2
                try:
                    year = findModeYearInPDF(path)
                    #print (file, year)
                except Exception as e:
                    year = -1
                    print ('Could not open file: ' + file)

                # Update log
                fout.write(country + ',' + file + ',' + str(year) + '\n')
                
fout.close()