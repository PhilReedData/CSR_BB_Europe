#!/usr/bin/python    

corruptFiles = ["072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf"]

import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2
unzipDirs = [f for f in listdir(unzipPath) if not (isfile(join(unzipPath, f)) )]

#print(len(unzipDirs), 'unzipped')

fout = open('years.csv','w')
fout.write('country,sourcefile,year\n')

countriesToSkip = ['ZZ_OTHER']

for unzipDir in unzipDirs:
    country = unzipDir
    if unzipDir not in countriesToSkip:
        print(unzipDir)
        files = [f for f in listdir(join(unzipPath, unzipDir)) if (isfile(join(unzipPath, unzipDir ,f)) )]
        #print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf') and (not file in corruptFiles):
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