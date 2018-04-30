#!/usr/bin/python    

# get mined year, add column to stats table, matching filename
# Could extend it to not perform mining on a report that has already been mined.

### Change this True/False to run Europe or UK version of code. ###
isEurope = True

statsPathIn  = 'stats41EU.csv' if isEurope else 'stats41UK.csv'
statsPathIn  = 'stats31EU.csv' if isEurope else 'stats31UK.csv' # TEMP
statsPathOut = 'stats43EU.csv' if isEurope else 'stats43UK.csv'
logPath = 'log43EU.csv' if isEurope else 'log43UK.csv' # in case of crash

txtPathEU = 'U:/Ser-Huang_Poon/Europe_CSR/Europe_CSR_txt_all/'
txtPathUK = 'U:/Phil_Read/CSR_UK/txt_allinone/'
txtPath   = txtPathEU if isEurope else txtPathUK

import utilGetYearFromTXT

#Load stats 41.csv to dataframe df.
import pandas as pd
df = pd.read_csv(statsPathIn)
df.fillna('',inplace=True) # replace any blank (nan) with empty string, eg filenametxt
log = open(logPath,'w')
log.write('filenamefull,filenametxt,minedyear\n')

#Function getMinedYear(filenametxt)
#	Call utility file
#	Return minedyear
def getMinedYear(filenamefull, filenametxt):
    year = ''
    if len(filenametxt) > 0:
        year = utilGetYearFromTXT.findModeYearInTXTLim2only(txtPath + filenametxt)
    log.write(filenamefull + ',' + filenametxt + ',' +str(year) + '\n') 
    return year

#Apply getMinedYear function to dataframe, save new column minedyear.
df['minedyear'] = df.apply(lambda x: getMinedYear(x['filenamefull'], x['filenametxt']), axis=1)

#Save df to stats43.csv.
df.to_csv(statsPathOut, index=False, encoding='utf-8')
log.close()
