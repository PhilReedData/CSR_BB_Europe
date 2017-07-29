#!/usr/bin/python    

# Extract text from HTML document (whole or part)

import utilGetYearFromPDF
from bs4 import BeautifulSoup

# From https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
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
    
def getTitleTextFromHTML(html):
    soup = BeautifulSoup(html)
    try:
        text = soup.title.string
    except:
        text = ""
    return text

# For given path to HTM file, return most frequent year mentioned. 
def findModeYearInHTM(path):
    print ('Opening: ' + path)
    file = open(path, 'r')
    text = getPlainTextFromHTML(file.read())
    file.close()
    
    print (str(len(text)) + ' characters read.')
    year = utilGetYearFromPDF.findModeYearInText(text)
    
    return year
    
# Look at title in HTML document for first year mentioned.
def getHTMMetaYear(path):
    print ('Opening: ' + path)
    file = open(path, 'r')
    title = getTitleTextFromHTML(file.read())
    file.close()
    
    creationYear = -2
    if (not title is None) and (len(title)>0):
        # Assume year is first instance of "20xx"
        try:
            # Find what is probably a year between 2000 and 2019
            if ('200' in title) or ('201' in title):
                start = title.index('20')
                creationYearString = title[start:start+4]
                creationYear = int (creationYearString)
        except ValueError:
            pass
        except Exception:
            pass
    return creationYear

if __name__ == "__main__":
    path = "U:/Ser-Huang_Poon/UK_ARunzip/062816_WPP_11k1_d216619d11k.htm"
    y = findModeYearInHTM(path)
    print (y, 'body')
    path = "U:/Ser-Huang_Poon/UK_ARunzip/120611_GNC_Preliminary_Annual_WD000000002038486593.htm"
    y = getHTMMetaYear(path)
    print (y, 'title')