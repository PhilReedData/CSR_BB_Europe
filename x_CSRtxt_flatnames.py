#!/usr/bin/python    

# x_CRtxt_flatnames.py
# Rename given list of directories of text and html files to remove the year directory.
# Adding feature to translate to English if required.
# LATEST: translation document limit is 15k characters. Ours are larger. 
#   Need to break them up, sensibly.
# NOTE: will adapt this once the input format changes.
# 2017-09-18

# Get list of directories
# For each directory
    # Get list of files
    # For each file
        # New filename is year_oldfilename
        # Copy file


from os import listdir, mkdir, makedirs
from os.path import isfile, join, exists
from shutil import copyfile, copy2
import time
import codecs

doTranslate = True
# If doTranslate, do we copy the non-translated reports too?
copyNonTranslated = True

parentPathIn = "U:/Phil_Read/CSR_UK_latest_txt_all/"
yearDirs = [
    "1999", "2000", "2001", "2002", "2003", "2004", "2005",
    "2006", "2007", "2008", "2009", "2010", "2011", "2012", 
    "2013", "2014", "2015", "2016"
    ]
parentPathOut = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/"
if doTranslate:
    parentPathOut = "U:/Phil_Read/CSR_UK_latest_txt_all_flat_trns/"

if not exists(parentPathOut):
    makedirs(parentPathOut)

# Use the langdect results in dict of outFilePath -> lang
import utilReadXLangdetectCSV
langDict = utilReadXLangdetectCSV.getLangDictFromCSV()
import utilTranslate

# For each year
for yearDir in yearDirs:
    # Get all files
    inFiles = [f for f in listdir(join(parentPathIn, yearDir)) if isfile(join(parentPathIn+yearDir, f))]
    inFiles.sort()
    print (yearDir, len(inFiles))
    for inFilePath in inFiles:
        inFullPath = join(parentPathIn+yearDir, inFilePath)
        # New name, eg 1999_10_GB00B03MLX29_CR1.txt
        outFilePath = yearDir + '_' + inFilePath
        outFullPath = join(parentPathOut+outFilePath)
        lang = langDict[outFilePath]
        try:
            if (doTranslate and lang != 'en'):
                # Translate file, save to new destination
                # Read the file to text
                foreignText = ""
                with codecs.open(inFullPath, 'r', encoding='utf8', errors='ignore') as fileIn:
                    foreignText = fileIn.read()
                # Do translation, don't overload server
                chars = str(len(foreignText))
                print('Pausing 1 second before translating ' + chars +' chars from ' + lang)
                time.sleep(1)
                englishText = utilTranslate.translateToEn(foreignText)
                # Save the new text
                with codecs.open(outFullPath, 'w', encoding='utf8', errors='ignore') as fileOut:
                    fileOut.write(englishText)
            else:
                # Copy file
                if (copyNonTranslated or not doTranslate):
                    copy2(inFullPath, outFullPath)
        except IOError as e:
            import sys
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            print ('Could not write to ' + outFullPath)
            print ('Lang = ' + lang + ', doTranslate = ' + str(doTranslate))