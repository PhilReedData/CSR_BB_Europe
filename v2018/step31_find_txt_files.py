#!/usr/bin/python    

# find txt files, add these columns to stats table in the right places, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = False

statsPathIn  = 'stats21EU.csv' if isEurope else 'stats21UK.csv'
statsPathOut = 'stats31EU.csv' if isEurope else 'stats31UK.csv'

txtPathEU = 'U:/Ser-Huang_Poon/Europe_CSR/Europe_CSR_txt_all/'
txtPathUK = 'U:/Phil_Read/CSR_UK/txt_allinone/'
txtPath   = txtPathEU if isEurope else txtPathUK

#foundTxts = Read list of directory of txt files
from os import listdir
from os.path import isfile, join
# Produce a list of all .txt files in the given directory.
foundTxts = [f for f in listdir(txtPath) if (isfile(join(txtPath, f)) and f.endswith('.txt'))]
foundTxts.sort()

#	Load dataframe from stats31.csv 
import pandas as pd
df = pd.read_csv(statsPathIn)

#	Function getFilenameTxt(filenameshort)
#		Look for filenameshort + ".txt" in foundTxts
#		Return this filename, else blank.
def getFilenameTxt(filenameshort):
    filenametxt = ''
    if filenameshort + '.txt' in foundTxts:
        filenametxt = filenameshort + '.txt'
    return filenametxt

#	Apply function getFilenameTxt to dataframe, new col filenametxt
df['filenametxt'] = df.apply(lambda x: getFilenameTxt(x['filenameshort']), axis=1)

#	Save dataframe to stats31.csv
df.to_csv(statsPathOut, index=False, encoding='utf-8')