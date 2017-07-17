#!/usr/bin/python    

#import utilReadExcelCSREurope

#from utilReadExcelCSREurope import companies

#lastCompany = companies.companies[-1:]
#print lastCompany
#lastCompany.setYear(2020)
#print lastCompany


import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"

from os import listdir
from os.path import isfile, join
unzipDirs = [f for f in listdir(unzipPath) if not (isfile(join(unzipPath, f)) )]

#print(len(unzipDirs), 'unzipped')

fout = open('years.csv','w')
fout.write('country,file,year\n')

for unzipDir in unzipDirs:
    if not unzipDir.startswith('ZZ_'):
        print(unzipDir)
        files = [f for f in listdir(join(unzipPath, unzipDir)) if (isfile(join(unzipPath, unzipDir ,f)) )]
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf'):
                path = join(unzipPath, unzipDir, file)
                year = -1
                try:
                    year = findModeYearInPDF(path)
                    print (file, year)
                except Exception as e:
                    print (file, 'could not open')
                fout.write(unzipDir + ',' + file + ',' + str(year) + '\n')
                
fout.close()