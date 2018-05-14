#!/usr/bin/python    

# Updated 2017-10-02: Now reads from flat directory of TXT reports
# with the original filenames from Bloomberg.

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import PyPDF2
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import codecs

from os.path import join

unzipPath = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/"
statsPathIn = 'statsUK.csv'
statsPathOut = 'statsUK_lang.csv'
logPath = 'logUK_lang.csv'
with open(logPath, 'w') as logFile:
    logFile.write('sourcefile, lang\n')

def getPlainTextFromTXTPath(path):
    text = u''
    with codecs.open(path, 'r', encoding='utf8', errors='ignore') as fileIn:
        text = fileIn.read()
    return text
    
# Detect the language of the report
def getLang(reporttype,sourcefile,destfile,bestyear):
    # We are now using txt versions of reports, not PDF
    # At this time, the txt reports use destname.txt, not sourcename.pdf
    #filename = sourcefile.replace('.pdf','.txt') # LATER
    filename = str(bestyear) + '_' + destfile.replace('.pdf','.txt')
    filenamesToSkip = [
        ]
    if filename in filenamesToSkip:
        return '-2' # corrupt file
    if not (filename.endswith('.txt')):
        return '-3' # only interested in txt reports
        
    fullPath = join(unzipPath, filename)
    print ('Reading: ' + fullPath)
    
    textToTest = u''
    try:
        if filename.endswith('.txt'):
            textToTest = getPlainTextFromTXTPath(fullPath)
    except IOError as ioe:
        print ('Error reading from: ' + fullPath)
        lang = '-4'
        with open(logPath, 'a') as logFile:
            logFile.write(sourcefile+','+lang+'\n')
        return lang
    try:
        # Do the language detection
        lang = detect(textToTest)
    except LangDetectException:
        lang = '-1'
    print ('Detected: ' + lang)
    
    with open(logPath, 'a') as logFile:
        logFile.write(sourcefile+','+lang+'\n')
    return lang

# Open stats file which contains all filenames.
# For each file, get language, add to table.
# Use the raw unzipped directory, but could be adapted for the other
# Save table with next extra column.

# Read in all columns to a dataframe.
df = pd.read_csv(statsPathIn)
#   The lambda function is used so getLang is applied to all rows,
#   creating a new lang column as output.
df['lang'] = df.apply(lambda x: getLang(x['reporttype'], x['sourcefile'], x['destfile'], x['bestyear']), axis=1)
# Save the file back out (several hours later) with all original columns + 1
df.to_csv(statsPathOut, index=False, sep=',')
