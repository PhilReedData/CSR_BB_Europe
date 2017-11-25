#!/usr/bin/python   
# Mine the documents for most frequent year 

corruptFiles = [
    ]

SEP = ','

import utilGetYearFromTXT
from utilGetYearFromTXT import findModeYearsInTXT

txtDir = "U:/Ser-Huang_Poon/Europe_CSR/Europe_CSR_txt_trns/"

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile, copy2

fout = open('yearstxt.csv','w')
fout.write('sourcefile'+ SEP + 'minedyear150' + SEP + 'minedyear2000\n')

print(txtDir)
# Get list of files in txtDir
files = [f for f in listdir(txtDir) if (isfile(join(txtDir,f)) )]
files.sort()
print (len(files), 'files')
for file in files:
    if file.endswith('.txt') and (not file in corruptFiles):
        print (file)
        # Get year from first so many characters of TXT
        path = join(txtDir, file)
        years = (-2,-2)
        try:
            years = findModeYearsInTXT(path)
            #print (file, year)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            years = (-1, -1)
            print ('Could not read file: ' + file)

        # Update log
        fout.write(file + SEP + str(years[0]) + SEP + str(years[1]) + '\n')
    
fout.close()