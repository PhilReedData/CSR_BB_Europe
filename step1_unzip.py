#!/usr/bin/python    

# Unzip everything from "U:\Ser-Huang_Poon\CSR_Europe\*.zip"
# to "U:\Phil_Read\CSR_Europe\unzipped_raw\"

import utilCSR

zipPath = "U:/Ser-Huang_Poon/CSR_Europe/"
unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"

from os import listdir
from os.path import isfile, join
zipfiles = [f for f in listdir(zipPath) if (isfile(join(zipPath, f)) )]

import zipfile
import os.path
for zip in zipfiles:
    extractFolder = utilCSR.getIsoFromString(zip)
    extractPath = os.path.abspath(os.path.join(unzipPath, extractFolder))
    try:
        if zip.startswith('IBEX2013_'): # Error in this file for now
            zipfile.ZipFile(zipPath + zip).extractall(extractPath)
    except zipfile.BadZipfile as e:
        import sys
        print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        print('File:' + zip)
        raise e