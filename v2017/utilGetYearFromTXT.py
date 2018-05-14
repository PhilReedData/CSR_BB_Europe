#!/usr/bin/python    

# Get most likely year from first so many characters of TXT

import operator
import codecs

# How many characters to read?
LIMIT_1 = 150
LIMIT_2 = 2000

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
# Look at first <LIMIT_1> characters.
# If no year found, look at first <LIMIT_2> characters.
# If still no year found, give up.
def findModeYearInTXT(path):
    text = u''
    with codecs.open(path, 'r', encoding='utf8', errors='ignore') as fileIn:
        # Read in file as far as LIMIT_2
        text = fileIn.read(LIMIT_2)
    year = findModeYearInTXTHead(text, LIMIT_1)
    if year < 0:
        year = findModeYearInTXTHead(text, LIMIT_2)
    return year

# Search given text for most occuring year, or -2 if none.
# Look at first <LIMIT_1> characters.
# Look at first <LIMIT_2> characters.
# Return tuple of both results.
def findModeYearsInTXT(path):
    text = u''
    print ('Opening', path)
    with codecs.open(path, 'r', encoding='utf8', errors='ignore') as fileIn:
        # Read in file as far as LIMIT_2
        # What if limit exceeds file length?! TO DO
        text = fileIn.read(LIMIT_2)
    year1 = findModeYearInTXTHead(text, LIMIT_1)
    year2 = findModeYearInTXTHead(text, LIMIT_2)
    # Could extend this to mine entire file
    print ('year150', year1, 'year2000', year2)
    return (year1, year2)

# Search given text for most occuring year, or -2 if none.
# Look at characters from start of text to limit.
def findModeYearInTXTHead(text, limit):
    assert (limit > 0), "Year mining head, limit must be greater than zero."
    if limit <= len(text):
        # Don't read past end of text!
        # Only look at first so many characters
        text = text[:limit]
    
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
    # What about multi-mode? Need most recent? 
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
    


if __name__ == "__main__":
    y = findModeYearInText("2001 2006 2009 200120092008")
    print('mode',y)
    
