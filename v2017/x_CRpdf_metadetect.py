#!/usr/bin/python    

# x_CRpdf_metadetect.py
# Extract the meta creation date for a given directory of pdf files.
# 2017-11-25

import codecs
from os import listdir, mkdir
from os.path import isfile, join, exists
import utilGetYearFromPDF

# Change which of these lines are uncommented and re-run
parentPathIn = "U:/Ser-Huang_Poon/UK_CRunzip/"
logPath = "x_CRpdf_metadetect.csv"
#parentPathIn = "U:/Ser-Huang_Poon/UK_ARunzip/"
#logPath = "x_ARpdf_metadetect.csv"
#parentPathIn = "U:/Ser-Huang_Poon/UK_ESGunzip/"
#logPath = "x_ESGpdf_metadetect.csv"

logFile = open(logPath, 'w')
SEP = ','
# Header
logFile.write('filename'+SEP+'creation\n')

# Get all files
files = [f for f in listdir(parentPathIn) if isfile(join(parentPathIn, f))]
files.sort()
print ('Files', len(files))
for filePath in files:
    fullPath = join(parentPathIn, filePath)
    data = ""
    creation = ''
    if filePath.endswith('.pdf'):
        creation = utilGetYearFromPDF.getPDFMetaCreationYear(fullPath, getWholeDate=True)
    print(filePath, creation)
    logFile.write(filePath + SEP + str(creation) + '\n')
logFile.close()
