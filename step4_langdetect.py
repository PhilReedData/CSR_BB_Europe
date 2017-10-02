#!/usr/bin/python    

# Updated 2017-10-02: Now reads from flat directory of TXT reports
# with the original filenames from Bloomberg.
# Various bits using PDF/HTM will be deleted.

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import PyPDF2
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import codecs

from os.path import join

unzipPath = "U:/Phil_Read/fromIrina/Europe_CSR_txt/"
statsPathIn = 'stats.csv'
statsPathOut = 'stats_lang.csv'
logPath = 'log_lang.csv'
with open(logPath, 'w') as logFile:
    logFile.write('sourcefile, lang\n')

# NOT USED
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

# NOT USED
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

# NOT USED
def getPlainTextFromHTMLPath(path):
    file = open(path, 'r')
    text = getPlainTextFromHTML(file.read())
    file.close()
    return getPlainTextFromHTML(text)

def getPlainTextFromTXTPath(path):
    text = u''
    with codecs.open(path, 'r', encoding='utf8', errors='ignore') as fileIn:
        text = fileIn.read()
    return text
    
# Detect the language of the report
def getLang(country,filename):
    # We are now using txt versions of reports, not PDF
    filename = filename.replace('.pdf','.txt')
    filenamesToSkip = [
        "072409_BNP_Corporate_Responsibility_WC000000001985010381.pdf",
        "052715_INF_Corporate_Responsibility_SD000000002233279310.pdf",
        "050808_BARC_Corporate_Responsibility_SD000000000083695052.pdf",
        "072808_NRE1V_Corporate_Responsibility_WC000000000087573266.pdf"
        ]
    if filename in filenamesToSkip:
        return '-2' # corrupt file
    if not (filename.endswith('.txt')):
        return '-3' # only interested in txt reports
    # NOT USED:
    #if not (filename.endswith('.pdf') or filename.endswith('.htm')):
    #    return '-3' # not implemented other files yet

    fullPath = join(unzipPath, filename)
    print ('Reading: ' + fullPath)
    
    textToTest = ""
    try:
        if filename.endswith('.txt'):
            textToTest = getPlainTextFromTXTPath(fullPath)
        elif filename.endswith('.pdf'): # NOT USED:
            textToTest = getTextContentOfPdfPages(fullPath)
        elif filename.endswith('.htm'): # NOT USED:
            textToTest = getPlainTextFromHTMLPath(fullPath)
    except IOError as ioe:
        print ('Error reading from: ' + fullPath)
        lang = '-4'
        with open(logPath, 'a') as logFile:
            logFile.write(filename+','+lang+'\n')
        return lang
    try:
        # Do the language detection
        lang = detect(textToTest)
    except LangDetectException:
        lang = '-1'
    print ('Detected: ' + lang)
    
    # NOT USED:
    # Extend search if not found and PDF
    if (filename.endswith('.pdf')) and (lang=='-1'):
        textToTest = getTextContentOfPdfPages(fullPath, 5, 10)
        try:
            lang = detect(textToTest)
        except LangDetectException:
            lang = '-1'
        print ('Detected: ' + lang)
    with open(logPath, 'a') as logFile:
        logFile.write(filename+','+lang+'\n')
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
