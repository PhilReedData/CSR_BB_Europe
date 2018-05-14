#!/usr/bin/python 

# x_EUCSRtxt_dropdirty.py
# 2017-10-06 email from Irina, remove lost files and htm from set
# until conversion is improved

from os import listdir, mkdir, makedirs, remove
from os.path import isfile, join, exists

reportsDir = "U:/Phil_Read/fromIrina/Europe_CSR_txt_dropdirty/"
reportsDirEn = "U:/Phil_Read/fromIrina/Europe_CSR_txt_trns_dropdirty/"
dirtyPDFsPath = "U:/Phil_Read/fromIrina/2017-10-11/files_lost.csv"
dirtyImgPDFsPath = "U:/Phil_Read/fromIrina/2017-10-11/image_like_pdfs.csv"
dirtyHTMsPath = "U:/Phil_Read/fromIrina/2017-10-11/htm_files.csv"
keptReportsPath = "U:/Phil_Read/fromIrina/2017-10-11/kept_files.csv"
keptReportsPathEn = "U:/Phil_Read/fromIrina/2017-10-11/kept_files_en.csv"

# PHASE 1: Copy all reports to new directory
# (Done this in File Explorer: copy/paste directory, remove non-report files)

# PHASE 2: DROP DIRTY FILES
# read dirty lists, skip header
dirtyPDFs = open(dirtyPDFsPath,'r').read().strip().split('\n')[1:]
print(len(dirtyPDFs), 'dirty PDFs')
# example member: "./010610_MRK_Corporate_Responsibility_SD000000001993077252.pdf"

dirtyImgPDFs = open(dirtyImgPDFsPath,'r').read().strip().split('\n')[1:]
print(len(dirtyImgPDFs), 'dirty image-like PDFs')

dirtyHTMs = open(dirtyHTMsPath,'r').read().strip().split('\n')[1:]
print(len(dirtyHTMs), 'dirty HTMs')

# reduce filenames to stems (drop extension .pdf or .txt)
# some filenames begin "./" so drop that too.
dirtyPDFsStems = [i[2:i.rindex('.')] for i in dirtyPDFs]
dirtyImgPDFsStems = [i[:i.rindex('.')] for i in dirtyImgPDFs]
dirtyHTMsStems = [i[2:i.rindex('.')] for i in dirtyHTMs]
# concatenate lists
dirtyStems = dirtyPDFsStems + dirtyImgPDFsStems + dirtyHTMsStems

# read files in Dir
files = [f for f in listdir(reportsDir) if isfile(join(reportsDir, f))]
files.sort()
print (len(files), 'files')

filesEn = [f for f in listdir(reportsDirEn) if isfile(join(reportsDirEn, f))]
filesEn.sort()
print (len(filesEn), 'filesEn')

def deleteDirtyFiles(files, reportsDir):
    print ('Deleting dirty files from ' + reportsDir)
    # For each file in dir
    for file in files:
        # get name stem (ie drop .pdf .txt)
        stem = file[:file.rindex('.')]
        # if stem in dirty list, delete
        if stem in dirtyStems:
            remove(join(reportsDir, file))

# The action follows (commented out after completion, so we can skip to Phase 3            

deleteDirtyFiles(files, reportsDir)
files = [f for f in listdir(reportsDir) if isfile(join(reportsDir, f))]
print (len(files), 'files') 
# Write list of files out
open(keptReportsPath,'w').write("\n".join(files))

# Repeat for translated reports
deleteDirtyFiles(filesEn, reportsDirEn)
filesEn = [f for f in listdir(reportsDirEn) if isfile(join(reportsDirEn, f))]
print (len(filesEn), 'filesEn') 
open(keptReportsPathEn,'w').write("\n".join(filesEn))

# PHASE 3: PRUNE THE STATS TABLE
#Go through stats table, drop rows which are not in dir
