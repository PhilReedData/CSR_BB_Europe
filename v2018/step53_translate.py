#!/usr/bin/python    

# translate non-English to English, add column to stats table, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = False

statsPathIn  = 'stats51EU.csv' if isEurope else 'stats51UK.csv'
statsPathOut = 'stats53EU.csv' if isEurope else 'stats53UK.csv'
logPath = 'log53EU.csv' if isEurope else 'log53UK.csv' # in case of crash

txtPathEU = 'U:/Ser-Huang_Poon/Europe_CSR/Europe_CSR_txt_all/'
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


#Function callTranslate(filenamefull, filenametxt, lang)
#	If filenametxt exists and lang <> en, Call utility
def callTranslate(filenamefull, filenametxt, lang):
    filenametxttrans = ''
    if len(filenametxt) > 0 and lang != 'en' and lang != '-1':
        ...do translate # maybe skip tiny files too
    return filenametxttrans

#Apply function getLang to df, save new column filenametxttrans.
df['filenametxttrans'] = df.apply(
    lambda x: getLang(x['filenamefull'], x['filenametxt'], x['lang']), axis=1
)


#Save df to stats53.csv.
df.to_csv(statsPathOut, index=False, encoding='utf-8')
log.close()


