#!/usr/bin/python    

# x_CRtxt_langdectect.py
# Detect the language for a given list of directories of text and html files.

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import codecs
from os import listdir, mkdir
from os.path import isfile, join, exists
from bs4 import BeautifulSoup


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


parentPathIn = "U:/Ser-Huang_Poon/UK_CRtxt&hml/"
yearDirs = [
    "-1/txt", "2000", "2001", "2002", "2003", "2004", "2005",
    "2006", "2007", "2008", "2009", "2010", "2011", "2012", 
    "2013", "2014", "2015", "2016", "2017"
    ]
logPath = "x_CRtxt_langdectect.csv"
logFile = open(logPath, 'w')
SEP = ','
# Header
logFile.write('year'+SEP+'filename'+SEP+'lang\n')

# For each year
for yearDir in yearDirs:
    # Get all files
    files = [f for f in listdir(join(parentPathIn, yearDir)) if isfile(join(parentPathIn+yearDir, f))]
    files.sort()
    print (yearDir, len(files))
    for filePath in files:
        fullPath = join(parentPathIn+yearDir, filePath)
        data = ""
        with codecs.open(fullPath, 'r', 'utf-8') as file:
            data = file.read()
        if filePath.endswith('.pdf'):
            # Don't read PDF, too slow!
            data = ""
        elif filePath.endswith('.htm'):
            # Strip HTML
            data = getPlainTextFromHTML(data)
        try:
            lang = detect(data)
        except LangDetectException:
            lang = '-1'
        logFile.write(yearDir +SEP+ filePath + SEP + lang + '\n')
logFile.close()