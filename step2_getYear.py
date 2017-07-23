#!/usr/bin/python    

import utilReadExcelCSREurope

from utilReadExcelCSREurope import companies

#lastCompany = companies.companies[-1:]
#print lastCompany
#lastCompany.setYear(2020)
#print lastCompany


import utilGetYearFromPDF
from utilGetYearFromPDF import findModeYearInPDF

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
outPath = "U:/Phil_Read/CSR_Europe/unzipped_country_year/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2
unzipDirs = [f for f in listdir(unzipPath) if not (isfile(join(unzipPath, f)) )]

#print(len(unzipDirs), 'unzipped')

if not exists(outPath):
    mkdir(outPath)

fout = open('years.csv','w')
fout.write('country,sourcefile,year,sic,isin,copy\n')

for unzipDir in unzipDirs:
    if not unzipDir.startswith('ZZ_'):
        print(unzipDir)
        files = [f for f in listdir(join(unzipPath, unzipDir)) if (isfile(join(unzipPath, unzipDir ,f)) )]
        print (len(files), 'files')
        for file in files:
            if file.endswith('.pdf'):
                # Get year from first page of PDF
                path = join(unzipPath, unzipDir, file)
                year = -2
                try:
                    year = findModeYearInPDF(path)
                    print (file, year)
                except Exception as e:
                    year = -1
                    print (file, 'could not open')
                # Generate new filename and copy
                country = unzipDir
                company = companies.getCompanyByBBFilename(country, file)
                sic = company.sic
                isin = company.isin
                reporttype = 'CR' # Only this for now
                # Try out filenames that do not exist
                # (there are multiple reports for some ticker/year/country)
                copycount = 0
                outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
                #print(outfilename)
                while isfile(join(outPath, country+'/'+str(year)+'/'+outfilename)):
                    # Increment suffix until no overwriting possible
                    copycount += 1
                    outfilename = sic + '_' + isin + '_' + reporttype +str(copycount)+'.pdf'
                
                outfilepath =  join(outPath, country+'/'+str(year)+'/'+outfilename)
                if not exists(join(outPath, country)):
                    mkdir(join(outPath, country))
                if not exists(join(outPath, country+'/'+str(year))):
                    mkdir(join(outPath, country+'/'+str(year)))
                copy2(path , outfilepath)
                
                # Update log
                fout.write(country + ',' + file + ',' + str(year) + ',' + str(sic) + ',' + isin + ',' + str(copycount) + '\n')
                
fout.close()