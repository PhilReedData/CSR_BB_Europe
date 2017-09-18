#!/usr/bin/python    

# x_CRtxt_flatnames.py
# Rename given list of directories of text and html files to remove the year directory.
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

parentPathIn = "U:/Phil_Read/CSR_UK_latest_txt_all/"
yearDirs = [
    "1999", "2000", "2001", "2002", "2003", "2004", "2005",
    "2006", "2007", "2008", "2009", "2010", "2011", "2012", 
    "2013", "2014", "2015", "2016"
    ]
parentPathOut = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/"

if not exists(parentPathOut):
    makedirs(parentPathOut)

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
        try:
            # Copy file
            copy2(inFullPath, outFullPath)
        except IOError as e:
            import sys
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            print ('Could not write to ' + outFullPath)