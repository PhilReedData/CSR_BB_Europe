#!/usr/bin/python    

# Get most likely year from first page of PDF

import operator
import pyPdf


    
# Year can be any of:
# TYPE_A 2006
# TYPE_B 2006-2007
# TYPE_C 2006-07
# Starting from 2000 up to 2019.
# Record year of range as the last year, eg 2006-07 is 2007
#   (So keep first two and last two digits).
# Problem that sometimes a different hyphen is used.
start = 2000
end = 2019
ALL_TYPE_A = []
ALL_TYPE_B = []
ALL_TYPE_C = []
for year in range(start, end):
    ALL_TYPE_A.append(str(year))
    ALL_TYPE_B.append(str(year) + '-' + str(year+1))
    ALL_TYPE_C.append(str(year) + '-' + str(year+1)[:-2])
ALL_YEAR_STRINGS = ALL_TYPE_A + ALL_TYPE_B + ALL_TYPE_C

# from 2006 to 2006, from 2006-2007 to 2007, from 2006-07 to 2007
def getYearStringValue(ys):
    try:
        year = int(ys[0:2] + ys[-2:])
    except ValueError:
        year = -1
    return year
    
# new blank matrix
# 2000:0, 2001:0, 2002:0, ...
def createYearMatrix():
    matrix = {}
    for year in range(start,end):
        matrix[year] = 0
    return matrix
    
# Search given text for most occuring year, or -1 if none.
def findModeYearInText(text):
    # Blank new matrix
    yearMatrix = createYearMatrix()
    for yearString in ALL_YEAR_STRINGS:
        # May need regex here instead, to catch word breaks
        # ie would now catch 3201699 as a year.
        numMatches = text.count(yearString)
        if numMatches > 0:
            # Increment count of that year 
            print(yearString, numMatches)
            yearMatrix[getYearStringValue(yearString)] += numMatches
    # Matrix is full, now analyse
    sortedYearMatrix = sorted(yearMatrix.items(), key=operator.itemgetter(1), reverse=True)
    # Sorted list of tuples instead of dict (year, freq)
    # What about multi-mode? Need most recent? TO DO
    highestFreq = sortedYearMatrix[0][1]
    yearsWithHighestFreq = []
    latestYearWithHighestFreq = sortedYearMatrix[0][0]
    # Loop through years, increasing the year 
    # until we hit the next frequency band lower
    for yearTuple in sortedYearMatrix:
        year = yearTuple[0]
        freq = yearTuple[1]
        if freq < highestFreq: 
            break
        latestYearWithHighestFreq = year   
    return latestYearWithHighestFreq
    

def getTextContentOfPdfPage1(path):
    content = ""
    num_pages = 1
    p = file(path, "rb")
    pdf = pyPdf.PdfFileReader(p)
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText() + "\n"
    #content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def findModeYearInPDF(path):
    return findModeYearInText(getTextContentOfPdfPage1(path))

    

if __name__ == "__main__":
    y = findModeYearInText("2001 2006 2009 200120092008")
    print('mode',y)
    
    #y = findModeYearInPDF("U:/Phil_Read/CSR_Europe/unzipped_raw/CH/122908_ADEN_Corporate_Responsibility_WD000000000096636192.pdf")
    #print('mode',y)
    