#!/usr/bin/python 

# Util ReadExcelCSREurope

from xlrd import open_workbook

class Company(object):
    def __init__(self, tickerFull, name, disclosure, constitCountry, isin, sic, sicName):
        self.indexCountry = ''
        self.tickerFull = tickerFull
        self.name = name
        self.disclosure = disclosure
        self.constitCountry = constitCountry
        self.isin = isin
        self.sic = sic
        self.sicName = sicName
        self.year = -1
    
    def setIndexCountry(self, indexCountry):
        self.indexCountry = indexCountry
    
    def getTickerShort(self):
        return self.tickerFull[:self.tickerFull.index(' ')]
    
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
