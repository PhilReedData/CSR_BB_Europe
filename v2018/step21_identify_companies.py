#!/usr/bin/python    

# load company details, add these columns to stats table in the right places, matching filename

### Change this True/False to run Europe or UK version of code. ###
isEurope = False

statsPathIn  = 'stats13EU.csv' if isEurope else 'stats13UK.csv'
statsPathOut = 'stats21EU.csv' if isEurope else 'stats21UK.csv'

# Load the master companies object
import utilReadExcelCSR
companies = utilReadExcelCSR.loadCompanies(isEurope)

# Load stats dataframe
import pandas as pd
df = pd.read_csv(statsPathIn)

# Match filename to company. Return field of (companyname, tickerfull, isin, sic)
def matchCompany(filenamefull, countries, field):
    firstCountry = countries[:2] # just use first country if multiple
    company = companies.getCompanyByBBFilename(firstCountry, filenamefull)
    fields = {
        'companyname': company.name,
        'tickerfull' : company.tickerFull,
        'isin'       : company.isin,
        'sic'        : company.sic
    }
    return fields[field]

# Apply matching function, once for each field (cannot create multiple cols at once)
fieldsToMatch = ['companyname', 'tickerfull', 'isin' , 'sic']
for field in fieldsToMatch:
    df[field] = df.apply(lambda x: matchCompany(x['filenamefull'], x['countries'], field), axis=1)

# Save dataframe to new csv statsOut
df.to_csv(statsPathOut, index=False, encoding='utf-8')
