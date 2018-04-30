#!/usr/bin/python    

# work out best year, add columns to stats table, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = True

statsPathIn  = 'stats43EU.csv' if isEurope else 'stats43UK.csv'
statsPathOut = 'stats45EU.csv' if isEurope else 'stats45UK.csv'


#Load stats43.csv to dataframe df; fill blanks with ''.
import pandas as pd
df = pd.read_csv(statsPathIn)
df.fillna('',inplace=True) # replace any blank (nan) with empty string, eg filenametxt

#Function getBestYear(metayear, minedyear, uploadyear)
def getBestYear(metayear, minedyear, uploadyear):
    bestyear = 0
    #If `metayear` is found, and is less than or equal to `uploadyear`, choose `metayear`.
    if metayear and metayear > 0 and metayear <= uploadyear:
        bestyear = metayear
	# Else if `minedyear` is found, and is less than or equal to `uploadyear`, choose `uploadyear`.
    elif minedyear and minedyear > 0 and minedyear <= uploadyear:
        bestyear = minedyear
	# Else give up (value -1)
    else:
        bestyear = -1
    return bestyear

#Function getYearSource(same)
def getYearSource(metayear, minedyear, uploadyear):
    yearsource = 0
    #If `metayear` is found, and is less than or equal to `uploadyear`, choose `metayear`.
    if metayear and metayear > 0 and metayear <= uploadyear:
        yearsource = 10
	# Else if `minedyear` is found, and is less than or equal to `uploadyear`, choose `uploadyear`.
    elif minedyear and minedyear > 0 and minedyear <= uploadyear:
        yearsource = 20
	# Else give up
    else:
        yearsource = -1
    return yearsource
    
#Apply getBestYear function to dataframe, save new column bestyear.
df['bestyear'] = df.apply(lambda x: getBestYear(x['metayear'], x['minedyear'], x['uploadyear']), axis=1)

#Apply getYearSource function to dataframe, save new column yearsource.
df['yearsource'] = df.apply(lambda x: getYearSource(x['metayear'], x['minedyear'], x['uploadyear']), axis=1)

#Save df to stats45.csv.
df.to_csv(statsPathOut, index=False, encoding='utf-8')
