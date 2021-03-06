#!/usr/bin/python 

# Util ReadExcelCSREurope

from xlrd import open_workbook

# I wrote this to store the imported data in Python Classes Companies and Company. 
# It now appears that it might be more efficient as a Panda DataFrame.

# Bloomberg filename includes Ticker between 1st and 2nd _
def getTickerFromBBFilename(filename):
    if '_' not in filename:
        return ('_TICKER NOR UNDERSCORE FOUND_' + filename)
    start = filename.index('_')
    end = start + filename[start+1:].index('_')
    ticker = '_TICKER_NOT_FOUND_'
    if start > 0 and end > start:
        ticker = filename[start+1:end+1]
    else:
        print('Ticker not found: ' + filename)# + ', start = ' + str(start) + ', end = ' + str(end))
    return ticker

class Company(object):
    def __init__(self, tickerFull, name, disclosure, constitCountry, isin, sic, sicName):
        self.indexCountry = ''
        self.tickerFull = tickerFull
        self.name = name
        self.disclosure = disclosure
        self.constitCountry = constitCountry
        self.isin = isin
        try:
            # Is the sic a valid integer? If so, keep it (as String)
            int(sic)
            self.sic = sic
        except Exception:
            # For anything else:
            self.sic = '99'
        self.sicName = sicName
        self.year = -1
    
    def setIndexCountry(self, indexCountry):
        self.indexCountry = indexCountry
        
    def getIndexCountry(self):
        return self.indexCountry
    
    def getTickerShort(self):
        # Remove slash or slashA from tickerFull,
        # because it's not present in the report filenames.
        tickerFullNoSlash = self.tickerFull.replace('/','')
        try:
            tickerShort = tickerFullNoSlash[:tickerFullNoSlash.index(' ')]
        except ValueError:
            tickerShort = "ERROR"
        return tickerShort
    
    def setYear(self, year):
        self.year = year
    
    def __str__(self):
        return("Company object:\n"
               "  indexCountry = {0}\n"
               "  tickerFull = {1}\n"
               "  name = {2}\n"
               "  disclosure = {3}\n"
               "  constitCountry = {4}\n"
               "  isin = {5} \n"
               "  sic = {6} \n"
               "  sicName = {7} \n"
               "  year = {8}"
               .format(self.indexCountry, self.tickerFull, self.name, self.disclosure,
                       self.constitCountry, self.isin, self.sic, self.sicName, self.year))


class Companies(object):
    def __init__(self, companies):
        self.companies = companies
        # dict of indexCountry -> (sub)list of companies
        self.companiesByIndexCountry = {}
        self.noneCompany = Company('UNKNOWN', 'UNKNOWN', '0', 'ZZ', 'UNKNOWN', '0', 'UNKNOWWN')
        
    def getAllCompanies(self):
        return self.companies
    
    def getCompaniesByIndexCountry(self, indexCountry):
        if indexCountry not in self.companiesByIndexCountry.keys():
            # If not requested before, create this sublist
            someCompanies = []
            for company in self.companies:
                if company.getIndexCountry() == indexCountry:
                    someCompanies.append(company)
            self.companiesByIndexCountry[indexCountry] = someCompanies
        # Return the (sub) list, regardless of generated this time or prior
        return self.companiesByIndexCountry[indexCountry]
    
    # Look through companies list for this index country. Return first match, else None.
    def getCompanyByTicker(self, indexCountry, ticker):
        for company in self.getCompaniesByIndexCountry(indexCountry):
            if company.getTickerShort() == ticker:
                return company
        return self.noneCompany
        
    def getCompanyByBBFilename(self, indexCountry, filename):
        return self.getCompanyByTicker(indexCountry, getTickerFromBBFilename(filename))
    
    def __str__(self):
        return("Companies object:\n"
               "  number of companies = {0}"
               .format(len(self.companies)))
        
companiesByCountry = {}
allCompanies = []


wb = open_workbook("U:/Ser-Huang_Poon/20170717c_EuropeCSR.xlsx")
for sheet in wb.sheets()[1:16]:
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    sheet_name = sheet.name
    index_country = sheet_name[sheet_name.index('.')+1:]

    items = []

    rows = []
    for row in range(3, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = Company(*values)
        item.setIndexCountry(index_country)
        items.append(item)
        allCompanies.append(item)
    companiesByCountry[index_country] = items
    #print (len(companiesByCountry), 'countries', len(items), 'more items', type(items), 'type')
companies = Companies(allCompanies)
    
#print ("Last two imports:")
#for item in items[:-2]:
#    print item
#    print("Accessing one single value (eg. indexCountry): {0}".format(item.indexCountry))
#print(len(items), 'items')
print(len(companiesByCountry), 'countries imported') # VARIABLE DOES NOT WORK!
print(len(allCompanies), 'companies imported')
print(companies)

# DOES NOT WORK! Why does type change from list to unicode?
#for country in companiesByCountry:
#    print (country, 'country', len(country), 'recalled items', type(country), 'type')

#for company in allCompanies[:2]:
#    print(company.getTickerShort())

fi = 'FI'
print(len(companies.getCompaniesByIndexCountry(fi)), fi)

countrytest = 'CH'
filenametest = "122908_ADEN_Corporate_Responsibility_WD000000000096636192.pdf"
tickertest = getTickerFromBBFilename(filenametest)
print(tickertest, 'ADEN')
companytest = companies.getCompanyByBBFilename(countrytest, filenametest)
print (companytest)

countrytest = 'NO'
filenametest = "122908_XXXXX_Corporate_Responsibility_WD000000000096636192.pdf"
companytest = companies.getCompanyByBBFilename(countrytest, filenametest)
print (companytest)
