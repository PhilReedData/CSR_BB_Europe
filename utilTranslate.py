#!/usr/bin/python    
# -*- coding: utf-8 -*-

# utilTranslate
# Translate text to English
# 2017-09-19

import codecs 
import time
from os import makedirs
from os.path import exists

# test input, in Swedish
input = u'''
Några ord från koncernchefen
Hållbar utveckling
Våra policies och åtaganden
Hälsa och säkerhet
Anställdas utveckling och delaktighet
Balans mellan arbete och fritid
Djurförsök och etik
FoU-investeringar i Bangalore, Indien
Miljöprestanda Jämförelse av resultat Användning av naturresurser Avfall Användning av vatten Utsläpp till omgivningen Vatten Luft Energi- och klimatfrågan Transporter Hur vi uppfyller myndigheternas krav Läkemedel i miljön Andra frågor
Koncernchefens pris för framstående prestationer
Policy och etiska regler
Kontakta oss
'''

fileInLarge = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/2012_15_GB00BYSRJ698_CR1.txt"
fileInSmall = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/2009_20_GB0005758098_CR1.txt"
fileInSV = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/2000_35_GB0009895292_CR1.txt"

#METHOD 1: py-translate 1.0.3 (older but may be more reliable)
# https://pypi.python.org/pypi/py-translate
# pip install py-translate
# pip install futures
#from translate import translator
#result = translator('sv', 'en', input)
#print (result)
# WE GOT 503 ERRORS (BLOCKED) AFTER 3 RUNS!

#METHOD 2: googletrans 2.1.4 (newer)
# https://pypi.python.org/pypi/googletrans
# pip install googletrans
# LATEST: translation document limit is 15k characters. Ours are larger. 
#   Need to break them up, sensibly.
from googletrans import Translator
translator = Translator()

#METHOD 3: translate
# pip install translate
# https://github.com/terryyin/google-translate-python
# Uses http://mymemory.translated.net/  and 1000 words per day
# Default en to cn, change: auto to en.

# METHOD 2
def translateToEn(input):
    charsS = str(len(input))
    print('Pausing 1 second before translating ' + charsS +' chars')
    time.sleep(1)
    result = translator.translate(input)
    return result.text

# Take the whole report (string) and return the whole translation. 
def translateInChunks(input):
    chunkSize = 5000
    chars = len(input)
    charsS = str(chars)
    print('Input has ' + charsS + ' character(s)')
    if chars > chunkSize:
        print ('Too big, just use first ' + str(chunkSize) + ' characters.')
        input = input[:chunkSize]
    
    result = translateToEn(input)
    return result

def loadFile(fileIn=fileInLarge):
    with codecs.open(fileIn, 'r', encoding='utf8', errors='ignore') as fileIn:
        foreignText = fileIn.read()
    return foreignText
    # Do translation, don't overload server
    #chars = str(len(foreignText))

def writeFile(englishText, path):
    with codecs.open(path, 'w', encoding='utf8', errors='ignore') as fileOut:
        fileOut.write(englishText)

if __name__ == "__main__":
    #result = translator.translate(input)
    #foreignText = loadFile(fileInSV)
    #resultText = translateInChunks(foreignText)
    #result = translator.translate(foreignText)
    #resultSrc = result.src
    #resultDest = result.dest # = 'en'
    #resultText = result.text
    #resultPronunciation = result.pronunciation # = None
    #print ('Translated from '+ resultSrc + ' to ' + resultDest + ':')
    #print (resultText[:200] + '...')
    
    # Read in list to translate, save back
    fromDir = "U:/Phil_Read/CSR_UK_latest_txt_all_flat/"
    toDir = "U:/Phil_Read/CSR_UK_latest_txt_all_flat_trns/"
    listPath = "./x_toBeTranslated.txt"
    if not exists(toDir):
        makedirs(toDir)
    foreignReports = open(listPath,'r').read().split('\n')
    for filename in foreignReports[:1]: # TEMP LIMIT TO FIRST REPORT
        print ('Read from ' + fromDir + filename)
        foreignText = loadFile(fromDir + filename) # should use os join
        resultText = translateInChunks(foreignText)
        charsOut = str(len(resultText))
        print ('Writing ' + charsOut + ' character(s).')
        writeFile(resultText, toDir+filename)

