#!/usr/bin/python    

# x_CRtxt_langdectect.py
# Detect the language for a given directory of text files.
# 2017-09-12
# 2017-11-25 newer file name convensions

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import codecs
from os import listdir, mkdir
from os.path import isfile, join, exists

parentPathIn = "U:/Ser-Huang_Poon/UK_CRunzip_txt/"
logPath = "x_CRtxt_langdectect.csv"
logFile = open(logPath, 'w')
SEP = ','
# Header
logFile.write('filename'+SEP+'lang\n')


# Get all files
files = [f for f in listdir(parentPathIn) if isfile(join(parentPathIn, f))]
files.sort()
print ('Files', len(files))
for filePath in files:
    fullPath = join(parentPathIn, filePath)
    data = ""
    with codecs.open(fullPath, 'r', encoding='utf8', errors='ignore') as file:
        data = file.read()
    if filePath.endswith('.pdf'):
        # Don't read PDF
        data = ""
    elif filePath.endswith('.htm'):
        # Don't read HTML
        data = ""
    try:
        lang = detect(data)
    except LangDetectException:
        lang = '-1'
    print(filePath, lang)
    logFile.write(filePath + SEP + lang + '\n')
logFile.close()
