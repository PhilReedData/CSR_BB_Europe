#!/usr/bin/python    
# utilReadXLangdectectCSV
# Read the CSV file produced by script x_CRtxt_langdectect.py
# Produce a dict of flatfilename to lang
# 2017-09-19
import csv
def getLangDictFromCSV(csvIn="x_CSRtxt_langdectect.csv"):
    cr = csv.reader(open(csvIn, 'rb'))
    header = cr.next()
    langDict = {}
    for row in cr:
        year = str(row[0])
        filename = row[1]
        lang = row[2]
        key = year + '_' + filename
        langDict[key] = lang
    return langDict
        
