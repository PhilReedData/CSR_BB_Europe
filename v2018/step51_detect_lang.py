#!/usr/bin/python    

# work out language, add column to stats table, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = True

statsPathIn  = 'stats45EU.csv' if isEurope else 'stats45UK.csv'
statsPathOut = 'stats51EU.csv' if isEurope else 'stats51UK.csv'
logPath = 'log51EU.csv' if isEurope else 'log51UK.csv' # in case of crash

txtPathEU = 'U:/Ser-Huang_Poon/Europe_CSR/Europe_CSR_txt_all/'
txtPathUK = 'U:/Phil_Read/CSR_UK/txt_allinone/'
txtPath   = txtPathEU if isEurope else txtPathUK

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import codecs
from os import listdir, mkdir
from os.path import isfile, join, exists

#Load stats51.csv to dataframe df; fill blanks with ''.
import pandas as pd
df = pd.read_csv(statsPathIn)
df.fillna('',inplace=True) # replace any blank (nan) with empty string, eg filenametxt
log = open(logPath,'w')
log.write('filenamefull,filenametxt,lang\n')

#Function getLang(filenamefull, filenametxt)
#	Calls utility
def getLang(filenamefull, filenametxt):
    lang = ''
    if len(filenametxt) > 0:
        fullPath = join(txtPath, filenametxt)
        data = ""
        with codecs.open(fullPath, 'r', encoding='utf8', errors='ignore') as file:
            data = file.read()
        try:
            lang = detect(data)
        except LangDetectException:
            lang = '-1'
    print(filenametxt, lang)
    log.write(filenamefull + ',' + filenametxt + ',' + lang + '\n')
    return lang

#Apply function getLang to df, save new column lang.
df['lang'] = df.apply(lambda x: getLang(x['filenamefull'], x['filenametxt']), axis=1)

#Save df to stats51.csv.
df.to_csv(statsPathOut, index=False, encoding='utf-8')
log.close()
