#!/usr/bin/python    

# Copy and rename converted txt files

fromPath = "U:/Martin_Carpenter/CSR_Report_Conversion/European_CSR_Reports_Txt_Format/"
toPath = "U:/Phil_Read/CSR_Europe/txt_allinone/"
head = 'RTF_Format'

#foundTxts = Read list of directory of txt files
from os import listdir
from os.path import isfile, join
# Produce a list of all .txt files in the given directory.
foundTxts = [f for f in listdir(fromPath) if (isfile(join(fromPath, f)) and f.startswith(head))]
foundTxts.sort()

# copy these, dropping the head of the filename for each
from shutil import copy2
for txtFile in foundTxts:
    # txtFile[len(head):] means 'RTF_Format123.txt' becomes '123.txt'
    copy2(join(fromPath, txtFile), join(toPath, txtFile[len(head):]))
    print("Copied",txtFile)