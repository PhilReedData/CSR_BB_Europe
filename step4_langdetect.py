#!/usr/bin/python    

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import PyPDF2
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

from os.path import join

unzipPath = "U:/Phil_Read/CSR_Europe/unzipped_raw/"
statsPathIn = 'statsB.csv'
statsPathOut = 'statsB_langB.csv'
logPath = 'log_lang.csv'
with open(logPath, 'w') as logFile:
    logFile.write('country, sourcefile, lang\n')

# Get the text of first 5 pages of given PDF file, or other range.
def getTextContentOfPdfPages(path, start=0, end=5):
    content = ""
    p = file(path, "rb")
    try:
        pdf = PyPDF2.PdfFileReader(p) # Replace pyPdf with PyPDF2 ?
    except:
        print ('Error reading file: ' + path)
        return content # can't open file.
    for i in range(start, end):
        try:
            content += pdf.getPage(i).extractText() + "\n"
        except Exception:
            print ('Problem reading page '+ str(i+1) +': ' + path)
            pass # may not be that many pages!
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def getPlainTextFromHTML(html):
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text    

def getPlainTextFromHTMLPath(path):
    file = open(path, 'r')
    text = getPlainTextFromHTML(file.read())
    file.close()
    return getPlainTextFromHTML(text)
    
# Detect the language of the report
def getLang(country,filename):
    if country == 'GB':
        return '-2' # skip GB
    filenamesToSkip = [
        "072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf",
        "052715_INF_Corporate_Responsibility_SD000000002233279310.pdf",
        "050808_BARC_Corporate_Responsibility_SD000000000083695052.pdf",
        "072808_NRE1V_Corporate_Responsibility_WC000000000087573266.pdf"
        ]
    if filename in filenamesToSkip:
        return '-2' # corrupt file
    if not filename.endswith('.pdf'):
        return '-3' # not implemented HTM file yet

    fullPath = join(unzipPath, country + '/' + filename)
    print ('Reading: ' + fullPath)
    
    textToTest = ""
    if filename.endswith('.pdf'):
        textToTest = getTextContentOfPdfPages(fullPath)
    elif filename.endswith('.htm'):
        textToTest = getPlainTextFromHTMLPath(fullPath)
    try:
        lang = detect(textToTest)
    except LangDetectException:
        lang = '-1'
    print ('Detected: ' + lang)
    
    # Extend search if not found and PDF
    if (filename.endswith('.pdf')) and (lang=='-1'):
        textToTest = getTextContentOfPdfPages(fullPath, 5, 10)
        try:
            lang = detect(textToTest)
        except LangDetectException:
            lang = '-1'
        print ('Detected: ' + lang)
    with open(logPath, 'a') as logFile:
        logFile.write(country+', '+filename+','+lang+'\n')
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
