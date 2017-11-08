#!/usr/bin/python    

# step5_translate
from os import makedirs
from os.path import exists
from shutil import copy2

import utilTranslate

# Read in list to translate, save back
fromDir = "U:/Phil_Read/fromIrina/2017-10-27/Europe_CSR_txt_all/"
toDir = "U:/Phil_Read/fromIrina/2017-10-27/Europe_CSR_txt_trns/"
listPath = "U:/Phil_Read/fromIrina/2017-10-27/x_toBeTranslated.txt"
englishPath = "U:/Phil_Read/fromIrina/2017-10-27/x_english.txt"
successPath = "U:/Phil_Read/fromIrina/2017-10-27/x_translated.txt"
copiedPath = "U:/Phil_Read/fromIrina/2017-10-27/x_copied.txt"
failPath = "U:/Phil_Read/fromIrina/2017-10-27/x_failTranslated.txt"
if not exists(toDir):
    makedirs(toDir)
foreignReports = open(listPath,'r').read().split('\n')
englishReports = open(englishPath,'r').read().split('\n')
for filename in foreignReports: 
    # If filename matches
    if filename in englishReports:
        # Skip translation if already in English
        print ('Skipping translation for English ' + filename)
        copy2(fromDir + filename, toDir + filename)
        open(copiedPath, 'a').write(filename + '\n')
        continue
    try:
        print ('Read from ' + fromDir + filename)
        foreignText = utilTranslate.loadFile(fromDir + filename) # should use os join
        resultText = utilTranslate.translateInChunks(foreignText)
        charsOut = str(len(resultText))
        print ('Writing ' + charsOut + ' character(s).')
        utilTranslate.writeFile(resultText, toDir+filename)
        # Write log
        open(successPath, 'a').write(filename + '\n')
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print ('Could not read/translate/save ' + filename)
        open(failPath, 'a').write(filename + '\n')