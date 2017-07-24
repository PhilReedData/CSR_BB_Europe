#!/usr/bin/python    

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import pyPdf
from pyPdf.utils import PdfReadError

import pandas as pd
import numpy as np

from os.path import join

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
statsPathIn = 'stats.csv'
statsPathOut = 'stats_lang.csv'

# Get the text of first 5 pages of given PDF file.
def getTextContentOfPdfPages(path, num_pages=5):
    content = ""
    p = file(path, "rb")
    try:
        pdf = pyPdf.PdfFileReader(p)
    except PdfReadError:
        print ('Error reading file: ' + path)
        return content # can't open file.
    for i in range(0, num_pages):
        try:
            content += pdf.getPage(i).extractText() + "\n"
        except Exception:
            print ('Problem reading page '+ str(i+1) +': ' + path)
            pass # may not be that many pages!
    #content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content
    
# Detect the language of the report
def getLang(country,filename):
    if filename == "072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf":
        return '-1' # corrupt file

    fullPath = join(unzipPath, country + '/' + filename)
    print ('Reading: ' + fullPath)
    page1text = getTextContentOfPdfPages(fullPath)
    try:
        lang = detect(page1text)
    except LangDetectException:
        lang = '-1'
    print ('Detected: ' + lang)
    return lang

# Open stats file which contains all filenames.
# For each file, get language, add to table.
# Use the raw unzipped directory, but could be adapted for the other
# Save table with next extra column.

# Read in all columns to a dataframe.
df = pd.read_csv(statsPathIn)
# Expected headings below, though only need country, sourcefile
#   ('country,sourcefile,year,sic,isin,CRpart,destfile\n')
#   The lambda function is used so getLang is applied to all rows,
#   using the country and sourcefile columns as input
#   and creating a new lang column as output.
df['lang'] = df.apply(lambda x: getLang(x['country'], x['sourcefile']), axis=1)
# Save the file back out (several hours later) with all original columns + 1
df.to_csv(statsPathOut, index=False, sep=',')
