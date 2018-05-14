#!/usr/bin/python    

# Get most likely year from first page of PDF

import operator
import PyPDF2


    
# Year can be any of:
# TYPE_A 2006
# TYPE_B 2006-2007
# TYPE_C 2006-07
# Starting from 2000 up to 2019.
# Record year of range as the last year, eg 2006-07 is 2007
#   (So keep first two and last two digits).
# Problem that sometimes a different hyphen is used, or a slash.
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
        year = -3
    return year
    
# new blank matrix
# 2000:0, 2001:0, 2002:0, ...
def createYearMatrix():
    matrix = {}
    for year in range(start,end):
        matrix[year] = 0
    return matrix
    
# Search given text for most occuring year, or -2 if none.
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
    if highestFreq == 0:
        return -2 # no year found
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
    

def getTextContentOfPdfPages(path,startPage=0,endPage=1):
    content = ""
    p = file(path, "rb")
    pdf = PyPDF2.PdfFileReader(p)
    for i in range(startPage, endPage):
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

# Look for year in first page, if none found then second page, then third.
def findModeYearInPDF(path):
    year = findModeYearInText(getTextContentOfPdfPages(path, 0, 1))
    if year == -2: # no year found
        year = findModeYearInText(getTextContentOfPdfPages(path, 1, 2))
        if year == -2: # no year found
            year = findModeYearInText(getTextContentOfPdfPages(path, 2, 3))
    return year

def getPDFMetadata(path):
    p = file(path, "rb")
    try:
        pdf = PyPDF2.PdfFileReader(p)
        pdf_info = pdf.getDocumentInfo()
        return pdf_info
    except ValueError:
        print ('Error reading: ' + path)
        return []
    except Exception:
        print ('Exception reading: ' + path)
        return []
        
    
def getPDFMetaCreationYear(path, getWholeDate=False):
    meta = getPDFMetadata(path)
    if meta == None or len(meta) == 0:
        # Could not read file
        return -1
    keys = meta.keys()
    creationDateRaw = ""
    creationYear = -2
    for key in keys:
    #for item in meta:
        #print (item[0])
        if "creationdate" in key.lower():
            creationDateRaw = meta[key]
            if getWholeDate:
                return creationDateRaw
            break
    if len(creationDateRaw)>0:
        # Assume year is first instance of "20xx"
        try:
            start = creationDateRaw.index('20')
            creationYearString = creationDateRaw[start:start+4]
            creationYear = int (creationYearString)
        except ValueError:
            pass
        except Exception:
            pass
    return creationYear

if __name__ == "__main__":
    #y = findModeYearInText("2001 2006 2009 200120092008")
    #print('mode',y)
    
    #y = findModeYearInPDF("U:/Phil_Read/CSR_Europe/unzipped_raw/CH/122908_ADEN_Corporate_Responsibility_WD000000000096636192.pdf")
    path = "U:/Phil_Read/CSR_Europe/unzipped_raw/AT/060910_TKA_Corporate_Responsibility_SD000000002004960095.pdf"
    #t = getTextContentOfPdfPages(path, 0, 1)
    #print (t)
    #y = findModeYearInText(t)
    #print('mode page1',y)
    #y = findModeYearInText(getTextContentOfPdfPages(path, 1, 2))
    #print('mode page2',y)
    
    #meta = getPDFMetadata(path) 
    #print(str(meta))
    y = getPDFMetaCreationYear(path)
    print ('meta creation year',y)
    
