#!/usr/bin/python    

# translate non-English to English, add column to stats table, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = True

statsPathIn  = 'stats51EU.csv' if isEurope else 'stats51UK.csv'
statsPathOut = 'stats53EU.csv' if isEurope else 'stats53UK.csv'
logPath = 'log53EU.csv' if isEurope else 'log53UK.csv' # in case of crash

txtPathEU = 'U:/Phil_Read/CSR_Europe/txt_allinone/'
txtPathUK = 'U:/Phil_Read/CSR_UK/txt_allinone/'
txtPath   = txtPathEU if isEurope else txtPathUK

txtTransPathEU = 'U:/Phil_Read/CSR_Europe/txt_allinone_trans/'
txtTransPathUK = 'U:/Phil_Read/CSR_UK/txt_allinone_trans/'
txtTransPath   = txtTransPathEU if isEurope else txtTransPathUK

#Load stats51.csv to dataframe df; fill blanks with ''.
import pandas as pd
df = pd.read_csv(statsPathIn)
df.fillna('',inplace=True) # replace any blank (nan) with empty string, eg filenametxt
log = open(logPath,'w')
log.write('filenamefull,filenametxttrans\n')

from os.path import isfile, join, exists, getsize
from shutil import copy2
import utilTranslate

#Function callTranslate(filenamefull, filenametxt, lang)
#	If filenametxt exists and lang <> en, Call utility
def callTranslate(filenamefull, filenametxt, lang):
    filenametxttrans = ''
    if len(filenametxt) > 0:
        # Skip if file already translated/copied # NOT YET TESTED
        filenametxttransExisting = filenametxt[:-4] + '.tran.txt'
        if isfile(join(txtTransPath, filenametxttransExisting)):
            return filenametxttransExisting
        filenametxttransExisting = filenametxt[:-4] + '.orig.txt'
        if isfile(join(txtTransPath, filenametxttransExisting))
            return filenametxttransExisting
            
        size = getsize(join(txtPath,filenametxt))
        MIN_SIZE = 64 # bytes
        if len(lang) > 1 and lang != 'en' and lang != '-1' and size>MIN_SIZE:
            # do translate 
            print ('Translating ' + txtPath + filenametxt)
            foreignText = utilTranslate.loadFile(join(txtPath, filenametxt))
            try:
                resultText = utilTranslate.translateInChunks(foreignText)
                charsOut = str(len(resultText))
                print ('Writing ' + charsOut + ' character(s).')
                # Replace the file extension from .txt to .tran.txt
                filenametxttrans = filenametxt[:-4] + '.tran.txt'
                utilTranslate.writeFile(resultText, join(txtTransPath,filenametxttrans))
            except ValueError:
                import sys
                filenametxttrans = '_ERROR ON LINE ' + str(sys.exc_info()[-1].tb_lineno)
                print ('Error translating. Skipping.')
        elif lang == 'en' and size>MIN_SIZE:
            # Copy the file to .orig.txt
            print ('Copying already English file ' + filenametxt)
            filenametxttrans = filenametxt[:-4] + '.orig.txt'
            copy2(join(txtPath,filenametxt), join(txtTransPath,filenametxttrans))
        else:
            print ('Not copying ' + filenametxt)
    log.write(filenamefull + ',' + filenametxttrans + '\n')    
    return filenametxttrans

#Apply function callTranslate to df, save new column filenametxttrans.
df['filenametxttrans'] = df.apply(
    lambda x: callTranslate(x['filenamefull'], x['filenametxt'], x['lang']), axis=1
)

# Add summary column to easily see what was translated or not # NOT TESTED
def summarizeTranslate(filenametxttrans):
    summary = ""
    if filenametxttrans.endswith('.tran.txt'):
        summary = "Translated to English txt"
    elif filenametxttrans.endswith('.orig.txt'):
        summary = "Already English txt"
    elif filenametxttrans.startswith('_ERROR'):
        summary = "Error translating txt"
    else:
        summary = "No txt to translate"
    return summary
df['translated'] = df.apply(lambda x: summarizeTranslate(x['filenametxttrans']), axis=1)
    
#Save df to stats53.csv.
df.to_csv(statsPathOut, index=False, encoding='utf-8')
log.close()
